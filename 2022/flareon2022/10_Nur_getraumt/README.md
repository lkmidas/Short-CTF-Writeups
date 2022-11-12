# Chall10
- Set up Mini vMac by following its documentation
- Rename the given image to not containing unicode, then drag it into Mini vMac to mount
- Analyze the program with the given Super ResEdit
- Code is very simple: XOR a FLAG string in the program's resource with our input passphrase, then compare its CRC16 with another value in the resource to check
- The hint says something about "guessing" and "music in 1983", the resource is also named "99 Luftballons", turns out, the first line of the lyric is the correct passphrase (WTF is this challenge FLARE team???)
