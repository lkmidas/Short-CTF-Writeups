from malduck import *
import os

key = b"A secret is no longer a secret once someone knows it"

#data = open("./Documents_broken/.daiquiris.txt.broken", "rb").read()
#data = open("/home/midas/Documents/test.txt.broken", "rb").read()

def RC4_mod(data, key):
    S = list(range(256))
    j = 0
    out = b""
    #KSA Phase
    for i in range(256):
        j = (j + S[i] + key[i % len(key)] ) % 256
        S[i] , S[j] = S[j] , S[i]

    #PRGA Phase
    i = j = 0
    x = 0
    for b in data:
        i = ( i + 1 ) % 256
        j = ( j + S[i] ) % 256
        S[i] , S[j] = S[j] , S[i]
        rnd = S[(S[i] + S[j]) % 256]
        out += p8(b ^ (rnd ^ x))
        x = rnd
    return out

rootdir = "Documents_broken"
for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        path = os.path.join(subdir, file)
        data = open(path, "rb").read()
        dec_data = RC4_mod(data, key)
        open(os.path.join("Documents", file[:-7]), "wb").write(dec_data.strip(b"\x00"))
        