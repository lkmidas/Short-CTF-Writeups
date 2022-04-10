---
title: "GoogleCTF2021 - weather writeups"
subtitle: ""
date: 2021-07-19T19:40:02+07:00
lastmod: 2021-07-19T19:40:02+07:00
draft: false
author: "Midas"
description: "Writeup for GoogleCTF2021 weather challenge"

tags: []
categories: [writeups]

hiddenFromHomePage: false
hiddenFromSearch: false

featuredImage: ""
featuredImagePreview: ""

toc:
  enable: true
math:
  enable: false
lightgallery: false
license: ""
---

<!--more-->
{{< admonition note "Note" >}}
*Use the table of contents on the right to navigate to the section that you are interested in.*
{{< /admonition >}}

## Introduction
{{< admonition info "Challenge Info" >}}
- **Given files:** [weather](weather).
- **Description:** `I heard it's raining flags somewhere, but forgot where... Thankfully there's this weather database I can use.`
- **Category:** Reverse engineering
- **Summary**: A VM reverse engineering challenge. This VM is created using custom `printf` formats. My solution is to build an emulator for it and use `z3` to solve it automatically without digging deep into the VM code.
{{< /admonition >}}

{{< admonition tip "TL;DR" >}}
1. Analyze the main function -> pretty normal, can notice some unfamiliar `printf` formats.
2. Analyze the init function -> learn that this program registers a bunch of new different `printf` formats.
3. Analyze each handler function -> learn that most of them are used to create a register based VM.
4. Write an emulator + disassembler to analyze it -> learn that the first block of VM code tries to decode a larger block of code using the first byte of our input.
5. Because this is a format string VM, the first byte of the block of code must be `%` -> find out the first correct byte of the input is `T`.
6. Use the emulator + disassembler to analyze the decrypted code block -> reach the check instruction.
7. Insert `z3` variables into the input bytes, change the emulator a bit -> let `z3` solve the correct input automatically.
8. Run the original program, pass in the correct input -> get flag
{{< /admonition >}}

## Analyzing main function
The `main` function is quite ordinary, it first reads in 100 bytes of input from the user and stores it at address `6080`. It then compares the input with some constant city names and prints the corresponding values. The interesting bit in `main` is that it uses some unfamiliar `printf` formats like `%P`, `%W`, `%T`, `%F`:
```C
printf("Precipitation: %P\n", &v7, a4);
printf("Wind: %W\n", &v10);
printf("Temperature: %T\n", &v5);
printf("Flag: %F\n", a4);
```

When we run the program, it will print using these formats just fine, it means that these formats must be registered somewhere else in the binary. The oldest trick in the book to do this is to use the ELF `init` function.

## Analyzing init function
We can see a function `sub_2328` in `.init_array`:
```C
int init_register_printf()
{
  register_printf_function('W', format_W, arginfo);
  register_printf_function('P', format_P, arginfo);
  register_printf_function('T', format_T, arginfo);
  register_printf_function('F', format_F, arginfo);
  register_printf_function('C', format_C_jcc, do_nothing);
  register_printf_function('M', format_M_load, do_nothing);
  register_printf_function('S', format_S_add, do_nothing);
  register_printf_function('O', format_O_sub, do_nothing);
  register_printf_function('X', format_X_mult, do_nothing);
  register_printf_function('V', format_V_div, do_nothing);
  register_printf_function('N', format_N_mod, do_nothing);
  register_printf_function('L', format_L_lshift, do_nothing);
  register_printf_function('R', format_R_rshift, do_nothing);
  register_printf_function('E', format_E_xor, do_nothing);
  register_printf_function('I', format_I_and, do_nothing);
  return register_printf_function('U', format_U_or, do_nothing);
}
```

