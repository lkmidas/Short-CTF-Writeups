from ctypes import (windll, wintypes, c_uint64, cast, POINTER, Union, c_ubyte,
                    LittleEndianStructure, byref, c_size_t)
import zlib


# types and flags
DELTA_FLAG_TYPE             = c_uint64
DELTA_FLAG_NONE             = 0x00000000
DELTA_APPLY_FLAG_ALLOW_PA19 = 0x00000001


# structures
class DELTA_INPUT(LittleEndianStructure):
    class U1(Union):
        _fields_ = [('lpcStart', wintypes.LPVOID),
                    ('lpStart', wintypes.LPVOID)]
    _anonymous_ = ('u1',)
    _fields_ = [('u1', U1),
                ('uSize', c_size_t),
                ('Editable', wintypes.BOOL)]


class DELTA_OUTPUT(LittleEndianStructure):
    _fields_ = [('lpStart', wintypes.LPVOID),
                ('uSize', c_size_t)]


# functions
ApplyDeltaB = windll.msdelta.ApplyDeltaB
ApplyDeltaB.argtypes = [DELTA_FLAG_TYPE, DELTA_INPUT, DELTA_INPUT,
                        POINTER(DELTA_OUTPUT)]
ApplyDeltaB.rettype = wintypes.BOOL
DeltaFree = windll.msdelta.DeltaFree
DeltaFree.argtypes = [wintypes.LPVOID]
DeltaFree.rettype = wintypes.BOOL


def apply_patchfile_to_buffer(buf, buflen, patchpath, legacy):
    with open(patchpath, 'rb') as patch:
        patch_contents = patch.read()

    # some patches (Windows Update MSU) come with a CRC32 prepended to the file
    # if the file doesn't start with the signature (PA) then check it
    if patch_contents[:2] != b"PA":
        paoff = patch_contents.find(b"PA")
        if paoff != 4:
            raise Exception("Patch is invalid")
        crc = int.from_bytes(patch_contents[:4], 'little')
        patch_contents = patch_contents[4:]
        if zlib.crc32(patch_contents) != crc:
            raise Exception("CRC32 check failed. Patch corrupted or invalid")

    applyflags = DELTA_APPLY_FLAG_ALLOW_PA19 if legacy else DELTA_FLAG_NONE

    dd = DELTA_INPUT()
    ds = DELTA_INPUT()
    dout = DELTA_OUTPUT()

    ds.lpcStart = buf
    ds.uSize = buflen
    ds.Editable = False

    dd.lpcStart = cast(patch_contents, wintypes.LPVOID)
    dd.uSize = len(patch_contents)
    dd.Editable = False

    status = ApplyDeltaB(applyflags, ds, dd, byref(dout))
    if status == 0:
        raise Exception("Patch {} failed".format(patchpath))

    return (dout.lpStart, dout.uSize)


from malduck import *
import os

for subdir, dirs, files in os.walk(".\\2\\patches"):
    print(files)
    for i in range(len(files)):
        with open("./1.png", 'rb') as r:
            inbuf = r.read()
        buf = cast(inbuf, wintypes.LPVOID)
        n = len(inbuf)
        to_free = []

        f = files[i]
        path = os.path.join(subdir, f)
        print(path)
        try:
            buf, n = apply_patchfile_to_buffer(buf, n, path, False)
            to_free.append(buf)
            
            outbuf = xor(b"meoow", bytes((c_ubyte*n).from_address(buf)))
            
            with open(".\\2\\decoded\\" + f + ".txt", 'wb') as w:
                w.write(outbuf)
            for buf in to_free:
                DeltaFree(buf)
        except:
            pass
