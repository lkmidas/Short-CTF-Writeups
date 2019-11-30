# SVATTT2019FINAL: THREE_O_THREE (pwn)
## First look
- Given files: `three_o_three`, `libc.so.6`.
- Given libc's version is 2.27.
- This is a puzzle-ish pwn challenge, an upgraded version of HITCON2019 `trick-or-treat` challenge.
## Analysis
**(1)** The first `malloc()`'s size is arbitrary, the created chunk (magic)'s address is printed out.

**(2)** We have 3 arbitrary 8-byte writes at an arbitrary offset to magic.

**(3)** `scanf()`'s format string is `%lu`, which is different from `trick-or-treat`.

**(4)** Overwriting `__free_hook` with `one_gadget` does not work on remote server.

## Exploit plan
**Step 1:** Pass a very large size to `malloc()`, which will cause it to call `mmap()` and return a magic chunk at a page right above libc. Its address will be printed out, so we have full control over libc.

**Step 2:** Use the 1st write to overwrite `__free_hook` to `exit()`, again, `one_gadget` does not work.

**Step 3:** Use the 2nd write to overwrite the pointer to `rtld_lock_default_unlock_recursive()` in `_rtld_global` (which is in the `ld` page right after libc) to `one_gadget`. This function will be called in `_dl_fini()`, which is called in `exit()`.

**Step 4:** Use the 3rd write to pass a very long string to `scanf()`, which will cause it to call `free() -> exit() -> _dl_fini -> rtld_lock_default_unlock_recursive() -> one_gadget`. Only this method of calling `one_gadget` works remotely.

## Full exploit
See `solve.py`.
