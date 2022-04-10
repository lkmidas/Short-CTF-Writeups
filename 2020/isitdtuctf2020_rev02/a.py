from z3 import BitVec, Solver, Or

v = []
for i in range(16):
    v.append(BitVec('v' + str(i), 8))

s = Solver()

for i in range(16):
    s.add(Or((v[i] == ord('t')), (v[i] == ord('u')), (v[i] == ord('a')), (v[i] == ord('n')), (v[i] == ord('l')), (v[i] == ord('i')), (v[i] == ord('h'))))

s.add(v[0] + v[1] + v[2] == 0x4a)
s.add(v[1] + v[2] + v[3] == 0x44)
s.add(v[2] + v[3] + v[4] == 0x3b)
s.add(v[3] + v[4] + v[5] == 0x43)
s.add(v[4] + v[5] + v[6] == 0x43)
s.add(v[5] + v[6] + v[7] == 0x3f)
s.add(v[6] + v[7] + v[8] == 0x42)
s.add(v[7] + v[8] + v[9] == 0x42)
s.add(v[8] + v[9] + v[10] == 0x42)
s.add(v[9] + v[10] + v[11] == 0x37)
s.add(v[10] + v[11] + v[12] == 0x3d)
s.add(v[11] + v[12] + v[13] == 0x43)
s.add(v[12] + v[13] + v[14] == 0x4b)
s.add(v[13] + v[14] + v[15] == 0x4c)

s.check()
ans = s.model()
result = ''
for i in range(0, 16):
    result += chr(ans[v[i]].as_long())
print result
