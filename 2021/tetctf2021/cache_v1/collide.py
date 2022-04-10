INV_MAGIC = 0x5f7a0ea7e59b19bd
R = 16
MASK64 = 0xffffffffffffffff
DIFF = b"\x00\x00\x00\x00\x00\x00\x00\x80\x00\x00\x00\x00\x00\x00\x00\x80"
m = (0xc6a4a793 << 32) | 0x5bd1e995
h = (0xc70f6907 ^ (16 * m)) & (2**64 - 1)
r = 47

def unshiftRight(x, shift):
    res = x
    for i in range(64):
        res = x ^ res >> shift
    return res

def invert64(n):
    x = (n * 0x5f7a0ea7e59b19bd) & MASK64
    x = unshiftRight(x, r)
    x = (x * 0x5f7a0ea7e59b19bd) & MASK64
    return int.to_bytes(x, 8, 'little')

a = b'A'*16
b = bytes(x^y for x,y in zip(a,DIFF))

x1, x2 = int.from_bytes(a[:8], 'little'), int.from_bytes(a[8:], 'little')
y1, y2 = int.from_bytes(b[:8], 'little'), int.from_bytes(b[8:], 'little')

print((invert64(y1) + invert64(y2)).hex())
print((invert64(x1) + invert64(x2)).hex())