
from z3 import *
from malduck import p32, u32


args = [0]*14
for i in range(14):
    args[i] = BitVec("args{}".format(i), 4*8)

s = Solver()

for i in range(14):
    s.add(args[i] % 256 <= 0x7e)
    s.add((args[i] >> 8) % 256 <= 0x7e)
    s.add((args[i] >> 16) % 256 <= 0x7e)
    s.add((args[i] >> 24) % 256 <= 0x7e)

for i in range(1, 15):
    mem = [0]*12
    mem[0]  = args[i-1]
    mem[1]  = mem[0] ^ args[i%14]
    mem[2]  = mem[1] ^ args[(i+1)%14]
    mem[3]  = mem[2] ^ args[(i+2)%14]
    mem[4]  = mem[0] + mem[1] + mem[2] + mem[3]
    mem[5]  = mem[0] - mem[1] + mem[2] - mem[3]    
    mem[6]  = mem[0] + mem[1] - mem[2] - mem[3]
    mem[7]  = mem[0] - mem[1] - mem[2] + mem[3]
    mem[8]  = (mem[6] & mem[7]) ^ (mem[4] | mem[5])
    mem[9]  = (mem[7] & mem[4]) ^ (mem[5] | mem[6])
    mem[10] = (mem[4] & mem[5]) ^ (mem[6] | mem[7])
    mem[11] = (mem[5] & mem[6]) ^ (mem[7] | mem[4])

    r1 = And(mem[8] == 4127179254, mem[9] == 4126139894, mem[10] == 665780030, mem[11] == 666819390)
    r2 = And(mem[8] == 1933881070, mem[9] == 2002783966, mem[10] == 1601724370, mem[11] == 1532821474)
    r3 = And(mem[8] == 4255576062, mem[9] == 3116543486, mem[10] == 3151668710, mem[11] == 4290701286)
    r4 = And(mem[8] == 1670347938, mem[9] == 4056898606, mem[10] == 2583645294, mem[11] == 197094626)
    r5 = And(mem[8] == 2720551936, mem[9] == 1627051272, mem[10] == 1627379644, mem[11] == 2720880308)
    r6 = And(mem[8] == 2307981054, mem[9] == 3415533530, mem[10] == 3281895882, mem[11] == 2174343406)
    r7 = And(mem[8] == 2673307092, mem[9] == 251771212, mem[10] == 251771212, mem[11] == 2673307092)
    r8 = And(mem[8] == 4139379682, mem[9] == 3602496994, mem[10] == 3606265306, mem[11] == 4143147994)
    r9 = And(mem[8] == 4192373742, mem[9] == 4088827598, mem[10] == 3015552726, mem[11] == 3119098870)
    r10 = And(mem[8] == 530288564, mem[9] == 530288564, mem[10] == 3917315412, mem[11] == 3917315412)
    r11 = And(mem[8] == 4025255646, mem[9] == 2813168974, mem[10] == 614968622, mem[11] == 1827055294)
    r12 = And(mem[8] == 3747612986, mem[9] == 1340672294, mem[10] == 1301225350, mem[11] == 3708166042)
    r13 = And(mem[8] == 3098492862, mem[9] == 3064954302, mem[10] == 3086875838, mem[11] == 3120414398)
    r14 = And(mem[8] == 2130820044, mem[9] == 2115580844, mem[10] == 2130523044, mem[11] == 2145762244)

    s.add(Or(r1, r2, r3, r4, r5, r6, r7, r8, r9, r10, r11, r12, r13, r14))

s_count = 0
s.add(args[0] == u32(b"zer0"))
s.add(args[1] == u32(b"pts{"))


while s_count < 4 and s.check() == sat:
    model = s.model()
    args_sol = [model[args[i]].as_long() for i in range(14)]

    print(''.join([p32(a).decode("utf-8") for a in args_sol]))

    cond = True
    for i in range(0, 14):
        cond = And(cond, args[i] == args_sol[i])

    s.add(Not(cond))
    s_count += 1

print("Done")
