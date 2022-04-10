import struct

core_data = open("./core", "rb").read()

flag_buf = core_data[0x30a0 : 0x30a0+0x40]

# Flag 1 - search for flag buffer and simple xor
flag_buf = bytearray([flag_buf[i] ^ 0xa5 for i in range(len(flag_buf))])
print("Flag 1: {}".format(flag_buf.decode("utf-8")))

flag_xor_1 = (0xc4d2c981312f9749ead54bd51956632af4464465d7d4dc0dc0b819132401105c1991ab8c1674bbf6c46a704af4d838075136ebbbf60734f80083ed7e794313b).to_bytes(64, byteorder='little')
flag_buf = bytearray([flag_buf[i] ^ flag_xor_1[i] for i in range(len(flag_buf))])

# Flag 2 - search for otp file content on the heap and xor
flag_start = b"PCTF{"
otp_data_pattern = bytearray([flag_buf[i] ^ flag_start[i] for i in range(5)])
otp_data_addr = core_data[0x5000:].find(otp_data_pattern) + 0x5000 - 0x40 # 0x5000 is heap address offset
otp_data = core_data[otp_data_addr : otp_data_addr + 128]
flag_buf = bytearray([flag_buf[i] ^ otp_data[0x40 + i] for i in range(len(flag_buf))])
print("Flag 2: {}".format(flag_buf.decode("utf-8")))

flag_xor_2 = (0xbb73ad9a9992c6b62212646a9e04b61fa68305eb42fcb00c2d142fcaf5dca6b9f82c6ec691ca0b04f490b1c93df46711eb4def5ac740dcf6301641f2866c34b).to_bytes(64, byteorder='little')
flag_buf = bytearray([flag_buf[i] ^ flag_xor_2[i] for i in range(len(flag_buf))])
flag_buf = bytearray([flag_buf[i] ^ otp_data[i] for i in range(len(flag_buf))])

# Flag 3 - troll z3 equations, use info from the end of flag4 function instead
st7_reg = 8758372.44193981720582 # FPU stack is circular -> `fstp st0` at the end of flag4 saves st0 value into st7
xor_val = struct.pack("<d", st7_reg) * 8
flag_xor_3 = (0x6140948cf3453c97200ed5e2ef4a3f972002d5e2ec4a3f97230ed5e2ec4a3f972301dae2ec45309b2f01dae2ef4a3f97230ed5e2ec4530982f01d6f7c8701da9).to_bytes(64, byteorder='little')
flag_buf =  bytearray([xor_val[i] ^ flag_xor_3[i] for i in range(len(flag_buf))])
print("Flag 3: {}".format(flag_buf.decode("utf-8")))

# Flag 4 - bunch of FPU operations on parts of the flag, use info from st0 - st7 registers in gdb to reverse
flag_doubles = [
    1.96471717331242601289886806625873,
    1.94662990954210757287880240173905,
    1.96396555922453175412924208931287,
    1.96194592543749757275126088806871,
    1.96055999186344309670460006600479,
    1.96127523285948934805844601214631,
    1.96122205790569692496205789211672,
    1.93761962060497139326287197036436
] # results from b.c
flag_buf = b''.join([struct.pack("<d", flag_doubles[i])[:6] for i in range(len(flag_doubles))])
print("Flag 4: {}".format(flag_buf.decode("utf-8")))
