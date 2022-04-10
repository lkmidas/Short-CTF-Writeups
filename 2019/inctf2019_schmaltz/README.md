# INCTF2019: SCHMALTZ (pwn)
## First look
- Given files: `schmaltz`, `libc.so.6`, `ld-2.28.so`.
- Given libc is a customized libc version 2.29.
- This is a heap challenge.
## Bugs
**(1)** Double free in remove function (useless due to libc 2.29).

**(2)** Off-by-one note can be created/viewed (useless).

**(3)** Uninitialized chunk's data when created (exploitable).

**(4)** Incorrect null-byte handling in get_inp() (exploitable).

**(5)** Custom libc cannot invoke `/bin/sh` (makes your life harder).

## Exploit plan
**Step 1:** Leak heap address thanks to (3).

**Step 2:** Fill up a tcache bin, also set up a fake big unsorted chunk.

**Step 3:** Use (4) to clear the inused bit of an unsorted chunk an consolidate it with the one created in step 2.

**Step 4:** Leak libc address from the chunk in step 3 thanks to (3).

**Step 5:** Use the chunk in step 3 to corrupt tcache and set `environ` to NULL to deal with (5).

**Step 6:** Repeat step 5 to set `__free_hook` to `system()`.

**Step 7:** Free a chunk with `/bin/sh`, get shell.
## Full exploit
See `solve.py` (well-commented).
