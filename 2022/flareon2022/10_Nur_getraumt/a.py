from malduck import xor

enc = b"\x0c\x00\x1d\x1a\x7f\x17\x1c\x4e\x02\x11\x28\x08\x10\x48\x05\x00\x00\x1a\x7f\x2a\xf6\x17\x44\x32\x0f\xfc\x1a\x60\x2c\x08\x10\x1c\x60\x02\x19\x41\x17\x11\x5a\x0e\x1d\x0e\x39\x0a\x04"
passphrase = b"Hast du etwas Zeit f\xfc\x00r mich"

print(xor(passphrase, enc))
