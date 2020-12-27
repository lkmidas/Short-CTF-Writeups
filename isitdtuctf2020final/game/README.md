# ISITDTU CTF 2020 Final - Game

## Introduction
**Given files:** `Auto9Yin.2.72.17.zip`.

**Description:** In this challenge, our goal is to decrypt this key: `C2BAC628EC275E5F9D64A403A57AF4E9880BA46AE78560CC0B26F6D630C93A5BC3153098F77E7A871FE7C7484F72F36BC42BFA9E0E331C186E33646BDC61C9F21958CBE5DC6468EB84676F99C2504BA7B8BA29463E9C481C1182C4A718D2E45EB2ACEA664D10249E8F34DDA801E5692ECB3E4E34375589D38CCE4018A004C7EC9C6805C27A2D37C45290C38F7D7CE679762567DB2FDD44309F74365C18310673F6B98D99A1A27E2204555B3D12113CC4C72B665548C3738BE2E310206A68E89A1E5BE492AC00ABC22ACA5099FDF7E1426D82AF89AF53D8A84255002D166352890DA2FE8881450D836FC95AE28C9F604ACB00D3CF95CB2AAF1445F0D1234DE1BAD13739E6D18B3D0718ABD10C259635B6`

**Category:** Reverse engineering

**Summary:** This is a real world reverse engineering problem of an online game's third-party module. This is a paid botting module that requires player to buy a key to gain access to its features. Our task is to reverse engineer the key check phase in order to decrypt the given key. The author also gives us a [link to download the actual game](http://cuuam.gosu.vn/tai-game.html) (which is 22GB in size!) and a [link to a video](https://www.youtube.com/watch?v=M-GNl2B6m7A) where he shows us how to install and use the `Auto9Yin` module.

## TL;DR:
1. *Optional:* Download the game, watch the video and test out the module itself.
2. Extract the module and investigate it => See a lot of DLLs.
3. Investigate the `lua` scripts => See some scripts that load `auto_main` and `auto_core`.
4. Analyze the corresponding DLLs (and some others) => See the same structure, only differ is in the encrypted part.
5. Decrypt the similar part => Get a `lua` function to decrypt the different parts.
6. Decrypt the different part in `auto_9yin.dll` => Get the `lua` script that has the encrypt and decrypt routine.
7. Use the script to decrypt the given key => Get flag.

## Optional: Install the game and Auto9Yin
Before the event even started, the author gave us a link to download the game itself, because the game would be too large to be downloaded on site. I downloaded the game the night before and tried to play with it for a bit. It is actually a real Chinese RPG that got translated into Vietnamese that has quite a large player base. The game itself is free-to-play, so I didn't know what do we have to crack yet, so I just kept it as it is.

The day after, in the competition, we are given this challenge. The author gives us a link where he demonstrates how to install the `Auto9Yin` module itself and how to activate it. To activate it, we have to buy a valid code and submit it into the game, then we will have access to various botting features. I label this section as *Optional* because actually, we don't need to install neither the game nor the module, all we have to do is decrypt the given key.

## First look into the module and the lua scripts
Extracting the given zip files, I ended up with a quite large folder. There is a `bin` folder inside of it which contains many DLL files, which is quite intimidating to look at. Therefore, I didn't start by looking into the DLLs, but instaed at the folder `lua` (because I have watched some game development video before and they like to do scripting in `lua`, so this folder might be interesting). In that folder, I saw some short `lua` scripts that load `auto_main` and `auto_core`, which are 2 of the DLLs in `bin`. So I continued by analyzing these 2 DLLs.

## Analyzing the DLLs
Opening the 2 mentioned DLLs in IDA, I saw that all the functions in them are similar, I also opened other DLLs as well, and they are all almost similar. The only difference between them is that in function `luaopen_auto_*()` (`*` is different for each DLL), the strings that look to be encrypted are different. `luaopen_auto_*()` first makes a call to `sub_10001130()`, so I analyzed this function first.

This function is similar accross all DLLs and has a repeated pattern: first copies an encrypted string to a buffer, call `sub_10001000()` on it, then calls `luaL_loadbuffer()` and `lua_pcall()`. By quickly doing some Google search, I knew that the 2 latter functions are just from an API to interact with `lua` from native code. As far as I know, `luaL_loadbuffer()` compiles a piece of lua code, then pushes it into the lua stack, and `lua_pcall()` pops and runs it. Therefore, `sub_10001000()` must be the function where it decrypts the encrypted buffer into `lua` code.

