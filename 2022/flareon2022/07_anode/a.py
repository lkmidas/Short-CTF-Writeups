from z3 import *

exps = open("exps.txt", "r").read().split("\n")

lines = []
vars = set()
target = [106, 196, 106, 178, 174, 102, 31, 91, 66, 255, 86, 196, 74, 139, 219, 166, 106, 4, 211, 68, 227, 72, 156, 38, 239, 153, 223, 225, 73, 171, 51, 4, 234, 50, 207, 82, 18, 111, 180, 212, 81, 189, 73, 76]

for i in range(len(exps) - 1, -1, -1):
    lines += [exps[i]]

    if "&= 0xFF" in exps[i]:
        continue

    if len(lines) > 50 or i == 0:
        v = []
        b = [0] * 44
        s = Solver()
        for i in range(44):
            v += [BitVec("v_{}".format(i), 8)]

        for i in range(44):
            b[i] = v[i]

        for l in lines[::-1]:
            exec(l)

        for i in range(44):
            s.add(b[i] == target[i])

        sol_count = 0
        solutions = []

        #print("Checking")

        while sol_count < 5 and s.check() == sat:
            model = s.model()
            result = [model[v[i]].as_long() for i in range(44)]
            print(''.join([chr(x) for x in result]))
            solutions.append(result)
            sol_count += 1

            #print("sol_count=", sol_count)

            cond = True
            for i in range(44):
                cond = And(cond, v[i] == result[i])

            s.add(Not(cond))

        target = result
        vars = set()
        lines = []
