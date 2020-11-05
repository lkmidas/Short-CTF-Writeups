# ASCIS2020 QUALS: FINDME (RE)
- Given files: `findme.exe`.
- The given file is a normal Windows 32-bit PE file which reads in and checks a password.
## Analysis

### Step 1: Static analysis (IDA Pro)
First off, I started to analyze the file statically. By looking at the `main` function, it is clear that this program reads an input password, then pass it to the checking function using the **Remote procedure call** (RPC) protocol, I knew this because the program makes calls to `RpcStringBindingComposeA`, `RpcBindingFromStringBindingA` and `NdrClientCall2` (although at the time, I knew nothing about RPC). 

By reading the documentation from Microsoft about RPC and also doing some googling, I knew that this is a server - client protocol, and our program is acting as a client (RPC is always initiated by the client). Therefore, there must be a server running somewhere, but I couldn't find the part where the program initiates the server in `main`.

### Step 2: Getting the server dll (IDA Pro)
Initially, my suspect was that the server is initiated somewhere before `main`, in the `init` process of the PE. But I thought that looking into it would cost too much time, so I went the easier way, which is using the debugger attach option of IDA to list all the processes running in the system, and I found out that there was a dll running in the `%TEMP%` folder of Windows, and this probably was the server (I renamed it too `server.dll`).

### Step 3: Static analyzing the server (IDA Pro)
I opened up the dll in IDA, there is a lot of functions, and most of the calls are (maybe) obfuscated in the way that they are called indirectly by some pointers in the data segment. Again, the client passes the password to the server using `NdrClientCall2`, one of the parameter of that function is a *MIDL-generated procedure format string*, which indicates what function will be called in the server. I did some googling to try and understand this parameter, but I didn't find much information, so I just looked at all the functions in the server dll one by one, and the most interesting function is the first function `sub_401000`, which only takes in 1 parameter and passes it to a lot of bitwise equations and finally returns a boolean value, and that seems likely to be the password checking function. 

### Step 4: Solve the equations (z3)
So then, I simply wrote a python script to solve the equations using `z3`, the checking process is pretty simple: it checks if the length of the password is 16, and then do a series of calculations that form 16 equations. The script is as follow:
```
from z3 import BitVec, Solver

a = []
for i in range(16):
	a.append(BitVec('a' + str(i), 8))

s = Solver()

v1 = a[14]
v32 = a[12]
v31 = v1
v2 = a[15] ^ v1
v3 = a[13]
v4 = v3 ^ v2
v5 = a[6]
v6 = v32 ^ v3 ^ v2
v33 = a[10]
v35 = a[11]
v43 = a[9]
v44 = a[8]
v34 = a[5]
v42 = a[4]
v29 = v32 ^ v2
v40 = a[1]
v41 = a[0]
v38 = a[3]
v36 = a[2]
v24 = v43 ^ v40 ^ v36 ^ v32 ^ v2
v37 = a[7]
v25 = v43 ^ a[0] ^ v33 ^ v5 ^ v37 ^ v3 ^ v35
v26 = v44 ^ v42 ^ v40 ^ a[0] ^ v37 ^ v3 ^ v35
v30 = a[15] ^ v32
v39 = v3 ^ v32 ^ v35
v27 = v43 ^ v44 ^ a[0] ^ v36 ^ v37 ^ v3 ^ v2
v28 = v31 ^ v3 ^ v32 ^ v35 ^ v44 ^ v42 ^ a[0] ^ v33 ^ v36
s.add((v35 ^ (v43 ^ v34 ^ v40 ^ a[0] ^ v33 ^ v5 ^ v38 ^ v36 ^ v2)) == 117)
v8 = 0
s.add((v35 ^ (v43 ^ v44 ^ v34 ^ v42 ^ v40 ^ a[0] ^ v6)) == 49)
s.add((v44 ^ (v34 ^ v42 ^ v5 ^ v38 ^ v37 ^ v6)) == 82)
v10 = 0
s.add((v35 ^ (v43 ^ v44 ^ v34 ^ v40 ^ v41 ^ v33 ^ v4)) == 102)
v12 = a[6]
s.add((v35 ^ (v43 ^ v34 ^ v42 ^ v40 ^ v38 ^ v36 ^ v30)) == 115)
v13 = 0
s.add((v44 ^ (v42 ^ v41 ^ v12 ^ v38 ^ v36 ^ v29)) == 56)
s.add(v28 == 50)
s.add((v42 ^ (v33 ^ v12 ^ v38 ^ v36 ^ v39)) == 110)
v16 = 0
s.add(v27 == 7)
v17 = 0
s.add((v31 ^ (v32 ^ v35 ^ v42 ^ v41 ^ v33 ^ v12 ^ v36)) == 7)
s.add(v26 == 16)
v19 = 0
s.add((v43 ^ (v44 ^ v41 ^ v37 ^ v39)) == 29)
s.add(v25 == 7)
v21 = 0
s.add(((v43 ^ (v34 ^ v42 ^ v38 ^ v30)) == 25))
s.add(v24 == 78)
s.add((v31 ^ (v34 ^ v40 ^ v38 ^ v37)) == 48)

s.check()
ans = s.model()
result = ''
for i in range(16):
	result += chr(ans[a[i]].as_long())
print result
```
The password is ``HkX~^=`asfWY^&y<``. Simply enter it into the client and get the flag: `ASCIS{pl4y1ng_wi1h_RPC_i5_v3ry_4un}`

