
# TETCTF2020: SMALLSERVICE (pwn)
- Given files: `smallservice`, `client.py`.
- The binary has: `Partial RELRO`, `Canary found`, `NX enabled` and `No PIE`.
## Functionalities
- This program implements a small service which has the following functionalities: request a user, login, ping an IP and change password. We won't go deep into all of them because only 1 functionality is used to pwn this challenge.
- The `client.py` file gives us a nice and easy way to send payloads and communicate with the service.
- In `ping`, the program will first authenticate your user, if it is valid, then it will make a call to `inet_aton()` on the IP address and use `system()` to ping it.
## Vulnearabilities
**(1)** In `ping`, when authenticating with the `auth()` function, it will always return 1 or 2, which is both true, so you don't even need to be logged in as a valid user to ping.

**(2)** The `inet_aton()` function will return true as long as there is a valid IP address at the start of the string separated with the rest by a whitespace, so `127.0.0.1 ;/bin/sh;` is a valid IP address.

**(3)** The IP address will then be passed in to `system()` which will get us a shell.

## Exploit plan

**Step 1:** Edit the `client.py` file: changes the `self.r.recvuntil("\n\n\n")[:-3]` to one `self.r.recvline().strip()` and two `self.r.recvline()`s, or it won't work correctly.

**Step 2:** In `ping(self, host)`, replace `self.privatekey` with any string.

**Step 3:** Call `cl.ping("127.0.0.1 ;/bin/sh;")` and get shell.

## Full exploit
See `solve.py`.

