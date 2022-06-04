from z3 import *

s = Solver()

v = [0] * 9
for i in range(9):
    v[i] = BitVec("v_{}".format(i), 32)
    s.add(And(v[i] >= 0x5f, v[i] <= 0x7a))
    s.add(v[i] != 0x60)

x = 1
y = 0
for i in range(len(v)):
    t = URem((v[i] + x), 0xfff1)
    x = t & 0xffff
    t = URem((y + x), 0xfff1)
    y = t & 0xffff

z = x ^ y
s.add(z == 0x12e1)

if s.check():
    model = s.model()
    result = [chr(model[v[i]].as_long()) for i in range(9)]
    print(result)