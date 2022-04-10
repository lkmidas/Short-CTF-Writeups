from malduck import unhex, u16
from z3 import *

KEY = bytearray(unhex(b"450144013B011B01FB00FB0020013C015101420147013B0141012C01400119011901160147015D014301350132013801360130013A014A014901430142013E013401FA00F200D900E600D200D100D600D700D300D400A900890063006300BF0008014A01"))
flag = []
for i in range(55):
	flag.append(BitVec('flag' + str(i), 16))

s = Solver()
s.add(And(flag[0] == ord('j'), flag[1] == ord('c'), flag[2] == ord('t'), flag[3] == ord('f'), flag[4] == ord('{'), flag[54] == ord('}')))

# Printable condition
for i in range(5, 55):
    s.add(And(flag[i] >= 0x21, flag[i] <= 0x7e))

# Flag check
for i in range(7, 55):
    s.add(flag[i%0x37] + flag[(i-1)%0x37] + flag[(i-2)%0x37] == u16(KEY[i*2-14 : i*2-14+2]))

sol_count = 0
while sol_count < 10 and s.check() == sat:
    model = s.model()

    result = ""
    for i in range(55):
	    result += chr(model[flag[i]].as_long())
    print(result)

    sol_count += 1

    cond = True
    for i in range(55):
        cond = And(cond, flag[i] == model[flag[i]])
    s.add(Not(cond))

print("Done")