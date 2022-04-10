
# EFIENSCTF2019R2: INTERPRETATION(pwn)
## First look
- Given files: `interpreter`, `libc-2.27.so`.
- This is a beginner-level ret2libc challenge.
- I am this challenge's author.
## Analysis
**(0)** The binary has no PIE.

**(1)** The interpreter has 8 opcodes `RLPMOISE`, these have the same funcitonalities as `brainf*ck`'s opcodes.

**(2)** The memory upper bound check  of opcode `R` is bigger than the actual memory's size -> out of bound.

## Exploit plan
**Step 1:** Pass in a program that uses opcodes `R` and `I`  to overwrite `main()`'s return address to ROP into `puts()` and leak libc, then return to `main()`.

**Step 2:** Pass in the same program in step 1 to overwrite `main()`'s return address to ROP into `system()`.

## Full exploit
See `solve.py`.
