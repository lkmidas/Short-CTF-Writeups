# TETCTF2020: CALCCONV (pwn)  

- Given files: `CalcConv`.  
- The binary has: `Full RELRO`, `No canary found`, `NX enabled` and `PIE enabled`.  

## Functionalities  

- This program is where you can pass in commands in the form of `(<command>)` to choose between three functionalities: calculator, converter or setting.
- All the commands and outputs of this program is stored in a log file, which by default is `/tmp/debug.txt`.
- The program uses a self-calculated `canary` instead of a normal one.
- To use the program, first, you pass in a command in the form of `(<command>)` and then an expression for the corresponding command.
- In `calculator`, you can pass in a mathematical expression consists of 2 operands and 1 operator in +, -, *, /, %.
- In `convertor`, you can pass in a number followed by a currency unit.
- In `setting`, you can pass in a file name to change the path to the log file.

## Vulnearabilities  

**(1)** Unintended by the author: the canary is calculated using the address of the buffer containing `/dev/urandom` values instead of the values themselves, so we can calculate the canary if we can leak the stack address.

**(2)** We can use `setting` to set the log file to `/proc/self/fd/1` to display all the log on `stdout` (locally, `/dev/stdout` and `/dev/pts/0` work too, while on the server, only `/proc/self/fd/1` works, idk why).  This will get us a leakage on .text address and stack address.
  
**(3)** In the `get_input()` function, if the last byte is not `\n`, no null byte will be inserted. This is useful for leaking.

**(4)** In the `print_debug()` function, the buffer for the debug message is actually smaller than most of the debug messages' maximum size, this leads to a stack BOF.
  
## Exploit plan  
  
**Step 1:** Use `(setting)` to change the log file to `/proc/self/fd/1`.
  
**Step 2:** Leaking canary, there are 2 ways. The unintended way is to leak a stack address using the debug message and calculate it. The intended way is that the `command` in the `main_process()` function is right next to the canary, so if we can brute force a `)` character in the old RBP right after the canary (to make the program not crash at `strchr()`), then we can leak the canary in the debug message.
  
**Step 3:** Use `(calculator)`, leak .text address and stack address along the way, pass in a long expression without `\n` that concatenates with a libc address on the stack to leak libc.
  
**Step 4:**  Use `calculator()` again, this time pass in a command that contains `calculator()` and also a valid stack that can pass the canary check and then return to `one_gadget`, because we will pivot the stack to bss later.

**Step 5:** Because of the overflow in `print_debug()`, if we pass in an expression with size of 0x80, `remainder` will overwrite `canary`, `result` will overwrite old RBP. We pass in an expression so that the `canary` is the one that we leaked/calculated and the old RBP is on bss, where we set up the fake stack.

**Step 6:** From `print_debug()`, the program will return 2 times, so RSP will be pivotted into bss. Then, it will return to `one_gadget` and we get a shell.
  
 **Note 1:** The libc version is libc-2.27, which is not shown. But we can check by returning to `puts@PLT` instead of `one_gadget` and print out a libc address, then check with `libc-database`.
 
 **Note 2:** The call to `print_debug()` in `main()` can overflow more and is easier to manipulate, but it can't be use because the program only returns 1 time after that call, so we can't pivot the stack. Overwriting the return address with `one_gadget` also doesn't meet the constraints.
## Full exploit  

See `solve.py`.  
  

