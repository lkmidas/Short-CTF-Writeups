# ASCIS2020 FINAL: RWE (RE)
- Given files: `rwe`, `description`.
- The `rwe` file is an ELF 32-bit executable statically compiled and stripped. It asks for an input command when being executed.
- The `description` file says: *"Please try to read flag.txt file"*.
## Analysis

### Step 1: Analyze main function (IDA Pro)
The binary is stripped, so IDA can't identify the `main` function, but because this is an ELF file, I could identify where `main` is by inspecting the `start` function, it is `sub_804CD40`.

Initially, IDA cannot decompile `main` because it fails to analyze the indirect `call` at address `0x0804CE9F`. By checking the `Stack pointer` box in IDA's `Option -> General` to show the stack pointer analysis at each instruction, I saw that the `call` instruction subtracts the sp value by a lot, which is not normal and is also the reason why IDA can't analyze it. Thanks to `@lanleft`'s suggestion, I modified that value (by pressing `alt + k`) to a reasonable one and then IDA can decompile it cleanly.

All of the libc functions are also stripped, which makes reverse engineering a lot harder. Normally, we can use the following trick to "unstrip" the binary: statically compile a dummy binary and use a binary diffing tool (`BinDiff` or `diaphora`) to compare the two binaries and identify the similar functions. However, most of the functions in this binary is not that hard to recognize based on its parameters if you are familiar with ELFs, so I just assumed them all this way. 

The program first prints out a banner and a prompt, then read in 512 bytes of input. The complex block of code after reading input is actually just `buf[strlen(buf)-1] = '\0'`, I recognized this by debugging and googling some weird constants. Next is a call to `sub_804D930`, which is a base64 decoding routine on our input (this can be assumed easily without digging into it by using IDA plugin `findcrypt`). After that comes the important part: the program initializes a struct, assigns one of its field to be a function-pointer table, allocates and assigns two big memory spaces and copy our decoded input into one of it (in `sub_804E390` and `sub_804E2B0`). This immediately gave me an idea that this is a virtual machine, the two memory spaces are the code and the stack, but those were just assumptions that would later be verified when I dug deeper into it.

### Step 2: Analyze VM execution (IDA Pro + gdb)
The VM's execution function is the second function in the function table, which gets called right after initialization. The function is supringly simple with only 3 cases of opcodes: `DE`, `DF` and `DD`. Analyzing these small cases gave me the following information: 
- The 2 fields I mentioned earlier are indeed the code and the stack, they are managed by a program counter and a stack pointer.
- There are also 6 other registers, I named them `reg0` to `reg5`.
- `DE` and `DF` are 2-byte instructions, which are `pop regX` and `push regX`, `X` must be less than or equal to 5.
- `DD` is a 5-byte instruction, which is `push imm32`, `imm32` must be less than or equal to 0x1000, we will see later that actually all `imm32` in this VM must satisfy that condition.

After that comes the weird part that answers why the code is so simple: if the opcode is not any of those, the VM will subtract it by 0x10 and use it as an index to an offset table to retrieve an offset from `0x820A000`, then jump to that location. By using a simple python script, I could identify the destination of each corresponding opcodes:
```
OFFSETS = [4293147974, 4293149121, 4293149088, 4293147991, 4293147991, 4293147991, 4293147991, 4293147991, 4293147991, 4293149037, 4293147991, 4293147991, 4293147991, 4293147991, 4293147991, 4293148998, 4293148934, 4293148871, 4293148827, 4293148768, 4293147991, 4293147991, 4293147991, 4293147991, 4293147991, 4293147991, 4293147991, 4293147991, 4293147991, 4293147991, 4293147991, 4293147991, 4293148718, 4293147991, 4293147991, 4293147991, 4293147991, 4293148608, 4293147991, 4293147991, 4293147991, 4293147991, 4293147991, 4293147991, 4293147991, 4293147991, 4293147991, 4293147991, 4293148514, 4293147991, 4293147991, 4293147991, 4293147991, 4293147991, 4293147991, 4293147991, 4293147991, 4293147991, 4293147991, 4293147991, 4293147991, 4293147991, 4293147991, 4293147991, 4293148441, 4293148330, 4293147991, 4293147991, 4293147991, 4293147991, 4293147991, 4293147991, 4293147991, 4293147991, 4293147991, 4293147991, 4293147991, 4293147991, 4293147991, 4293147991, 4293148222, 4293148110, 4293147991, 4293147991, 4293147991, 4293147991, 4293147991, 4293147991, 4293147991, 4293147991, 4293147991, 4293147991, 4293147991, 4293147991, 4293147991, 4293147991, 4293147991, 4293147991, 4293147991, 4293147991, 4293147991, 4293147991, 4293147991, 4293147991, 4293147991, 4293147991, 4293147991, 4293147991, 4293147991, 4293147991, 4293147991, 4293147991, 4293148079, 4293148040, 4293147999, 4293147991, 4293147991, 4293147991, 4293147991, 4293147991, 4293147991, 4293147991, 4293147991, 4293147991, 4293147991, 4293147991, 4293147991, 4293147991, 4293147923]
all_insts = {}

for i in range(len(OFFSETS)):
    all_insts[i] = 0x820A000 + OFFSETS[i] - 0x100000000
    
temp = {val : key for key, val in all_insts.items()} 
insts = {val : key for key, val in temp.items()} 
for key, val in insts.items():
    print("{} : {}".format(hex(key + 0x10), hex(val)))
```

But because of this specific handler of opcodes, IDA can't know in advance what is the destination of each opcodes, therefore it can't decompile them. I got stuck here for a while trying to read and understand the asm code, but it was kinda hopeless, so I came up with an idea: patching the jump of one of the push/pop instructions so that it jumps into the opcode I wanted to decompile, by this way I could analyze the opcodes one by one, here are their functionalities (actually only 2 additional opcodes are required for the solution, but I decided to reverse them all anyway to practice a bit, the opcodes marked with `?` are the ones that I am unsure about):
```
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
```

### Step 3: Writing the code to read flag.txt (pwntools)
So then based on what `description` says, my goal is to read the `flag.txt` file. Being a pwnable player, because we have an opcode to make a syscall, I knew that we can achieve this by writing a piece of VM code to call `execve("/bin/sh", NULL, NULL)` or writing an `open-read-write` chain. But since I didn't know the absolute path to the flag file, I went with the `execve` way (which is also simpler).

The code is actually extremely simple: I put `execve` syscall number (`0x0b`) into `reg0`, `0x00` into `reg2` and `reg3` by using pushes and pops. The `/bin/sh\0` string for `reg1` can be inserted at the end of our input code, and then I used opcode `19` to put its address into `reg1`. Finally, a syscall instruction is called to open the shell.

```
from pwn import *
from base64 import b64encode

r = process("./rwe")

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
```