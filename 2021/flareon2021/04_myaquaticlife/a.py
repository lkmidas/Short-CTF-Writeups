from malduck import *
import itertools

desired_hash = b"6c5215b12a10e936f8de1e42083ba184"

base_hash = unhex("9625A4A9A3969A909FAFE538F9819E16F9CBE4A4878F8FBAD29DA7D1FCA3A8")

creatures_774 = [b"newaui", b"HwdwAZ", b"SLdkv"]
creatures_77C = [b"DFWEyEW", b"PXopvM", b"BGgsuhn"]

for perm_x in list(itertools.permutations(creatures_774)):
    for perm_y in list(itertools.permutations(creatures_77C)):
        x = b"".join(perm_x)
        y = b"".join(perm_y)
        resulting_hash = b""
        for i in range(len(base_hash)):
            resulting_hash += p8(((base_hash[i] ^ y[i % len(y)]) - x[i % 17]) & 0xff)
        if enhex(md5(resulting_hash)) == desired_hash:
            print(perm_x, perm_y)
