from malduck import *

rc4_key = b"https://www.youtube.com/watch?v=dQw4w9WgXcQ"
cipher = unhex("7188bb1563e5702342e22a856ad3df1cfa9729b4115d8cfb1f07a0c6fc916477f02f77d656834379b32e")
plain = rc4(rc4_key, cipher)
print(plain)

xor_key = unhex("0000005F00000000501B2B4401477E285F5C3B7E010400566B0B030600124347004007445C415A530000")
plain = xor(xor_key, plain)
print(plain)
