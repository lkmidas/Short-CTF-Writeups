from z3 import *

s = Solver()
v = [0] * 10
x = [0] * 10

for i in range(10):
    v[i] = Int("v_{}".format(i))
    s.add(And(v[i] >= 0, v[i] <= 9))


for i in range(10):
    for j in range(10):
        x[i] += If(v[j] == i, 1, 0)

for i in range(10):
    s.add(x[i] == v[i])

if s.check():
    model = s.model()
    result = [model[v[i]].as_long() for i in range(10)]
    print(result)
