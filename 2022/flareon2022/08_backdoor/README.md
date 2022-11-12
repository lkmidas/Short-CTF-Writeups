# Chall8
- Obfuscated .NET binary, all funcs with the name `flared_X()` are obfuscated to become garbage bytes, most funcs with the name `flare_X()` calls the obfuscated funcs in a `try ... catch` statement.
- `flare_74()` is not obfuscated and is called first to setup some lists, some dictionaries and a collection `FLARE15.c`
- `flare_70()`, `_66()`, `_69()`, `_47()`, `_67()`, `_35()` and `_68()` exception handlers call `flare_71()`, while all other functions' exception handlers call `flare_70()`
- `flare_71()` uses the lists and dictionaries created by `flare_74()` to generate C# bytecode and runs them using `dynamicMethod.Invoke()`
- However, before invoking the dynamic method, the type info of variables in the method is replaced by some kind of tokens. Therefore, if we patch the obfuscated funtions with the invoked code, the functions will still be wrong
- Instead, we can patch them by using the lists and dictionaries directly. This way, we can deobfuscate 70, 66, 69, 47, 67, 35, and 68
- All the functions mentioned above are called in the call tree of `flare_70()`, which handles the deobfuscation of other `flared` functions
- `flared_70()` gets the `metadataToken` of the obfuscated function the needs to be decrypted, runs it through a series of hashing and encrypting algorithm to generate the deobfuscated code
- We can symply set a breakpoint at the beginning of `flared_70()`, then change the `metadataToken` to any function we want when the program hits that breakpoint. We also set a breakpoint at the end of `flared_70()` to dump out the code. This way, we can slowly but surely deobfuscate the whole binary
- The program implements a backdoor in a state machine fashion: first it will generate a number called `flare.agent.id`, then use this value to generate the name of various sub-domains under `flare-on.com` and connect to them. The server is expected to send numbers as command to this backdoor and the backdoor will execute shell commands correspondingly
- To debug the program, we set breakpoints at where it connects to the servers, then set `localhost`'s domain name to the domain names that we can see in the debugger. We also need to set a breakpoint and change the first byte of the IP address in the process memory to be greater than 127 to pass a check (`localhost` is `127.0.0.1`)
- The logic that we are interested in is `flared_56()`: this is where the commands from the server is processed, but they will only be processed if they are passed in the correct order. This order is determined by a simple XOR and the `FLARE15.c` collection created at the beginning of the program
- For each command from the server in the correct order, it will add a bit of hex string to `FLARE14.sh`. The corresponding shell command executed by the backdoor will be added to the result of `flared_57()` and append to `FLARE14.h`, which is a SHA-256 hash function
- `flared_57()` simply adds the 2 prototypes of the 2 nearests methods in the stack trace. This is to place a trap on deobfuscated code, since we need to run this function when it's still obfuscated to get the correct stack trace 
- Note: There is a mismatch between the prototype of `InvokeMethod` in the system .NET libs and the dnSpy's .NET libs that can make the result of `flared_57()` incorrect. Manually debug to get the correct prototype instead of just calling it in interactive C#
- When the collection `FLARE15.c` is finally emptied, it will call `flared_54()` to begin decrypting a file using `FLARE14.sh` and `FLARE14.h`
- Write a C# interactive script to call the functions in `flared_56()` in the correct order as the program expected from the server, and then call `flared_54()` to decrypt the flag file

