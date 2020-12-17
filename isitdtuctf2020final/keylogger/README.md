# ISITDTU2020 FINALS: KEYLOGGER (RE)

## Introduction
**Given files:** `Launcher.exe`, `capture.pcapng`.

**Description:** `We are tracking a suspect in a gold robbery of 4 men, After a few days he had access to a public computer. We then analyzed that computer and found it a keylogger software that someone secretly installed earlier, Hope you can find out what the thief accessed, whom to contact, any information that could lead to evidence of the robbery. `

## Analyzing Launcher.exe
The `Launcher.exe` executable file throws an error when being executed, then it seems like nothing happens after that. So I started to reverse it statically using IDA. The flow is quite simple: it first throws a fake error about missing a DLL, then clones itself using the name `XblAuthenticator.exe`, then decrypts some data and saves it under the name `XblCloud.dll`, all the files created in this challenge are somehow related to XBox stuffs, but most likely they are just fake names. My teammates said that it also does something to the registry hive, but that information is unecessary for the solution. The most important thing then was to get the DLL file. I think it can be retrieved by reversing the decryption function and decrypting the data, but my teammate `@Edisc` used `SpyStudio` and dumped it out for me. So all I needed to do was to continue and analyze the DLL file and the traffic capture file.

## First look at capture.pcapng
Before reversing the big DLL file, I took a look at the network traffic capture. One of the things that I like to do when analyzing a `pcap` file is to throw it into `Wireshark` and then use the `Follow TCP stream` functionality to skim through all the TCP streams. Here are the informations that I gathered from doing that:
- The user (or the keylogger, I didn't know yet) sended a zip file called `message.zip` containing `message.txt` to `c.unsafesector.com/upload` in TCP stream number 4. Dumping the zip file and trying to extract it, I found out that it is archived using an unknown password.
- TCP streams number 0, 1, 2, 5, 6, 7, 8, 9, 11, 12 are quite identical, it seems like they contain the logged key presses and got encoded as a protocol in some way.
- TCP stream number 10 is quite large, and I had no information about it yet.

Since the packets are likely to be encoded in a custom protocol, I moved on to investigate `XblCloud.dll` to reverse it.

## Analyzing XblCloud.dll
Analyzing from `DllEntryPoint()` onward, I arrived at function `sub_180002370`, which makes a lot of calls to `GetAsyncKeyState()`. 

The first two `GetAsyncKeyState()` are called with parameters 1 and 2, respectively. Looking at Microsoft's [virtual key codes documentation](https://docs.microsoft.com/en-us/windows/win32/inputdev/virtual-key-codes), I knew that these are to log mouse presses. I could also see that the X and Y coordinates of the cursor are encrypted by XORing with `0xCAFEFAAA`.

The next two `GetAsyncKeyState()` are called with parameters from `0x30 - 0x39` and `0x60 - 0x69`. Again looking at the documentation, these are the number keys from 0 to 9, with `0x30 - 0x39` being normal keys and `0x60 - 0x69` being the numpad keys. They are then added with a constant to map into the range of `0x96 - 0x9f`.

The next `GetAsyncKeyState()` is called with parameter from `0x41 - 0x5a`, these are uppercase characters from A to Z. The encoding here is subtracting by `0x7a`.

The last `GetAsyncKeyState()` is specifically for the whitespace character `0x20`, which is encoded into `0x86`.

Also in each of these encoding, I saw that a timestamp retrieved from `GetTickCount64()` and a sequence number that got incremented after every logged keys are included. There are also some other complex fields, but they are too complex to reverse, so I checked back at `Wireshark` to see if I could figure something out.

## Parsing the keylog
I used my instinct to make a lot of assumptions in this part, so don't get confused about how can I figured them out, it was just my instinct.

Starting by looking at TCP stream 0, I could see a repetitive pattern in it: there are a lot of sequence starting with `\x0a\xXX\x08`. The sequences start at the fifth byte of the stream, so the first 4 bytes are most likely be the length of the stream, and that can be easily verified.

Now let's take a look at the first sequence: 
```
0a 14 08 00 10 c2 a6 b6 c3 03 18 00 22 08 ff ff fe ca aa fa fe ca
```
I could see there are two `0xcafe` bytes in this sequence, so this is likely the result from the XORing with `0xCAFEFAA` in the log of a mouse click. The first 3 bytes seem like a header of some sort. The fourth byte in these sequences gets incremented every sequence, starting from 0, so it must be the sequence number. The next 7 bytes are incremented a little bit after each sequence, so I assumed that they are the timestamp. For the next 3 bytes, I don't even know what they are. And finally the last 8 bytes are the encrypted X and Y coordinate of the cursor when the mouse is pressed. This way, I could already parse the mouse click sequences into sequence number, timestamp and coordinates:
```python
def parse(data):
	length = u32(data[0:4])
	data = data[4:]
	i = 0
	while i < length:
		if data[i:i+3] == b"\x0a\x14\x08":
			seq_num = data[i+3]
			timestamp = u64(data[i+4:i+11] + b"\0")
			point_x = u32(data[i+14:i+18]) ^ 0xCAFEFAAA
			point_y = u32(data[i+18:i+22]) ^ 0xCAFEFAAA
			print("{} \t {} \t Mouse x = {}, y = {}".format(seq_num, timestamp, point_x, point_y))
			i += 22
```
Let's take a look at a shorter sequence that comes later in the TCP stream:
```
0a 0e 08 02 10 9e fb b6 c3 03 18 02 22 02 df 29
```
Again, I assumed the first 3 bytes are header, the fourth byte is sequence number, the next 7 are timestamp, the next 3 is unknown. For the last 2, by trial and error, I knew that the first of them is the encoded key code, and the second is unknown and unimportant. The code to parse these sequences:
```python
	elif data[i:i+3] == b"\x0a\x0e\x08":
		seq_num = data[i+3]
		timestamp = u64(data[i+4:i+11] + b"\0")
		key_enc = data[i+14]
		if key_enc >= 0x96  and key_enc <= 0x9f:
			key = chr(key_enc - 0x66)
		elif key_enc >= 0xbb  and key_enc <= 0xe0:
			key = chr(key_enc + 0x7a - 0x100)
		elif key_enc == 0x86:
			key = " "
		else:
			key = "unknown"
		print("{} \t {} \t Key = {}".format(seq_num, timestamp, key))
		i += 16
```
By using these 2 functions to parse the streams that contain the keylog, it failed at some later sequences because their headers are different: `\x0a\x0f\x08` and `\x0a\x15\x08`. But it is actually quite simple: they are still the sequences for key presses and mouse clicks, but because the sequence number is greater than 255 then, they need one more byte to represent it. These two can be parsed using the following code:
```python
	elif data[i:i+3] == b"\x0a\x0f\x08":
		seq_num = u16(data[i+3:i+5]) - 0x100
		timestamp = u64(data[i+5:i+12] + b'\0')
		key_enc = data[i+15]
		if key_enc >= 0x96  and key_enc <= 0x9f:
			key = chr(key_enc - 0x66)
		elif key_enc >= 0xbb  and key_enc <= 0xe0:
			key = chr(key_enc + 0x7a - 0x100)
		elif key_enc == 0x86:
			key = " "
		else:
			key = "unknown"
		print("{} \t {} \t Key = {}".format(seq_num, timestamp, key))
		i += 17

	elif data[i:i+3] == b"\x0a\x15\x08":
		seq_num = u16(data[i+3:i+5]) - 0x100
		timestamp = u64(data[i+5:i+12] + b'\0')
		point_x = u32(data[i+15:i+19]) ^ 0xCAFEFAAA
		point_y = u32(data[i+19:i+23]) ^ 0xCAFEFAAA
		print("{} \t {} \t Mouse x = {}, y = {}".format(seq_num, timestamp, point_x, point_y))
		clicks.append((point_x, point_y))
		i += 23
```
Okay, then I could parse the key log:
```
0        6759538558943760        Mouse x = 1365, y = 0
1        6759538560579088        Mouse x = 646, y = 601
2        6759538564505104        Key = Y
3        6759538564573968        Key = O
4        6759538564634640        Key = U
5        6759538564788240        Key = T
6        6759538573237520        Key = U
7        6759538573363216        Key = B
8        6759538573431824        Key = E
9        6759538574540816        Key = Y
...
440      6759538946316560        Mouse x = 322, y = 181
441      6759538946603536        Mouse x = 385, y = 234
442      6759538946773776        Mouse x = 265, y = 79
443      6759538947125776        Mouse x = 373, y = 145
444      6759538947303952        Mouse x = 378, y = 118
445      6759538947587088        Mouse x = 436, y = 171
446      6759538947883024        Mouse x = 281, y = 111
447      6759538948105232        Mouse x = 346, y = 176
```
It seems that the dudes who were using this computer were just googling for some weird currency stuffs on the Internet, nothing seemed interesting to me yet. So I moved on to see what information I could gather from the last unknown part of the pcap: the big TCP stream number 10.

## Back to XblCloud.dll
Let's go back to the DLL file and find where the big stream got sent. First of, I went back to the function that log the keys to find where is the function that actually sends the stuffs. It can be easily recognized at `sub_180001910` because it makes a bunch of calls to some WSA networking function. I didn't analyze this function at all, instead, I cross-referenced it and found out that it's also called at `sub_180001DD0`. 

The lower part of this function is quite identical to the function that logs the keys, so it seemed like I went in the right direction. Scrolling up to the top of the function I found that it makes some calls to `keybd_event()` and some functions that interact with the clipboard. Some quick searches around the Microsoft docs again and I knew that this function generates a `PrtScr` key press to take a screenshot and retrieves it from the clipboard. The image is then encoded in the `jpeg` format, I knew this by googling these 2 constants `1284378190221622446i64` and `3383081795586128797i64` in `sub_1800016B0`. Therefore, the big TCP stream is a `jpeg` image of the screenshot that got encrypted in some way.

## Decrypting the screenshot
The encryption routine is clearly shown in `sub_180001DD0`, but because it is decompiled into some weird `m128i_i64` fields, it is quite hard to read. This is where my instinct comes into play again, let's look at this block of code:
```C
    v13 = v11;
    if ( v11 < v10 )
    {
      v14 = &img_buf[v11 / 0x10u];
      v15 = v10 - v13;
      v16 = *(img_buf->m128i_i64 + v13);
      do
      {
        LOBYTE(v14->m128i_i64[0]) = BYTE1(v14->m128i_i64[0]) ^ v16;
        v14 = (v14 + 1);
        --v15;
        v16 = v14->m128i_i64[0];
      }
      while ( v15 );
    }
```
A bunch of weird variables and fields are referenced here, but let's ignore them and get a closer look: 
```C
LOBYTE(v14->m128i_i64[0])  =  BYTE1(v14->m128i_i64[0])  ^ v16;
... 
v16 = v14->m128i_i64[0];
```
This looks like every bytes in the image gets XORed with its next byte, except the last one. So I wrote a script to decrypt this to see if my theory is correct:
```python
from malduck import *

data = bytearray(unhex(open("screenshot_enc.hex", "r").read().replace("\n", "")))

for i in  range(len(data) - 2, -1, -1):
	data[i] = data[i] ^ data[i+1]

open("screenshot.jpg", "wb").write(data)
```
It actually is, I found the string `JFIF` in the decrypted data, so then I just had to cut out the part that is the header of the stream and I had the screenshot that got sent over by the keylogger.

## Analyze the screenshot
The screenshot was taken and sent after the user searched for the google calculator app, and did something with the numbers, as we can see from the parsed keylog. Linking it with the description, this is actually the 4 thieves stealing some gold and then converted the value of the gold they stolen to VND and divided it by 4. 

At this point, because I saw the calculator and all the mouse clicks, I immediately thought of plotting all the mouse clicks onto the screenshot to find out what they did after calculating the money. All I found after that was disappointment, because the only thing that the "thieves" did after calculating the money was randomly clicking on the screen, then searched for `hero of the storm WTF` and watched some funny vids. It was a brainfart by me because I completely forgot about the `message.zip` file. It was even worse of a brainfart because I already thought of an On-screen keyboard shenanigans at this point, but somehow I couldn't link it with the password of the zip file.

## Finding the zip password
When I cleared the fog in my brain, I looked back at the start of the keylog: there were a lot of mouse clicks before they connected to `c.unsafesector.com`, and maybe this was where they typed the password. I used `OpenCV` to plot the clicks directly onto the screenshot, and I found out that they clicked the On-screen Keyboard icon on the icon tray at the bottom right of the screen, then clicks some keys. The idea then was to have my own keyboard on the screen and plot the clicks. Thanks to the screenshot, I knew the resolution of the targeted PC is `1366 x 768`. Therefore, I changed my own screen resolution to that, pop my own on-screen keyboard up (remember to use the OSK that comes with the icon on the tray, not the one that you can find by searching the system, they are different!). I took my screenshot and started to plot on it using `OpenCV` (the keyboard clicks happened at the 16th to 49th clicks):
```python
cnt = 1
for i in  range(16, 50):
	img = cv2.imread("./keyboard.png")
	cv2.circle(img, clicks[i], 6, (0,0,255), -1)
	cv2.imwrite("./imgs/tmp{}.jpg".format(cnt), img)
	cnt += 1
```
But because they also switched to the number keyboard in between and press some numbers, I have to take 2 screenshots and plot them separately:
```python
cnt = 1
for i in  range(16, 37):
	img = cv2.imread("./keyboard.png")
	cv2.circle(img, clicks[i], 6, (0,0,255), -1)
	cv2.imwrite("./imgs/tmp{}.jpg".format(cnt), img)
	cnt += 1

for i in  range(37, 50):
	img = cv2.imread("./keyboard2.png")
	cv2.circle(img, clicks[i], 6, (0,0,255), -1)
	cv2.imwrite("./imgs/tmp{}.jpg".format(cnt), img)
	cnt += 1
```
The password could be recovered as: `emergency password 641578642380`, but it still was incorrect. Therefore I asked the author of this challenge `@ks75vl` and he told me the there was actually one more key press before the first `e`, but I didn't found it (weird?), so I just used my instinct again and assume that it was a `Shift` key. So the correct password is: `Emergency password 641578642380`.

Using that password to extract the zip file, I got the txt file that contains the flag:
```
ISITDTU{___1m_back_Y0ur3_part_at_16_0599416__108_2075535___}
```
## Appendix
The script for parsing the keylog and plotting the clicks is `parse_key.py`.

The script for decrypting the screenshot is `decrypt_screenshot.py`.
