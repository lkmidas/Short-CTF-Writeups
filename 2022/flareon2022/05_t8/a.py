from malduck import *
from pwn import *
from base64 import b64decode, b64encode

context.arch = "i386"

def to_wstr(s):
    wstr = ""
    for i in range(len(s)):
        wstr += s[i]
        wstr += "\x00"
    return wstr

magic = ""
for i in range(0x7fff):
    magic = "FO9" + str(i)
    key = to_wstr(md5(to_wstr(magic).encode("utf-8")).hex()).encode("utf-8")
    sent = b64encode(rc4(key, to_wstr("ahoy").encode("utf-8")))
    if sent == b"ydN8BXq16RE=":
        print(hex(i), sent)
        break
