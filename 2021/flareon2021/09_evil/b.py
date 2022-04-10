import socket
from malduck import *

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
sock.setsockopt(socket.IPPROTO_IP, socket.IPV6_DONTFRAG, 1)

def send(option, data):
    payload = p32(option) # option
    payload += p32(len(data)+1)
    payload += data
    sock.sendto(payload, ("127.0.0.1", 4356))

send(2, b"L0ve")
send(2, b"s3cret")
send(2, b"5Ex")
send(2, b"g0d")

send(3, b"MZ")

x = sock.recvfrom(0xFFFF)

print(x)
