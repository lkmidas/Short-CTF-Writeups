from malduck import *

data = bytearray(unhex(open("screenshot_enc.hex", "r").read().replace("\n", "")))

for i in range(len(data) - 2, -1, -1):
    data[i] = data[i] ^ data[i+1]

open("screenshot.jpg", "wb").write(data)