## Decrypting the similar encrypted part
The decryption routine in `sub_10001000()` is not hard to understand: it simply maps some specific characters in the string to other characters then subtracts it by 1, and keeps the rest unchanged. It is easy enough to re-implement in python:

```python
MAP = {'H':'!', 'U':'*', 'N':'>', 'G':')', 'X':'e', 'I':'j', 'O':'v', 'A':'u', 'W':' ', 'T':'#', 'M':'/', 'L':'-', 'Y':'{', 'Z':'(', 'J':':', 'P':'^', 'C':'|', 'Q':'\\'}

def decrypt(str):
    result = ""
    i = len(str) - 1
    while True:
        c = str[i]
        if c in MAP.keys():
            c = chr(ord(MAP[str[i]]) - 1)
        else:
            c = chr(ord(str[i]) - 1)
        result += c
        i -= 1
        if i < 0:
            break
    return result
```

Using this python function to decrypt the encrypted buffer, I obtained the code in `xingxiang.lua`, which is obfuscated in the way that each of its function is written on only one line. I asked my teammate `@pcback` to help me beautify the lua code and re-implement it in python:

```python
def axing(buff):
    return ''.join(chr(int(buff[i:i+2],16)-1) for i in range(0, len(buff), 2))

begin = [ '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f' ]
last = [ 'x', 'u', 'h', 's', 'p', 'v', 'g', 'q', 'r', 'y', 'z', 'n', 'm', 'i', 'w','k']

def decr(buff):
    temp = buff[::]
    for i in range(16):
        temp = temp.replace(last[i], begin[i])
    return temp

def reveser(s):
    return s[::-1]

def axiang(buff):
    temp = buff.replace('5', 'z')
    temp = temp.replace('f', '5')
    temp = temp.replace('z', 'f')
    temp = buff.replace('6', 'z')
    temp = temp.replace('d', '6')
    temp = temp.replace('z', 'd')
    return temp

def xingxiang(s):
    return reveser(axing(axiang(decr(reveser(s)))))
```

I was done with `sub_10001130()`, so I returned to `luaopen_auto_*()`. The function then calls `sub_10001300()` on a lot of encrypted strings.

## Decrypting the different parts
This function is quite small. First it uses the same decryption routine that decrypts the `xingxiang` script on a small string to obtain the string `"xingxiang"`, then it uses some lua API functions on this string and on the encrypted parameter. I didn't look much into the documentation this time, because it is almost certain that it uses `xingxiang` to decrypt the encrypted parameter, so I simply used the python code for `xingxiang` above to decrypt all of `auto_main.dll` and `auto_core.dll`.

Disappointingly, decrypting these 2 DLLs only results in lua scripts that handle the in-game botting stuffs, there is no code in those scripts that take care of the key. My thought process then was to decrypt all of the DLLs to find what I seek. Of course though, I had to look at the DLLs that have the most interesting names first, so I instantly looked at `auto_9yin.dll`, and I did hit the jackpot.

## Running auto9yin to decrypt the key
The decrypted lua code from `auto_9yin.dll` is well commented, and it is used to handle everything about the key. Thereis a decrypt function in there, so firstly, I asked `@pcback` again to recode it into python. However, because of some differences between lua and python, he didn't succeed in doing that this time, so I have to find another way to do it.

My solution was to run the lua script itself on the given key to get the flag. However, there were also some hiccups doing this:
- The script requires some packages that is loaded somewhere else and I didn't have them, so I imple tried to remove all the `require()` calls.
- Doing the above will result in the lua script missing the `hex` and the `bit` packages. 
- I googles for those, but I can't find `hex`, so I looked in the script to find where it is used, and found out that it is simply use to convert the hex representation of the key into bytes. Therefore, I can do this in python, copy the result into lua and get rid of `hex`.
- For `bit`, I found it on the Internet, so I simply copy and paste it into the same folder.

With the above setups, I could successfully run the lua script to get the flag:
```
danchoihephoco,1922762076,This key was used as a real world challenge for a cyber security contest (see https://www.facebook.com/isitdtu/). If you are owner of this product, please do not share or leak it, thanks a lot. ISITDTU{r34l_w0rd_1s_fUn_4nd_34sY_bUt_lu4_sUcKs}
```

## Appendix
The script for decrypting both the similar and the different parts in DLLs is `decrypt.py`.

The decrypted `auto_9yin.dll` lua script is `auto_9yin.lua`

The `bit` package for lua is `bit.lua`.

The modified lua script to decrypt the key is `a.lua`.
