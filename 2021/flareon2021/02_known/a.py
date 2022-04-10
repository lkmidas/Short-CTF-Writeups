import struct

def __ROL__(n, d):
    return ((n << d)|(n >> (8 - d))) & 0xFF

def __ROR__(n, d):
    return ((n >> d)|(n << (8 - d))) & 0xFF

def decrypt_once(data, key):
    result = b""
    for i in range(8):
        result += struct.pack("B", (__ROL__(key[i] ^ data[i], i) - i) & 0xff)
    return result

enc = open("./Files/critical_data.txt.encrypted", "rb").read()

png_magic = b"\x89\x50\x4E\x47\x0D\x0A\x1A\x0A"
png_magic_enc = b"\xC7\xC7\x25\x1D\x63\x0D\xF3\x56"

key = b""
for i in range(8):
    key += struct.pack("B", __ROR__((png_magic[i] + i) & 0xFF, i) ^ png_magic_enc[i])

print("key =", key)

dec = b""
for i in range(0, len(enc), 8):
    dec += decrypt_once(enc[i:i+8], key)

print(dec)