This function uses `register_printf_function` to register new formats for `printf`, more about it can be found [here](https://www.gnu.org/software/libc/manual/html_node/Registering-New-Conversions.html). The most important parts are the first and second parameters to it. The first one is a single `char`, which is the new format, and the second one is the handler function for that format. So it is clear that the job now is to reverse each of them.

## Analyzing each format handler function
There are 16 new formats registered, I will explain each of them:
- `%W`, `%P` and `%T` are pretty standard, they are just wrappers around traditional `printf` formats.
- `%F` is also a wrapper around other `printf` formats, but it uses `%C`, which is a new format.
- `%C` is where it gets interesting. In this handler function we can see that instead of using the `printf`'s `args`, it uses the `info` instead.

The struct definition for `printf_info` can be found [here](https://code.woboq.org/userspace/glibc/stdio-common/printf.h.html) and it's documentation can be found [here](https://www.gnu.org/software/libc/manual/html_node/Conversion-Specifier-Options.html):
```C
struct printf_info
{
  int prec;                        /* Precision.  */
  int width;                        /* Width.  */
  wchar_t spec;                        /* Format letter.  */
  unsigned int is_long_double:1;/* L flag.  */
  unsigned int is_short:1;        /* h flag.  */
  unsigned int is_long:1;        /* l flag.  */
  unsigned int alt:1;                /* # flag.  */
  unsigned int space:1;                /* Space flag.  */
  unsigned int left:1;                /* - flag.  */
  unsigned int showsign:1;        /* + flag.  */
  unsigned int group:1;                /* ' flag.  */
  unsigned int extra:1;                /* For special use.  */
  unsigned int is_char:1;        /* hh flag.  */
  unsigned int wide:1;                /* Nonzero for wide character streams.  */
  unsigned int i18n:1;                /* I flag.  */
  unsigned int is_binary128:1;        /* Floating-point argument is ABI-compatible
                                   with IEC 60559 binary128.  */
  unsigned int __pad:3;                /* Unused so far.  */
  unsigned short int user;        /* Bits for user-installed modifiers.  */
  wchar_t pad;                        /* Padding character.  */
};
```

I will explain the fields that our binary uses:
- `width` is the width of the string to be printed with the format, for example: `%69x` results in `info->width = 69`. By default if width is not specified then it's 0.
- `prec` is the precision of a non-integer number, for example `%.69f` results in `info->prec = 69`. By default this is -1.
- `is_long_double`, `is_short`, `is_long` and `is_char` are 1-bit fields that correspond to the flags `ll`, `h`, `l`, `hh`, respectively, before the format type. Only one of these bit can be 1 at a time, for example: `%lx` sets `info->is_long` to 1 and the rest to 0.
- `left`, `showsign` are also 1-bit fields that correspond to the flags `-` and `+` at the start of the format, right after `%`. Only one of these two can be 1 at a time, for example `%+6x` or `%-9x`.
- `pad` is the padding character and can only be either whitespace (`' '`) or zero (`'0'`), default to whitespace. The first byte after `%` or `+/-` will determine this, if it's `0` then `info->pad = '0'`, for example: `%69x` is whitespace-padded and `%069` is 0-padded.

{{< admonition note "Note" >}}
*You may be unfamiliar with the `:1` after field names. This in C is used to define bit fields. For example: all 8 fields from `is_long_double` to `group` are only 1 bit in size, so they all will be stored in 1 single byte instead of 8 different bytes for memory optimization.*
{{< /admonition >}}

With the above knowledge, let's get back to the registered `printf` formats:
- `%C` is easier to understand now, it uses `left`, `showsign` and `pad` fields to determine the type of comparison. Afterwards, it uses the comparison result to decide to call another `fprintf` or not (all functions in `printf` family shares the registered format handlers). Notice that there are 2 different memory regions that are accessed here: one is 32-bit accessed in the comparison at address `70A0`, I called it `REGS`; the other is 8-bit accessed and contains other format strings at address `5080`, I called it `MEM`. So this `%C` format is basically a conditional call function that implements 4 different calls, I name them `CLZ`, `CGZ`, `CEZ` and `CALL`.
```C
__int64 __fastcall format_C_call(FILE *stream, const struct printf_info *info, const void *const *args)
{
  int prec; // [rsp+24h] [rbp-Ch]
  _BOOL4 cmp_flag; // [rsp+2Ch] [rbp-4h]

  prec = info->prec;
  if ( (*((_BYTE *)info + 12) & 0x20) != 0 )    // - flag
  {
    cmp_flag = REGISTERS[prec] < 0;
  }
  else if ( (*((_BYTE *)info + 12) & 0x40) != 0 )// + flag
  {
    cmp_flag = REGISTERS[prec] > 0;
  }
  else if ( info->pad == '0' )                  // padding char
  {
    cmp_flag = REGISTERS[prec] == 0;
  }
  else
  {
    cmp_flag = 1;
  }
  if ( cmp_flag )
    fprintf(stream, &MEM[info->width]);
  return 0LL;
}
```

- All the other formats follows the same structure, which uses `left` and `showsign` fields to get an address, and `is_long_double`, `is_short`, `is_long`, `is_char` fields to get a value. It then performs an arithmetic operation on what is at the address and the value and store the result back to address. The operations are: `%M - load`, `%S - add`, `%O - sub`, `%X - mult`, `%V - div`, `%N - mod`, `L - left shift`, `R - right shift`, `E - xor`, `I - and`, `U - or`.
```C
__int64 __fastcall format_M_load(FILE *stream, const struct printf_info *info, const void *const *args)
{
  int prec; // [rsp+24h] [rbp-14h]
  int width; // [rsp+28h] [rbp-10h]
  int val; // [rsp+2Ch] [rbp-Ch]
  char *addr; // [rsp+30h] [rbp-8h]

  width = info->width;
  prec = info->prec;
  if ( (*((_BYTE *)info + 12) & 0x20) != 0 )    // - flag
  {
    addr = &MEM[width];
  }
  else if ( (*((_BYTE *)info + 12) & 0x40) != 0 )// + flag
  {
    addr = &MEM[REGISTERS[width]];
  }
  else
  {
    addr = (char *)&REGISTERS[width];
  }
  val = 0;
  if ( (*((_BYTE *)info + 13) & 2) != 0 )       // hh flag
  {
    val = *(_DWORD *)&MEM[prec];
  }
  else if ( (*((_BYTE *)info + 12) & 2) != 0 )  // h flag
  {
    val = *(_DWORD *)&MEM[REGISTERS[prec]];
  }
  else if ( (*((_BYTE *)info + 12) & 1) != 0 )  // L flag
  {
    val = info->prec;
  }
  else if ( (*((_BYTE *)info + 12) & 4) != 0 )  // l flag
  {
    val = REGISTERS[prec];
  }
  *(_DWORD *)addr = val;
  return 0LL;
}
```

So in summary, these formats defined a VM as follow: A register-based VM that operates on a set of 32-bit registers and an 8-bit accessed memory. It has 11x3x4 arithmetic instructions and 4 call instructions. However, there is one more instruction that is not explicitly defined which is `RET`. After all, this VM operates on `printf`, and `printf` will stop printing at the end of a string. Therefore, a null byte `\x00` can be understood as a `RET` instruction. The binary will jump into this VM using the `printf` format `%F`, which then call `printf` format `%52C`, which means an unconditional `CALL` to `MEM[52]`.

## Writing an emulator + disassembler
Emulating unfamiliar instruction sets is actually one of my interest, so immediately I decided to solve this challenge using an emulator. The first step is to parse each format strings into different fields. My method is a naive one but it works in this case, the steps are:
1. Initiating all fields with there default values.
2. Get the first byte after `%`, if it's `+` then set `showsign` to 1, if it's `-` then set `left` to 1.
3. Get the next byte after that, if it's `0` then set pad to `'0'`.
4. If `hh` is in the string, set `hh` to 1, goto step 8.
5. If `h` is in the string, set `h` to 1, goto step 8.
6. If `ll` is in the string, set `L` to 1, goto step 8.
7. If `l` is in the string, set `l` to 1.
8. Get the format type as the last character of the string.
9. If `.` is in the string, goto 12.
10. From the bottom up, remove all non-digit characters.
11. What is left is `width`, end.
12. Split the string by `.`, the first half is `width` if it's not empty.
13. From the bottom up of the second half, remove all non-digit characters.
14. What is left is `prec`, end.

```python
def parse_fmt(fmt):
    fmt = fmt[1:]
    
    typ = None
    prec = -1
    width = 0
    pad = ord(' ')
    left = False
    showsign = False
    L = False
    h = False
    l = False
    hh = False
    
    if fmt[0] == "+":
        showsign = True
        fmt = fmt[1:]

    elif fmt[0] == "-":
        left = True
        fmt = fmt[1:]

    if fmt[0] == "0":
        pad = ord("0")

    if "hh" in fmt:
        hh = True
    elif "h" in fmt:
        h = True
    elif ("ll" in fmt) or ("L" in fmt):
        L = True
    elif "l" in fmt:
        l = True

    typ = fmt[-1]

    if "." in fmt:
        fmt1, fmt2 = fmt.split('.')
        if len(fmt1) > 0:
            width = int(fmt1)
        while not fmt2[-1].isdigit():
            fmt2 = fmt2[:-1]
        prec = int(fmt2)
    else:
        while not fmt[-1].isdigit():
            fmt = fmt[:-1]
        width = int(fmt)

    return (typ, prec, width, pad, left, showsign, l, h, L, hh)
```

With all the fields parsed, we can emulates the instructions easily using the knowledge from the last section. There is a little gimmick here about memory access, because accessing `MEM` is by 8-bit and `REGS` is by 32-bit, but the arithmetic instructions treat both of them the same way. Therefore, I have to define both of them as 8-bit arrays and use 2 helper functions `load32` and `store32` to access the registers.

The code for emulating is quite lengthy but straight-forward, everything that needs to be known to implement it has been explained, so I will just leave the code here without explaining more about it.

```python
def exec_calc(typ, prec, width, pad, left, showsign, l, h, L, hh):
    addr = 0
    where = 0
    val = 0
    dbg_cmd = ""
    dbg_where = ""
    dbg_addr = ""
    dbg_val = ""

    if left:
        addr = width
        where = mem
        dbg_where = "MEM"
        dbg_addr = str(addr)
    elif showsign:
        addr = load32(regs, width*8)
        where = mem
        dbg_where = "MEM"
        dbg_addr = "REGS[{}]".format(str(width))
    else:
        addr = width*8
        where = regs
        dbg_where = "REGS"
        dbg_addr = str(width)

    if hh:
        val = load32(mem, prec)
        dbg_val = "MEM[{}]".format(prec)
    elif h:
        val = load32(mem, load32(regs, prec*8))
        dbg_val = "MEM[REGS[{}]]".format(prec)
    elif L:
        val = prec
        dbg_val = str(prec)
    elif l:
        val = load32(regs, prec*8)
        dbg_val = "REGS[{}]".format(prec)

    left = load32(where, addr)
    right = val

    if typ == "M":
        val = val
        dbg_cmd = "LOAD"
    elif typ == "S":
        val = (load32(where, addr) + val) & 0xffffffff
        dbg_cmd = "ADD"
    elif typ == "O":
        val = (load32(where, addr) - val) & 0xffffffff
        dbg_cmd = "SUB"
    elif typ == "X":
        val = (load32(where, addr) * val) & 0xffffffff
        dbg_cmd = "MULT"
    elif typ == "V":
        val = load32(where, addr) // val
        dbg_cmd = "DIV"
    elif typ == "N":
        val = load32(where, addr) % val
        dbg_cmd = "MOD"
    elif typ == "L":
        val = (load32(where, addr) << val) & 0xffffffff
        dbg_cmd = "LSHIFT"
    elif typ == "R":
        val = (load32(where, addr) >> val) & 0xffffffff
        dbg_cmd = "RSHIFT"
    elif typ == "E":
        val = load32(where, addr) ^ val
        dbg_cmd = "XOR"
    elif typ == "I":
        val = load32(where, addr) & val
        dbg_cmd = "AND"
    elif typ == "U":
        val = load32(where, addr) | val
        dbg_cmd = "OR"
    else:
        print("UNKNOWN TYPE", typ)
        sys.exit(-1)

    store32(where, addr, val)
    
    print("{} {}[{}], {}".format(dbg_cmd, dbg_where, dbg_addr, dbg_val).ljust(30, " "), end="")
    print("# addr = {}, val_1 = {}, val_2 = {}, result = {}".format(hex(addr), hex(left), hex(right), hex(val)))

def exec_call(typ, prec, width, pad, left, showsign, l, h, L, hh):

    if typ != "C":
        print("UNKNOWN TYPE", typ)
        sys.exit(-1)
    
    cmp_flag = True
    dbg_cmd = ""
    dbg_reg = prec
    dbg_addr = width

    if left:
        cmp_flag = load32(regs, prec*8) > 0x7fffffff
        dbg_cmd = "CLZ"
    elif showsign:
        cmp_flag = (load32(regs, prec*8) < 0x80000000) and (load32(regs, prec*8) > 0)
        dbg_cmd = "CGZ"
    elif pad == ord('0'):
        cmp_flag = load32(regs, prec*8) == 0
        dbg_cmd = "CEZ"
    else:
        cmp_flag = True
        dbg_cmd = "CALL"

    print("{} REGS[{}], {}".format(dbg_cmd, dbg_reg, dbg_addr).ljust(30, " "), end="")
    print("# val = {}, cmp_flag = {}".format(load32(regs, prec*8), cmp_flag))

    if cmp_flag:
        execute(width)

def execute(init_pc):
    global regs, mem, s, v
    pc = init_pc
    while True:
        try:
            next_pc = mem[pc+1:].index(ord("%")) + 1 + pc
            fmt = ''.join([chr(b) for b in mem[pc:next_pc]])
            null = mem[pc+1:].index(ord("\0")) + 1 + pc
        except: # At the end no more %
            null = mem[pc+1:].index(ord("\0")) + 1 + pc
            fmt = ''.join([chr(b) for b in mem[pc:null]])
            next_pc = null + 1

        fmt = fmt.strip('\0')

        print("{}".format(pc).ljust(10, " "), end="")
        print("{}".format(fmt).ljust(30, " "), end="")
        
        pc = next_pc
        typ, prec, width, pad, left, showsign, l, h, L, hh = parse_fmt(fmt)
        if typ == "C":
            exec_call(typ, prec, width, pad, left, showsign, l, h, L, hh)
        else:
            exec_calc(typ, prec, width, pad, left, showsign, l, h, L, hh)

        if (next_pc - 1 >= null):
            print("{}".format(null).ljust(10) + "RET")
            break
```

The disassembler is basically the same as the emulator, except that instead of doing load/store/calculations/calls, we just decode the instruction and continue to the next one.
```python
def disass_calc(typ, prec, width, pad, left, showsign, l, h, L, hh):
    addr = 0
    where = 0
    val = 0
    dbg_cmd = ""
    dbg_where = ""
    dbg_addr = ""
    dbg_val = ""

    if left:
        dbg_where = "MEM"
        dbg_addr = str(width)
    elif showsign:
        dbg_where = "MEM"
        dbg_addr = "REGS[{}]".format(str(width))
    else:
        dbg_where = "REGS"
        dbg_addr = str(width)

    if hh:
        dbg_val = "MEM[{}]".format(prec)
    elif h:
        dbg_val = "MEM[REGS[{}]]".format(prec)
    elif L:
        dbg_val = str(prec)
    elif l:
        dbg_val = "REGS[{}]".format(prec)

    if typ == "M":
        dbg_cmd = "LOAD"
    elif typ == "S":
        dbg_cmd = "ADD"
    elif typ == "O":
        dbg_cmd = "SUB"
    elif typ == "X":
        dbg_cmd = "MULT"
    elif typ == "V":
        dbg_cmd = "DIV"
    elif typ == "N":
        dbg_cmd = "MOD"
    elif typ == "L":
        dbg_cmd = "LSHIFT"
    elif typ == "R":
        dbg_cmd = "RSHIFT"
    elif typ == "E":
        dbg_cmd = "XOR"
    elif typ == "I":
        dbg_cmd = "AND"
    elif typ == "U":
        dbg_cmd = "OR"
    else:
        print("UNKNOWN TYPE", typ)
        sys.exit(-1)

    print("{} {}[{}], {}".format(dbg_cmd, dbg_where, dbg_addr, dbg_val).ljust(30, " "))


def disass_call(typ, prec, width, pad, left, showsign, l, h, L, hh):

    if typ != "C":
        print("UNKNOWN TYPE", typ)
        sys.exit(-1)
    
    cmp_flag = True
    dbg_cmd = ""
    dbg_reg = prec
    dbg_addr = width

    if left:
        dbg_cmd = "CLZ"
    elif showsign:
        dbg_cmd = "CGZ"
    elif pad == ord('0'):
        dbg_cmd = "CEZ"
    else:
        dbg_cmd = "CALL"

    print("{} REGS[{}], {}".format(dbg_cmd, dbg_reg, dbg_addr).ljust(30, " "))


def disass(init_pc):
    global regs, mem
    pc = init_pc
    while True:
        try:
            next_pc = mem[pc+1:].index(ord("%")) + 1 + pc
            fmt = ''.join([chr(b) for b in mem[pc:next_pc]])
            null = mem[pc+1:].index(ord("\0")) + 1 + pc
        except: # At the end no more %
            null = mem[pc+1:].index(ord("\0")) + 1 + pc
            fmt = ''.join([chr(b) for b in mem[pc:null]])
            next_pc = null + 1

        fmt = fmt.strip('\0')
        if (len(fmt) == 0) or (fmt[0] != "%"):
            break

        print("{}".format(pc).ljust(10, " "), end="")
        print("{}".format(fmt).ljust(30, " "), end="")
        
        pc = next_pc
        typ, prec, width, pad, left, showsign, l, h, L, hh = parse_fmt(fmt)
        if typ == "C":
            disass_call(typ, prec, width, pad, left, showsign, l, h, L, hh)
        else:
            disass_calc(typ, prec, width, pad, left, showsign, l, h, L, hh)

        if next_pc - 1 >= null:
            print("{}".format(null).ljust(10) + "RET\n")
```


## Analyze the first code block
When I was solving this challenge, I actually mostly used just the emulator and only look at the code where it stucks. But in this writeups, I will explain the code by disassembling them instead of saying "just run the emulator".

Remembering that the VM starts executing by a `%52C` call, I disassembled `MEM[52]` to see what code is there:
```bash
52        %0.4096hhM                    LOAD REGS[0], MEM[4096]       
62        %0.255llI                     AND REGS[0], 255              
71        %1.0lM                        LOAD REGS[1], REGS[0]         
77        %1.8llL                       LSHIFT REGS[1], 8             
84        %0.1lU                        OR REGS[0], REGS[1]           
90        %1.0lM                        LOAD REGS[1], REGS[0]         
96        %1.16llL                      LSHIFT REGS[1], 16            
104       %0.1lU                        OR REGS[0], REGS[1]           
110       %1.200llM                     LOAD REGS[1], 200             
119       %2.1788llM                    LOAD REGS[2], 1788            
129       %7C                           CALL REGS[-1], 7              
132       %-6144.1701736302llM          LOAD MEM[6144], 1701736302    
152       %0.200hhM                     LOAD REGS[0], MEM[200]        
161       %0.255llI                     AND REGS[0], 255              
170       %0.37llO                      SUB REGS[0], 37               
178       %0200.0C                      CEZ REGS[0], 200              
186       RET
```

The access to `MEM[4096]` looks sus, but recall that `MEM` is at address `5080`, so `MEM[4096]` will be at `6080`. If you have a good memory, in the first section where we analyzed `main`, this is the address of our input! So basically this first few instructions will read the first 4 bytes of our input, then reduce it to the first 1 byte to save in `REGS[0]`, then load 200 to `REGS[1]`, 1788 to `REGS[2]` and call `%7C`. Let's disassemble at `MEM[7]`:
```bash
7         %3.1hM                        LOAD REGS[3], MEM[REGS[1]]    
13        %3.0lE                        XOR REGS[3], REGS[0]          
19        %+1.3lM                       LOAD MEM[REGS[1]], REGS[3]    
26        %1.4llS                       ADD REGS[1], 4                
33        %3.1lM                        LOAD REGS[3], REGS[1]         
39        %3.2lO                        SUB REGS[3], REGS[2]          
45        %-7.3C                        CLZ REGS[3], 7                
51        RET
```

We can see that `REGS[1]` is used as an index to `MEM` and `REGS[2]` is used as a counter. If we look in the binary at `MEM[200]`, it contains a bunch of weird bytes that looks like encrypted data. This code at `MEM[7]` basically decrypt that block of encrypted data using `REGS[0]` as the key, which is the first byte of our input. 

After finishing decrypting the data, it returns back to `MEM[132]`, this instruction loads the string `"none"` to `MEM[6144]`. Because when we run the binary normally and pass in a random input, it prints out `Flag: none`, so `MEM[6144]` will probably contain the flag. The VM then compares the value at `MEM[200]` to 37 and calls to it if they are equal. The value 37 is actually the ASCII value of `'%'`, so with this we can retrieve the first correct byte of our input by XORing 37 with the first byte in the encrypted data, resulting in the character `'T'`.

After knowing the first correct byte is `'T'`, I reran the emulator and indeed it called to `MEM[200]`. Let's analyze this block of code.

## Analyze the decrypted code block
The disassembly result:
```bash
200       %4.5000llM                    LOAD REGS[4], 5000            
210       %0.13200llM                   LOAD REGS[0], 13200           
221       %337C                         CALL REGS[-1], 337            
226       %0.0llM                       LOAD REGS[0], 0               
233       %500C                         CALL REGS[-1], 500            
238       %1262C                        CALL REGS[-1], 1262           
244       %0653.0C                      CEZ REGS[0], 653              
252       RET

253       %1.0llM                       LOAD REGS[1], 0               
260       RET

261       %3.0lM                        LOAD REGS[3], REGS[0]         
267       %3.2lN                        MOD REGS[3], REGS[2]          
273       %0253.3C                      CEZ REGS[3], 253              
281       %2.1llS                       ADD REGS[2], 1                
288       %3.2lM                        LOAD REGS[3], REGS[2]         
294       %3.3lX                        MULT REGS[3], REGS[3]         
300       %3.0lO                        SUB REGS[3], REGS[0]          
306       %3.1llO                       SUB REGS[3], 1                
313       %-261.3C                      CLZ REGS[3], 261              
321       RET

322       %+4.0lM                       LOAD MEM[REGS[4]], REGS[0]    
329       %4.2llS                       ADD REGS[4], 2                
336       RET

337       %1.1llM                       LOAD REGS[1], 1               
344       %2.2llM                       LOAD REGS[2], 2               
351       %261C                         CALL REGS[-1], 261            
356       %+322.1C                      CGZ REGS[1], 322              
364       %0.1llS                       ADD REGS[0], 1                
371       %1.13600llM                   LOAD REGS[1], 13600           
382       %1.0lO                        SUB REGS[1], REGS[0]          
388       %+337.1C                      CGZ REGS[1], 337              
396       RET

397       %0.0llM                       LOAD REGS[0], 0               
404       RET

405       %0.2llV                       DIV REGS[0], 2                
412       RET

413       %0.3llX                       MULT REGS[0], 3               
420       %0.1llS                       ADD REGS[0], 1                
427       RET

428       %1.0lM                        LOAD REGS[1], REGS[0]         
434       %1.2llN                       MOD REGS[1], 2                
441       %0405.1C                      CEZ REGS[1], 405              
449       %+413.1C                      CGZ REGS[1], 413              
457       %470C                         CALL REGS[-1], 470            
462       %0.1llS                       ADD REGS[0], 1                
469       RET

470       %1.0lM                        LOAD REGS[1], REGS[0]         
476       %1.1llO                       SUB REGS[1], 1                
483       %0397.1C                      CEZ REGS[1], 397              
491       %+428.1C                      CGZ REGS[1], 428              
499       RET

500       %2.0lM                        LOAD REGS[2], REGS[0]         
506       %2.4096llS                    ADD REGS[2], 4096             
516       %4.2hM                        LOAD REGS[4], MEM[REGS[2]]    
522       %4.255llI                     AND REGS[4], 255              
531       %+540.4C                      CGZ REGS[4], 540              
539       RET

540       %2.0lM                        LOAD REGS[2], REGS[0]         
546       %2.2llX                       MULT REGS[2], 2               
553       %2.5000llS                    ADD REGS[2], 5000             
563       %2.2hM                        LOAD REGS[2], MEM[REGS[2]]    
569       %2.255llI                     AND REGS[2], 255              
578       %4.2lE                        XOR REGS[4], REGS[2]          
584       %0.1llS                       ADD REGS[0], 1                
591       %2.0lM                        LOAD REGS[2], REGS[0]         
597       %470C                         CALL REGS[-1], 470            
602       %4.0lS                        ADD REGS[4], REGS[0]          
608       %4.255llI                     AND REGS[4], 255              
617       %0.2lM                        LOAD REGS[0], REGS[2]         
623       %2.1llO                       SUB REGS[2], 1                
630       %2.4500llS                    ADD REGS[2], 4500             
640       %+2.4lM                       LOAD MEM[REGS[2]], REGS[4]    
647       %500C                         CALL REGS[-1], 500            
652       RET

653       %0.123456789llM               LOAD REGS[0], 123456789       
668       %1.0llM                       LOAD REGS[1], 0               
675       %1.4096llS                    ADD REGS[1], 4096             
685       %1.1hM                        LOAD REGS[1], MEM[REGS[1]]    
691       %0.1lE                        XOR REGS[0], REGS[1]          
697       %2.0llM                       LOAD REGS[2], 0               
704       %2.846786818llS               ADD REGS[2], 846786818        
719       %2.0lE                        XOR REGS[2], REGS[0]          
725       %1.0llM                       LOAD REGS[1], 0               
732       %1.6144llS                    ADD REGS[1], 6144             
742       %+1.2lM                       LOAD MEM[REGS[1]], REGS[2]    
749       %1.4llM                       LOAD REGS[1], 4               
756       %1.4096llS                    ADD REGS[1], 4096             
766       %1.1hM                        LOAD REGS[1], MEM[REGS[1]]    
772       %0.1lE                        XOR REGS[0], REGS[1]          
778       %2.0llM                       LOAD REGS[2], 0               
785       %2.1443538759llS              ADD REGS[2], 1443538759       
801       %2.0lE                        XOR REGS[2], REGS[0]          
807       %1.4llM                       LOAD REGS[1], 4               
814       %1.6144llS                    ADD REGS[1], 6144             
824       %+1.2lM                       LOAD MEM[REGS[1]], REGS[2]    
831       %1.8llM                       LOAD REGS[1], 8               
838       %1.4096llS                    ADD REGS[1], 4096             
848       %1.1hM                        LOAD REGS[1], MEM[REGS[1]]    
854       %0.1lE                        XOR REGS[0], REGS[1]          
860       %2.0llM                       LOAD REGS[2], 0               
867       %2.1047515510llS              ADD REGS[2], 1047515510       
883       %2.0lE                        XOR REGS[2], REGS[0]          
889       %1.8llM                       LOAD REGS[1], 8               
896       %1.6144llS                    ADD REGS[1], 6144             
906       %+1.2lM                       LOAD MEM[REGS[1]], REGS[2]    
913       %1.12llM                      LOAD REGS[1], 12              
921       %1.4096llS                    ADD REGS[1], 4096             
931       %1.1hM                        LOAD REGS[1], MEM[REGS[1]]    
937       %0.1lE                        XOR REGS[0], REGS[1]          
943       %2.0llM                       LOAD REGS[2], 0               
950       %2.359499514llS               ADD REGS[2], 359499514        
965       %2.1724461856llS              ADD REGS[2], 1724461856       
981       %2.0lE                        XOR REGS[2], REGS[0]          
987       %1.12llM                      LOAD REGS[1], 12              
995       %1.6144llS                    ADD REGS[1], 6144             
1005      %+1.2lM                       LOAD MEM[REGS[1]], REGS[2]    
1012      %1.16llM                      LOAD REGS[1], 16              
1020      %1.4096llS                    ADD REGS[1], 4096             
1030      %1.1hM                        LOAD REGS[1], MEM[REGS[1]]    
1036      %0.1lE                        XOR REGS[0], REGS[1]          
1042      %2.0llM                       LOAD REGS[2], 0               
1049      %2.241024035llS               ADD REGS[2], 241024035        
1064      %2.0lE                        XOR REGS[2], REGS[0]          
1070      %1.16llM                      LOAD REGS[1], 16              
1078      %1.6144llS                    ADD REGS[1], 6144             
1088      %+1.2lM                       LOAD MEM[REGS[1]], REGS[2]    
1095      %1.20llM                      LOAD REGS[1], 20              
1103      %1.4096llS                    ADD REGS[1], 4096             
1113      %1.1hM                        LOAD REGS[1], MEM[REGS[1]]    
1119      %0.1lE                        XOR REGS[0], REGS[1]          
1125      %2.0llM                       LOAD REGS[2], 0               
1132      %2.222267724llS               ADD REGS[2], 222267724        
1147      %2.0lE                        XOR REGS[2], REGS[0]          
1153      %1.20llM                      LOAD REGS[1], 20              
1161      %1.6144llS                    ADD REGS[1], 6144             
1171      %+1.2lM                       LOAD MEM[REGS[1]], REGS[2]    
1178      %1.24llM                      LOAD REGS[1], 24              
1186      %1.4096llS                    ADD REGS[1], 4096             
1196      %1.1hM                        LOAD REGS[1], MEM[REGS[1]]    
1202      %0.1lE                        XOR REGS[0], REGS[1]          
1208      %2.0llM                       LOAD REGS[2], 0               
1215      %2.844096018llS               ADD REGS[2], 844096018        
1230      %2.0lE                        XOR REGS[2], REGS[0]          
1236      %1.24llM                      LOAD REGS[1], 24              
1244      %1.6144llS                    ADD REGS[1], 6144             
1254      %+1.2lM                       LOAD MEM[REGS[1]], REGS[2]    
1261      RET

1262      %0.0llM                       LOAD REGS[0], 0               
1269      %1.0llM                       LOAD REGS[1], 0               
1276      %1.4500llS                    ADD REGS[1], 4500             
1286      %1.1hM                        LOAD REGS[1], MEM[REGS[1]]    
1292      %2.0llM                       LOAD REGS[2], 0               
1299      %2.1374542625llS              ADD REGS[2], 1374542625       
1315      %2.1686915720llS              ADD REGS[2], 1686915720       
1331      %2.1129686860llS              ADD REGS[2], 1129686860       
1347      %1.2lE                        XOR REGS[1], REGS[2]          
1353      %0.1lU                        OR REGS[0], REGS[1]           
1359      %1.4llM                       LOAD REGS[1], 4               
1366      %1.4500llS                    ADD REGS[1], 4500             
1376      %1.1hM                        LOAD REGS[1], MEM[REGS[1]]    
1382      %2.0llM                       LOAD REGS[2], 0               
1389      %2.842217029llS               ADD REGS[2], 842217029        
1404      %2.1483902564llS              ADD REGS[2], 1483902564       
1420      %1.2lE                        XOR REGS[1], REGS[2]          
1426      %0.1lU                        OR REGS[0], REGS[1]           
1432      %1.8llM                       LOAD REGS[1], 8               
1439      %1.4500llS                    ADD REGS[1], 4500             
1449      %1.1hM                        LOAD REGS[1], MEM[REGS[1]]    
1455      %2.0llM                       LOAD REGS[2], 0               
1462      %2.1868013731llS              ADD REGS[2], 1868013731       
1478      %1.2lE                        XOR REGS[1], REGS[2]          
1484      %0.1lU                        OR REGS[0], REGS[1]           
1490      %1.12llM                      LOAD REGS[1], 12              
1498      %1.4500llS                    ADD REGS[1], 4500             
1508      %1.1hM                        LOAD REGS[1], MEM[REGS[1]]    
1514      %2.0llM                       LOAD REGS[2], 0               
1521      %2.584694732llS               ADD REGS[2], 584694732        
1536      %2.1453312700llS              ADD REGS[2], 1453312700       
1552      %1.2lE                        XOR REGS[1], REGS[2]          
1558      %0.1lU                        OR REGS[0], REGS[1]           
1564      %1.16llM                      LOAD REGS[1], 16              
1572      %1.4500llS                    ADD REGS[1], 4500             
1582      %1.1hM                        LOAD REGS[1], MEM[REGS[1]]    
1588      %2.0llM                       LOAD REGS[2], 0               
1595      %2.223548744llS               ADD REGS[2], 223548744        
1610      %1.2lE                        XOR REGS[1], REGS[2]          
1616      %0.1lU                        OR REGS[0], REGS[1]           
1622      %1.20llM                      LOAD REGS[1], 20              
1630      %1.4500llS                    ADD REGS[1], 4500             
1640      %1.1hM                        LOAD REGS[1], MEM[REGS[1]]    
1646      %2.0llM                       LOAD REGS[2], 0               
1653      %2.1958883726llS              ADD REGS[2], 1958883726       
1669      %2.1916008099llS              ADD REGS[2], 1916008099       
1685      %1.2lE                        XOR REGS[1], REGS[2]          
1691      %0.1lU                        OR REGS[0], REGS[1]           
1697      %1.24llM                      LOAD REGS[1], 24              
1705      %1.4500llS                    ADD REGS[1], 4500             
1715      %1.1hM                        LOAD REGS[1], MEM[REGS[1]]    
1721      %2.0llM                       LOAD REGS[2], 0               
1728      %2.1829937605llS              ADD REGS[2], 1829937605       
1744      %2.1815356086llS              ADD REGS[2], 1815356086       
1760      %2.253836698llS               ADD REGS[2], 253836698        
1775      %1.2lE                        XOR REGS[1], REGS[2]          
1781      %0.1lU                        OR REGS[0], REGS[1]           
1787      RET
```

Quite lengthy code, and actually because I have a working emulator, I didn't bother understand all of it. But there are some important points that must be noticed:
- The function at `MEM[200]` calls `MEM[500]` then `MEM[1262]`.
- The function at `MEM[500]` accesses `MEM[4096]`, which is our input.
- The function at `MEM[1262]` is called after `MEM[500]`, and there is a conditional call `CEZ REGS[0], 653` at `MEM[244]` after it returns.
- The function at `MEM[653]` accesses `MEM[4096]` and `MEM[6144]`, which is where I suspected the flag to be, so this is probably where the flag is decrypted.

Therefore, we want to get to `MEM[653]`, which means that `REGS[0]` must equal to 0 after `MEM[1262]`. This was enough information for me to insert `z3` in and let it solve everything for me.

## Inserting z3
The first step is to insert `z3` into our input. By looking at the function at `MEM[500]`, `MEM[1262]` and `MEM[653]`, we can see that the correct input is probably 28 bytes in length. Because we already knew the first byte, I declared 27 `BitVec` for the rest 27.

{{< admonition warning "Warning" >}}
*The `BitVec`s MUST be declared as 32-bit instead of 8-bit !!! The reason is all the calculations in this VM is 32-bit, if you declare the `BitVec` to be 8-bit it will truncate the result to 8-bit and ruin the calculations. This costs me like 2-3 hours to figure out.
{{< /admonition >}}

Some changes need to be made for the emulator:
- We know that the real code starts at `MEM[200]`, so I declared `z3` variables when the VM hits `MEM[200]`.
- The function at `MEM[500]` accesses our input, at `MEM[531]` there is a comparison with our input. Because our input is `z3` variables now, it will cause `python` to raise an exception when using `z3` variables in a `if-else` condition. Therefore, I made it so that it always returns `True` at `MEM[531]` if `z3` variables is in the condition.
- We know the comparison is at `MEM[244]`, so I add the `z3` constraint when the VM reaches there.

The full solver/emulator/disassembler is at [a.py](a.py). Let it run for a while and it will give us the correct input: `TheNewFlagHillsByTheCtfWoods`.

Run the binary normally and input that string, we get the flag: `CTF{curs3d_r3curs1ve_pr1ntf}`

## Appendix
The full solver/emulator/disassembler is at [a.py](a.py).
