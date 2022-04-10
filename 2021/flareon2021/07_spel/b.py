from idc import *
import idautils
import ida_allins
from malduck import *

def decrypt_string(ea, key):
    data = b""
    insn = idaapi.insn_t()
    while True:
        idaapi.decode_insn(insn, ea)
        if insn.itype == ida_allins.NN_mov:
            if get_operand_type(ea, 0) == o_displ:
                data += p32((get_operand_value(ea, 1) & 0xffffffff) ^ key)
            else:
                break
        else:
            break
        ea = next_head(ea) 
    print(data)
