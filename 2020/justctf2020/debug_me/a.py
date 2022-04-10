from malduck import unhex
ARR = list(bytearray(unhex(b"1B59294C3D6F227F261C2C2F074E171E610A531034654A4258081D603355374452392E720F6E7E3F32475A1319067A51181A634802773E543516045E4F49300315714D113812054527683A750920014069236A3B415F7B573C1F66565C0C36732D67435D4B2876787D316D2514745B6B0D5070640E622B0B462A7C796C2421")))

def get_key(n):
    key = ""
    while (n != 0):
        if n & 1:
            key += "0"
            n = (n - 1) // 2
        else:
            key += "1"
            n = (n - 2) // 2
    return key[::-1]

secret_key = ""
for i in range(1, 128):
    x = ARR.index(i)
    secret_key += get_key(x) + '?'

secret_key += "\n"
open("./secret_key", "w").write(secret_key)
