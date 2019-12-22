
# JUSTCTF2019: ATM SERVICE (pwn)
## First look
- Given files: `atm`, `libc.so.6`.
- Given libc's version is 2.27.
## Analysis
**(1)** The program has 3 functionalities: save a request, send a request and print a request (there is also a useless debugging functionality).

**(2)** User can only save up to 5 requests.

**(3)** The print request functionality only prints out the pin if the pin of the current request is not set.

**(4)** The data of a request is stored in the heap, but it is also very large so a region near libc will be mmapped.

**(5)** In the save request functionality, the bound of the pin's index is not checked, leads to an arbitrary read and also a 4 bytes `****` write to its location.

**(6)** In the send request functionality, you can pass a long string to `inet_aton()` using a hex number, then it will use `memcpy()` to copy a C string, but it's size is taken using C++ `size()`, this leads to a stack overflow if we insert a null byte.

**(7)** The offset to libc and to `tls` from the mmaped region may be different on the server and locally.
## Exploit plan
**Step 0:** To get correct offsets in later steps, you can either brute force the server for offset or build a `ubuntu:18.04` docker image yourself and exploit using that docker.

**Step 1:** Save a request with the pin's index at a memory cell where libc's address is located, note that we can only leak 4 bytes at a time, so we will leak the 2nd to 5th bytes of the address `0x007fxxyyzzttuu` (this means we leak `xxyyzztt` because `uu` is constant).

**Step 2:** Save a request without pin, then print request to get a libc leak.

**Step 3:** Save 2 requests with the pin's index at the lower 4 bytes and upper 4 bytes of the memory cell contains global canary in `tls`, overwrite it with `****`. Also, in the 2nd request, setup a long pin contains the canary as `********` and `one_gadget` to overflow the stack.

**Step 4:** Send the request, overwrite `send_req()`'s return address with `one_gadget` and get shell.

## Full exploit
See `solve.py`.
