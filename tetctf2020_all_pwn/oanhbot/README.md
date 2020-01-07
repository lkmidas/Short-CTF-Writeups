
# TETCTF2020: OANHBOT (pwn)
- Given files: `oanhbot`, `libc-2.23.so`.
- The binary has: `Partial RELRO`, `Canary found`, `NX enabled` and `No PIE`.
## Functionalities
- In this program, you will name your hero and choose an enemy to fight with and decide who wins.
- Firstly, the program reads 0x10 bytes of input as your hero's name.
- Secondly, you can choose one of the pre-defined name for your enemy, or name it yourself with another 0x10 bytes of input.
- Then, the program will go into a loop that continuously reducing your and your enemy's HP based on your and your enemy's damage. The problem is, all the HPs and damages are hard-coded in a way that you will always lose!
- But if somehow you win, you can say `Y` and then pass in 0x90 bytes of input as a `status`.
## Vulnearabilities
**(1)** In the `read_input()` function, there is a off-by-one null byte overflow if you read in the maximum number of bytes.

**(2)** The characters' `damage` is stored right next to their `name` in the struct, so the null byte overflow will lead to an overflow into the damage.

**(3)** Your `status`, after being read, will be passed directly as a `fmt` parameters for `snprintf`, leads to a format string bug.

## Exploit plan

**Step 1:** Send in any name for your hero, and then a 0x10 byte-long name for the enemy, this will lead to a null byte overflow and set your enemy's damage from `0x1F0` to `0x100`.

**Step 2:** We will win the battle using step 1, choose `Y` to pass in a status, the next step is to exploit the format string bug in the status. Calculate the offset to `main` and `system@plt` to craft the fmt payload.

**Step 3:** Craft the fmt payload in a way that it will overwrite `system@GOT` with `main` and `memset@GOT` with `system@PLT`, then send it.

**Step 4:** `system()` will be called, which is now `main()`, we are now back to main, repeat step 1 to win the battle, and then pass in `Y;sh;` so that we pass the check and get to `memset()`, which is now `system()`, to get the shell.

## Full exploit
See `solve.py`.

