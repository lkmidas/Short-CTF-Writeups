# SECCON2018: PROFILE (pwn)
## First look
- Given files: `profile`, `libc-2.23.so`.
- This is a ordinary ret2libc on a C++ binary.
## Vulnearability
**(0)** No PIE.

**(1)** `malloc_usable_size()` is used on a C++ string in `Profile::update_msg()`, which will behave incorrectly (return a huge number) if the string's length is < 8 and placed on the stack, overflowing the string's buffer on the stack.

**(2)** The message is placed preceded to the name in `Profile`, so we can overwrite name when overflowing message.
## Exploit plan
**Step 1:** Enter a name of length 8, a random age, and a message of length < 8 (to make use of (1)).

**Step 2:** Update the message and overwrite the least significant byte of name and bruteforce it several times to leak the canary.

**Step 3:** Update the message again to overwrite the name to GOT and leak libc address.

**Step 4:** Update the message again to overwrite ret, also need to overwrite name to NULL to prevent the string destructor from crashing.

**Step 5:** Exit to get shell.
## Full exploit
See `solve.py`.
