# SECCON2018: KINDVM (pwn)
## First look
- Given file: `kindvm`
- This is a 32-bit ELF that implement some kind of VM.
- The VM has 10 instructions:
```
0            : NOP
1 imm8  imm16: LOAD reg[imm8], mem[imm16]
2 imm16 imm8 : STORE mem[imm16], reg[imm8]
3 imm8  imm8 : MOV reg[imm8], reg[imm8]
4 imm8  imm8 : ADD reg[imm8], reg[imm8]
5 imm8  imm8 : SUB reg[imm8], reg[imm8]
6            : HALT
7 imm8  imm32: IN reg[imm8], imm32
8 imm8       : OUT imm[8]
9            : HINT
```
- It seems like the challenge provides some hint within the binary, but it is not needed.
## Vulnearability
**(0)** No PIE.

**(1)** `imm16` in `LOAD` and `STORE` is treated as signed, results in OOBRW in `mem`.

**(2)** `open_read_write()` function can read any file.
## Exploit plan
**Step 1:** Input the name as `"./flag.txt"` for later use.

**Step 2:** Because the `kc` is stored preceded to `mem`, we use `LOAD + OUT` to leak the `kc->name`, and `IN + STORE` to overwrite `kc->farewell` to `main`, then `HALT`.

**Step 3:** We are back to main, send a random name, then use `IN + STORE` to overwrite `kc->banner` to the leaked name address, then `HALT`. After halting, `kc->farewell()` will open_read_write the flag.
## Full exploit
See `solve.py`
