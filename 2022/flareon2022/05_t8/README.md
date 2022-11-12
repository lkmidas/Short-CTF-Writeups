# Chall5
- Program logic:
    - Use md5 to hash a string containing `FO9` concatenated with a random `uint16` number
    - Use it as RC4 key to encrypt the string `"ahoy"`, then base64 encdode it
    - Send it to `flare-on.com` and receive response
    - Decode the response with base64, do some magic to it
    - Use MD5 to hash the result and use it as RC4 key again for something else, base64 encode it and send
    - Second response from the server is a shellcode

- Analyze the PCAP file to get the first sent package
- Use it to brute force the `uint16` number
- Use python Flask to set up our own server in localhost, rename localhost domain to `flare-on.com`
- Make our server return the same packet as we see in the PCAP
- Run the program with the calculated `uint16` number -> the flag will be the string used for MD5 the second time
- Set a breakpoint there to read it
