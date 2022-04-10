from z3 import *
from pwn import *

data = b"\xBF\x96\xAA\x46\x11\x23\x6B\xB2\x73\x5E\x5C\x54\x46\x54\x42\x42\x54\x58\x4E\x52\x53\x53\x4D\x1E\x60\x07\x2E\x22\x23\x65\x2F\x34\x68\x6E\x09\x1F\x0A\x36\x16\x17\x08\x2C\x75\x73\x23\x3D\x33\x25\x3D\x79\x02\x03\x04\x7D\x37\x2C\x40\x18\x0D\x16\x16\x45\x0F\x09\x18\x1C\x1E\x45\x66\x39\x1C\x16\x50\x10\x15\x12\x1D\x1B\x57\x7D"
target = b""
k = 0x28
for i in range(80):
    target += p8((data[i] ^ k) & 0xff)
    k += 1

def hex1(r0, r1):
    if (r1 & (1 << 6)):
        return ~((r0 + 0x7A024204) & 0xffffffff)
    else:
        return ~((r0 + 0xA5D2F34) & 0xffffffff)

def hex2(r0, r1):
    if (r1 & (1 << 3)):
        return ((r0 ^ 0xE6F4590B) + 0x5487CE1E) & 0xffffffff
    else:
        return (~r0) ^ 0x48268673

def hex3(r0, r1):
    if (r1 & (1 << 8)):
        return ((~r0) + -0x7A889166) & 0xffffffff
    else:
        return ((r0 ^ 0x5A921187) + -0x1644E844) & 0xffffffff

def hex4(r0, r1):
    if (r1 & (1 << 0)):
        return r0
    else:
        return (~r0) ^ 0xD71037D1

def hex5(r0, r1):
    if (r1 & (1 << 0)):
        return ((~r0) + 0x101FBCCC) & 0xffffffff
    else:
        return ((~r0) + 0x55485822) & 0xffffffff

def hex6(r0, r1):
    if (r1 & (1 << 3)):
        return (r0 ^ 0x49A3E80E) ^ 0x6288E1A5
    else:
        return (r0 ^ 0x8B0163C1) ^ 0xEECE328B

f = [0]*4
f[3] = BitVec("flag_r3", 32)
f[2] = BitVec("flag_r2", 32)
s = Solver()

r0 = f[2]
r2 = 0x6F67202A
r1 = 1
r0 = hex1(r0, r1)

r2 = r2 ^ r0
r0 = f[3]
r3 = 0x656C676F
r1 = 6
r0 = hex2(r0, r1)

r3 = r3 ^ r0
r0 = 0x6E696220
r1 = 0xf
r0 = hex3(r0, r1)

r0 = r0 ^ r3
tmp_r2 = r2
r2 = r3
r3 = tmp_r2 ^ r0
r0 = 0x682D616A
r1 = 0x1c
r0 = hex4(r0, r1)

r0 = r0 ^ r3
tmp_r2 = r2
r2 = r3
r3 = tmp_r2 ^ r0
r0 = 0x67617865
r1 = 0x2d
r0 = hex5(r0, r1)

r0 = r0 ^ r3
tmp_r2 = r2
r2 = r3
r3 = tmp_r2 ^ r0
r0 = 0x2A206E6F
r1 = 0x42
r0 = hex6(r0, r1)

r0 = r0 ^ r3
tmp_r2 = r2
r2 = r3
r3 = tmp_r2 ^ r0

x = u64(target[:8])
s.add(r2 == (x & 0xffffffff))
s.add(r3 == (x >> 32))

sol_count = 0
solutions = []

print("Checking")
print(target)

while sol_count < 5 and s.check() == sat:
    model = s.model()
    result = [model[f[i]].as_long() for i in range(2, 4)]
    print(p32(result[0]) + p32(result[1]))

    solutions.append(result)
    sol_count += 1

    print("sol_count=", sol_count)

    cond = True
    for i in range(2, 4):
        cond = And(cond, f[i] == result[i-2])

    s.add(Not(cond))

