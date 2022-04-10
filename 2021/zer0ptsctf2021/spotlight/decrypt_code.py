from malduck import *


def _d(start, end, key):
    lo = key & 0xffffffff
    hi = key >> 32
    x = end - start
    while end >= start + 4:
        x = hi + lo * x
        enc = u32(ida_bytes.get_bytes(start, 4))
        ida_bytes.patch_bytes(start, p32(enc ^ x))
        start += 1


def decrypt(ea, key):
    start = 0
    end = 0
    while True:
        mark = ida_bytes.get_bytes(ea, 4)
        if mark == b"\xAB\xAD\xF0\x0D":
            start = ea
            break
        ea += 1
    ida_bytes.patch_bytes(ea, b"\x90\x90\x90\x90")

    while True:
        mark = ida_bytes.get_bytes(ea, 4)
        if mark == b"\x0D\xF0\xAD\xAB":
            end = ea
            break
        ea += 1
    ida_bytes.patch_bytes(ea, b"\x90\x90\x90\x90")
    print(hex(start), hex(end), hex(key))
    _d(start + 4, end, key)

