# Chall4
- The program XOR an initialized stack buffer with our input, then run it as shellcode
- We don't want the program to crash, so we will use the input to make the shellcode containing only `ret` instructions (0xc3)
