# SECCON2018: INTERNET_OF_SEAT (pwn)
## First look
- Given files: `initramfs.cpio.gz`, `main`, `wrapper.py`, `xinetd.conf`, `zImage`.
- We need to exploit an `httpd` of an ARM IoT device.
- For some reason, `main` is a MIPS file with just a few functions (???).
- Have to extract the file system to get the real `httpd`.
## Setup, analysis, debugging
- Use `binwalk -e` 2 times to extract `initramfs.cpio.gz` and get the real `httpd`.
- To rebuild the challenge's service:
```
stdbuf -i0 -o0 -e0 socat TCP-LISTEN:1337,reuseaddr,fork EXEC:"/path/to/internet_of_seat/wrapper.py"
```
- Can debug with `qemu-arm-static` and `gdb-multiarch` (a bit unreliable, but got the job done):
```
cd cpio-root
sudo cp /usr/bin/qemu-arm-static ./bin
sudo chroot . /bin/qemu-arm-static -g 1234 /sbin/httpd
```
## Vulnearability
**(0)** All data segments are RWX.

**(1)** Data are being dealt with incorrectly in `process_chunked()` (`r->chunk + r->chunk_off` in `memcpy` is buggy), a big header will cause overflow because `r->chunk_off` will become very large:

```
realloc(r->chunk, r->chunk_size);
...
memcpy(r->chunk + r->chunk_off, r->buf + content_off, content_len);
```

**(2)** The binary uses `uClibc`, so the initial heap arena is stored inlined in libc with a static size of 0x100 and a pointer to a `struct heap_free_area *__malloc_heap` at the end that stores the size of the arena and pointers to prev and next arenas, which can be overwrited to allocate arbitrary pointers (pretty similar to `house of force`).

**(3)** On the qemu server, we get qemu's debug messages.
## Exploit plan
**Step 1:** Send a normal request, get heap address thanks to (3).

**Step 2:** Send a header with chunked encoding and enough size to setup a overflow thanks to (1).

**Step 3:** Send the payload chunk to do the overwrite, we will get a big arena that can allocate arbitrary pointer.

**Step 4:** Send a big chunk with shellcode and overwrite GOT to shellcode address. Shellcode is nops + dup2s + execve.
## Full exploit
See `solve.py` (well-commented).
