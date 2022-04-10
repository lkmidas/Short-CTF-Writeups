from idc import *
import idautils
import ida_allins
from malduck import *

start_ea = 0x140002D77
ea = start_ea
insn = idaapi.insn_t()
data = b""

while ea != 0x1401796DF:
    idaapi.decode_insn(insn, ea)
    if insn.itype == ida_allins.NN_mov:
        data += p8(get_operand_value(ea, 1) & 0xff)
    else:
        print("NOT MOV")
    ea = next_head(ea) 

open("dump.bin", "wb").write(data)
print("DONE")
