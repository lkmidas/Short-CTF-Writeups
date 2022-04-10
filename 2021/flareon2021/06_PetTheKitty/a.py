from malduck import *

data = open("2.bin", "rb").read()
packets = data.split(b"PA30")[1:]

for i in range(len(packets)):
    p = b"PA30" + packets[i].split(b"ME0W")[0]
    if i % 2 == 0:
        name = str(i) + "_client"
    else:
        name = str(i) + "_server"
    open("./2/patches/" + name, "wb").write(p)
