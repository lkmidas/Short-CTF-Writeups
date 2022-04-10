f = open("rules.txt", "r")
lines = f.readlines()
splits = [0]*300

for l in lines:
    splits[int(l[:4])] = l.split("  ")[1]

for i in range(104, 118):
    #s = splits[i]
    rule = ""
    #rule += "mem[8] == {}, ".format(int(s.split(" == ")[1][:-1]))
    j = i
    x = 8
    while x != 12:
        s = splits[j]
        rule += "mem[{}] == {}, ".format(x, int(s.split(" == ")[1].split(")")[0]))
        j = int(s.split(" ")[5]) + 1
        x += 1
    print(rule)

