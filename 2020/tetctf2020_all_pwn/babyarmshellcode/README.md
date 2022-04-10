# TETCTF2020: BABY_ARM_SHELLCODE (pwn)  

- Given files: `babyshellcode`.  
- This binary is for `arm-32-little` and runs on a Ubuntu 18.04 system.
- The binary has: `Full RELRO`, `No canary found`, `NX enabled` and `PIE enabled`.  
- This is a very unique pwn + shellcode + linux system challenge.

## Functionalities  

- The program first `mmap()` a RWX region and then reads in 0x1000 bytes of input.
- It then prints out the higher 2 bytes of the mmapped region's address.
- After that, it `mmap()` another RWX region and then copies the built-in shellcode to the region, which will clear all the registers, then reads in another 0x48 bytes of input.
- After reading our shellcode, all the file descriptors `stdin`, `stdout` and `stderr` are closed.
- A seccomp rule is then defined, which will block all calls to syscall number -10181, 192 and 125, which are `__PNR_mmap`, `mmap2` and `mprotect`.
- Finally, the shellcode in the second region will be executed.

## Vulnearabilities  

**(1)** The 0x48 bytes of shellcode in the second region is too short, so we have to find a way to execute the 0x1000 bytes of shellcode in the other region. The intended way to do this is to write a specific piece of shellcode called the `egg hunter` to hunt for the first page and jump to it. Here, because the leak was 2 higher bytes of the address, we actually can bruteforce 4 bits of address to jump into the correct page.

**(2)** All file descriptors are closed, so we will have to make a call to `connect()` in our shellcode to backconnect to our server.
  
**(3)** All the `mmap()` and `mprotect()` syscalls are blocked, so we can't run anymore process other than our current one. This means we can't `execve()` any file, in other words, we can only interact with everything through our shellcode.

**(4)** Using the shellcode to investigate more about the server, we will find more interesting things.
  
## Exploit plan  
  
**Step 1:** In the second page, we used a `mov` and a `bx` instruction to bruteforce the first page address and jump to it (again, the better way is to use `egg hunter`).
  
**Step 2:** In the second page, we make a call to `connect()` to backconnect to our server.
  
**Step 3:** Then we make a call to `open()`, `read()` and `write()`, to read files and send output to our server. Reading the `/flag` file shows that we don't have the permission to read it. (File-reading shellcode can be found in `read_file.py`.)
  
**Step 4:**  Changing the shellcode to `open()` a directory and `getdents()` to list all the files in the opened directory and investigate around the server, we found another user `babyfmt` that has its own directory, its own binary and its own flag, it also shows that `/flag` is just a symbolic link. (Dir-listing shellcode can be found in `dir_list.py`.)

**Step 5:** Changing the shellcode to `getlink()` on `/flag`, we know that it is a symlink to `/home/babyfmt/flag`. So this means we somehow have to gain `babyfmt` privilege to read this file.

**Step 6:** Using the file-reading code again, we can dump the `babyfmt` binary.
  
**Step 7:** The suspection now is that the server run another service for `babyfmt` and we can get the flag through that service. Port scanning result in another opened port: 8888. (`babyshellcode` is at port 9999.)

**Step 8:** Connecting to port 8888 from our machine doesn't work. The suspection now is that the port is only opened locally, so we have to make another call to `connect()` in our shellcode to `localhost` at port `8888`, and it works this time. This means that we have to exploit the `babyfmt` file through our shellcode to get the flag. (Although the final hint shows that checking the files in `/etc/xinetd.d/` is a better way to get all these informations.)
## About BABYFMT
- The binary has: `Full RELRO`, `No canary found`, `NX enabled` and `PIE enabled`.  
- It is a very simple program, first, it reads the flag and stores it in bss, then it goes into an infinite loop that reads our input and passes it directly to the fmt parameter of `printf()`, resulting in an infinite format string bug.
- We can exploit this by using the format `%34$x` to leak an address of .text (the number 34 is achieved by bruteforce dumping the stack), then we can calculate the flag's address and use the format `%s` to print out the flag.
- The challenging part here is that we have no pwntools to help us simplify this exploit, since everything has to be done through shellcode. My teammate `@pickaxe` coded this fabulous ARM assembly code to do all the calculating to get the flag.
## Full exploit  

See `solve.py` (`@pickaxe`'s code).  
  

