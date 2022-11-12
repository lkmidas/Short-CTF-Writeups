import ida_bytes

def decrypt_xor(addr):
    name = []
    while (1):
        b = ida_bytes.get_bytes(addr, 1)
        if b == b"\x00":
            break
        name += [ord(b.decode()) ^ 0x17]
        addr += 1
        
    return ''.join([chr(x) for x in name]
)