# ISITDTU2020 QUALS: REV02 (RE)
- Given files: `rev02.nes`.
- The given file is a **NES ROM** file, which is a game ROM for the NES 8-bit video game console. The NES is based on the **6502 microcontroller** with a custom video controller called PPU. Therefore, this is essentially a 6502 assembly reverse engineering challenge.
## Analysis
I first try to load the file into different disassemblers, namely **IDA** and **Ghidra**. By default, **IDA** doesn't have the option to analyze 6502 code. **Ghidra** on the other hand can, but provides poorly formatted assembly and wrong decompiled code.

Later, the author suggested on the competition's Discord channel a program to emulate and debug NES files called **FCEUX** ([download link](http://fceux.com/web/download.html)). This is the tool which I used to solve this challenge.

*Static analysis:* by opening the ROM in FCEUX and  then opening the **Debugger** window, I could begin static analyzing the ROM. Looking around the **code** section (which is loaded at address **0x8000**) didn't reveal much, 6502 is a new architecture for me after all. Therefore, I started looking into the **data** that come after the code, I found the 2 interesting strings which are `GIVE ME THE PASSWORD` and `Correct! ISITDTU{`. By these, I could predict that this ROM will wait for a password to be entered, check it and then give us the flag if the password is correct.

*Dynamic Analysis*: I tried continuing static analyzing for a bit, but that didn't yield much result, so I started to analyze it dynamically. The program doesn't have any visual effect on the screen, it's just pitch black, but the author did say that the program still accepts input normally. Therefore, I opened the **Hex Editor** window to inspect the memory in real time and then started **button mashing** and found 2 keys to solve this:
- The input is stored at a 16 bytes buffer starting at address **0x300** in the memory space.
- The only **7 valid input keys** on the keyboard are: `s`, `d`, `f` and the arrow buttons. They are also mapped into the memory in the following way: `{s:a, d:u, f:t, left:l, right:i, up:n, down:h}`.

Using the info that the input buffer is at **0x300**, I then looked into the code to find the part of it which access that buffer. That code started at address **0x9131**:
```
 00:9131:A2 00     LDX #$00
 00:9133:AD 00 03  LDA $0300
 00:9136:18        CLC
 00:9137:6D 01 03  ADC $0301
 00:913A:90 02     BCC $913E
 00:913C:E8        INX
 00:913D:18        CLC
 00:913E:6D 02 03  ADC $0302
 00:9141:90 01     BCC $9144
 00:9143:E8        INX
 00:9144:E0 01     CPX #$01
 00:9146:F0 03     BEQ $914B
 00:9148:4C 34 93  JMP $9334
 00:914B:C9 4A     CMP #$4A
 00:914D:F0 03     BEQ $9152
 00:914F:4C 34 93  JMP $9334
 00:9152:CA        DEX
 ... (the same code snippet for the remaining bytes)
 ```
By reversing the instructions one by one while looking at the 6502 instruction set, its functionality can be briefly described as follow: *It loops through all the bytes in the buffer one by one, each byte is added with the two next bytes in the sequence, the result is then compared to a constant value*. This makes the checking process a **system of  14 equations** on 16 values, with the constraint being the values can only be one of the 7 characters listed above.
## Solution
I solved the equations using `z3`. The code itself is pretty simple: initialize a list of 16 `BitVec` of length 8, add the constraints and the equations, then just let the machine do the work. (see `a.py` for details).

The password is: `tuanlinhlnhatniu`

Using the mapping above and input the correct sequence into the emulator printed out the flag on the black screen: `ISITDTU{omg_the_nes-ted_if_in_n3s_is_s0_c00l}`.

