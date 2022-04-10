from malduck import unhex
from z3 import *

maze = list(unhex("00010001000101010000010101000101000101000001000100010100000100000100000001000001000001010001010001010000010000000101000001010000000100010000010100000101010001000100000100010100010000010101010001000001000101000001000100000101000101000101000000010001010001000001000101000100010000010001010001010000010100000100000100010100010100000001000100000101010001000101000001010000000100010100010001010000010000010001010000010001010001000101000001000001000101000100000100000101010001000100000100010100010000010000010101000100"))
CNT = 35

X = IntVector('X', CNT)
Y = IntVector('Y', CNT)

s = Solver()

MAZE = Array('MAZE', IntSort(), IntSort())
i = 0
for elem in maze:
    MAZE = Store(MAZE, i, elem)
    i = i + 1

# Coordinates condition
for i in range(CNT):
    s.add(And(X[i] >= 0, X[i] < 8))
    s.add(And(Y[i] >= 0, Y[i] < 8))

# Don't go back condition
for i in range(2, CNT):
    s.add(If(X[i] == X[i-2], Y[i] != Y[i-2], True))
    s.add(If(Y[i] == Y[i-2], X[i] != X[i-2], True))

# Initial coordinate condition
s.add(And(X[0] == 3, Y[0] == 0))

# Valid moves condition
for i in range(1, CNT):
    cond1 = If(Select(MAZE, 4 * (X[i-1] + 8 * Y[i-1]) + 2) == 1, And(X[i] == X[i-1] - 1, Y[i] == Y[i-1]), False)
    cond2 = If(Select(MAZE, 4 * (X[i-1] + 8 * Y[i-1]) + 3) == 1, And(X[i] == X[i-1] + 1, Y[i] == Y[i-1]), False)
    cond3 = If(Select(MAZE, 4 * (X[i-1] + 8 * Y[i-1]) + 0) == 1, And(X[i] == X[i-1], Y[i] == Y[i-1] - 1), False)
    cond4 = If(Select(MAZE, 4 * (X[i-1] + 8 * Y[i-1]) + 1) == 1, And(X[i] == X[i-1], Y[i] == Y[i-1] + 1), False)
    s.add(Or(cond1, cond2, cond3, cond4))

# Final coordinate condition
s.add(And(X[34] == 4, Y[34] == 7))

if s.check() == sat:
    model = s.model()
    
    X_res = [model[X[i]].as_long() for i in range(CNT)]
    Y_res = [model[Y[i]].as_long() for i in range(CNT)]
    path = ""
    for i in range(1, CNT):
        if X_res[i] == X_res[i-1] - 1:
            path += "L"
        elif X_res[i] == X_res[i-1] + 1:
            path += "R"
        elif Y_res[i] == Y_res[i-1] - 1:
            path += "U"
        elif Y_res[i] == Y_res[i-1] + 1:
            path += "D"

    print(path)
    
else:
    print("unsat")



    