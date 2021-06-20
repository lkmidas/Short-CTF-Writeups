from z3 import *

def func(p1, p2):
    return p1 / p2

s = Solver()
x = [Int("x%d"%i) for i in range(8)]

for i in range(8):
    s.add(And(x[i] > 0, x[i] < 26))

#for i in range(8):
#    for j in range(i+1, 8):
#        s.add(x[i] != x[j])

s.add(x[0] + x[1] + x[2] + x[3] + x[4] + x[5] + x[6] + x[7] == 0x66)
s.add(x[0] * x[1] == 0x10)
s.add(func(x[6], x[5]) == 4)
s.add(x[3] + x[2] == 0x1a)
s.add(x[4] - x[5] == 0x11)
s.add(func(x[1], x[0]) == 0x10)
s.add(func(x[2], x[5]) == 5)
s.add(x[3] + x[4] == 0x1b)

sol_count = 0
solutions = []

print("Checking")

while sol_count < 80 and s.check() == sat:
    model = s.model()
    x_sol = [model[x[i]] for i in range(8)]
    print(x_sol)

    solutions.append(x_sol)
    sol_count += 1

    print("sol_count=", sol_count)

    cond = True
    for i in range(8):
        cond = And(cond, x[i] == x_sol[i])

    s.add(Not(cond))

