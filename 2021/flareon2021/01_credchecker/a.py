from base64 import b64decode, b64encode
from malduck import xor

key = b64decode(b"P1xNFigYIh0BGAofD1o5RSlXeRU2JiQQSSgCRAJdOw==")
password = b64encode(b"goldenticket")

print(xor(password, key))