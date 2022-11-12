# Chall9
- The program is an encryptor that encrypts `.EncryptMe` files using ChaCha20 with a random generated 32-byte key and 12-byte nonce
- It also appends 4 big num values to the end of the encrypted file (let's call them `val1`, `val2`, `val3`, `val4`)
- `val1` and `val3` are useless
- `val4` is the result of using big num `powmod` function on the key + nonce (just call `key` for short): `(key ^ unk_404020) % val2`
- `unk_404020` is generated at the beginning of the program, by taking a closer look and using a bit of intuition, it's actually the private key `d` in RSA, and `val2` is `n`
- We can see that `e` is hardcoded to be 0x10001, so we can simply do `(val4 ^ e) % val2` to get back the `key` (just like in RSA)
- Use the key to decrypt the given encrypted file with ChaCha20
