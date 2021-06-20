Debugger: no$gba + desmume
Disassembler/Decompiler: ghidra with NDS plugin

Solution: basically find input buffer -> set read breakpoint -> trace to function -> reverse function
    - stage 1: input buffer gets copy around several times, then directly compare char by char
    - stage 2: input stored as int array, then check using simple equations
    - stage 3: "cheat" stored as int array, then directly compare to open the way to goal