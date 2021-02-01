from pwn import *

r = process("./supervisor", env={"LD_PRELOAD":"./ptrace_hook.so"}, aslr=False)

r.interactive()
