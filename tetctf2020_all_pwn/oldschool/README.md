
# TETCTF2020: OLDSCHOOL (pwn)
- Given files: `oldschool`, `libc-2.23.so`.
- The binary has: `Full RELRO`, `Canary found`, `NX enabled` and `PIE enabled`.
- This is an old-school libc 2.23 heap challenge.
## Functionalities
- This program is a simple note that will store data on the heap. It has 4 functionalities: `create` a note, `edit` a note, `show` a note and `delete` a note.
- In `create`, it will first `malloc()` a 0x10 byte chunk, then read in an integer as the size of the note, this small chunk will store the metadata of a note, which is the pointer to the content chunk, the size,  and the note's state (more on this later). Another `malloc()` will be called with the size the user chose to allocate the content chunk. The content itself will be read in afterwards. You can only have at most 10 notes at a time.
- In `edit`, if the note's state is 1 and the index is valid, it will call `realloc()` on the content pointer and the size, and then read in new content, then decrement the state. If the state is not 1, it will do nothing. This means that you can only edit a note once.
- In `show`, if the note's state is 1 and the index is valid, the name, size and state of the note will be displayed. This means that you can only show an unedited note.
- In `delete`, if the index is valid, the content chunk and the metadata chunk will be freed in that order. The pointers are also set to NULL.
## Vulnearabilities
**(1)** In the `read_input()` function, if the last byte is not `\n`, no null byte will be inserted. This leads to a leakage on uninitialized data.

**(2)** After creating, the content of a chunk is not cleared. This will lead to a leakage on a `fd` heap pointer in a fast chunk and a `main_arena` libc pointer in an unsorted chunk.

**(3)** The final subtle but critical vulnearability is based on how `malloc()` and `realloc()` works on size = 0:  `malloc()` returns a chunk in the 0x21 fastbin; while `realloc()` is exactly the same as `free()` when the pointer is valid and size = 0. This leads to a double free by using both the `edit` and `delete` functionalitites.

## Exploit plan

**Step 1:** Leak the heap address with vulnearabilities **(1)** and **(2)** using 2 consecutive fast chunks.

**Step 2:** Leak libc address using an unsorted chunk and a fast chunk (to prevent consolidate with top).

**Step 3:** Create a note of size 0, edit it and then delete it to achieve a double free. The double freed chunk will be in the 0x21 fastbin, which can't be used to overwrite `__malloc_hook` yet.

**Step 4:** Use that chunk to overwrite the content pointer of a note to a 0x71 fastbin chunk and its size to 0, use the same method to double free this chunk.

**Step 5:** Use this new double freed chunk to overwrite `__malloc_hook` with `one_gadget`.

**Step 6:** Make a call to `malloc()` and get shell.

## Full exploit
See `solve.py`.

