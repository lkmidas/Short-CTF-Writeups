# ASCIS2020 QUALS: CRYPT (RE)
- Given files: `Crypt`, `encrypted.bin`.
- The `Crypt` file is an ELF 64-bit executable compiled from C++ which takes 2 command line arguments: a key and a file name. It will check if the key is correct and then use it to somehow encrypt the file and generate `encrypted.bin`.
- The given `encrypted.bin` is the encrypted flag file, we have to reverse engineer the ELF file to find a way to decrypt this.
## Analysis

### Step 1: Static analysis: deobfuscating (IDA Pro)
First off, I started to analyze the file statically. The first thing that happened when I threw the program into IDA is that there were a bunch of errors about PLT. Skipping all those errors and looking into the file, it's obvious that all the library calls through PLT are obfuscated. The obfuscation scheme is not that difficult: the program has a table of all the pointers to the library functions (the same as GOT), and when it calls a library function, it makes some calls to some functions that literally get an offset from the start of that table to the desired function pointer. Therefore, it's not that hard to statically renamed all of the obfuscated library calls.

### Step 2: Retrieving the key (IDA Pro + GDB)
The comparison happens in the if statement using only 1 function `sub_45AE`, so using ANGR to try to solve the key is not a viable strategy (I did try it and failed horribly). Looking back up, I saw that three C++ strings were constructed, one from our input key, and two from the global variables `unk_9A80` and `unk_9AA0`. The values of these two variables are initialized somewhere in the initialization of the process and can be found by cross-referencing them, but they are really not that important because I decided to do this part dynamically anyway.

So, looking more carefully, our key and `unk_9AA0` go through a function `sub_411A`, by debugging, it's easy to recognize that this function simply mirror the string. The other variable `unk_9A80` in the other hand, goes through a series of function and then gets passed in to a final function `sub_47CC` together with our mirrored input key. 

About that "series of functions", I didn't even reverse them statically and just found the resulting string by debugging, it was `3669372743793841`.

About `sub_47CC`, it literally is just an addition function on two strings that represent large integers, where the leftmost digit being the least significant digit (that is why our strings are mirrored). The value of `unk_9AA0` after mirroring is `2333602996074364`. So in the end, all the key checking part does is to check if our input key satisfies this equation: `1483973472739663 + key == 4634706992063332`. Therefore, the key can be found very easily: `3150733519323669`.

### Step 3: Decrypt the encrypted file (IDA Pro + PyCrypto)
After the key comparison is a bunch of C++ allocators and strings garbage that I simply just ignored. The important encryption function is under the for loop, function `sub_34C8`. Digging deep into this function, it is quite a complicated cryptographic function, so I looked for constants to find out if it is any of the popular crypto. I found an interesting array of constants `byte_9020`, which after some quick googling, I knew that this is called the `AES Sbox`. So this is for sure an AES encryption, the problem then was to know which AES mode it is, and what is the AES key.

About the key, it was just the matter of debugging with GDB again and dumping it out, which was ``P4nd`p<c8gE;T$F8``.

About the mode, I tried to create a file contains all character `a`, and encrypted it with the program. The result is that the encrypted file contains a bunch of the same blocks. I asked my team crypto player `@pcback` which mode of AES it is that makes the same cipher blocks for the same plain content, and he said it is **AES ECB**. With all the information, I just wrote a quick python script to decrypt the given encrypted file, which turns out to be a PNG image of the flag. The script is as follow:
```
import base64
from Crypto.Cipher import AES
from Crypto import Random


key = b"P4nd`p<c8gE;T$F8"
encrypt = open("./encrypted.bin", "rb").read()
cipher = AES.new(key, AES.MODE_ECB)
open("out.png","wb").write(cipher.decrypt(encrypt))
```
The flag is `ASCIS{C4yp1o_1s_5impl3_b4t_C++_i5_cr4z9}`.
