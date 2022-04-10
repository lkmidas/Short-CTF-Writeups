from idc import *
import idautils
import ida_allins
from malduck import *

start_ea = 0x140002D77

#nop_offset = [0x16836, 0x16837, 0x16e4d, 0x16e4e, 0x15e2a, 0x15e2b]
nop_offset = [0x16836, 0x16837, 0x16e4d, 0x16e4e]
#loop_offset = [0x16bb6]

#for patch in patch_offset:
#    ea = start_ea + patch*8 + 7
#    patch_byte(ea, 0x90)

#patch_byte(start_ea + 0x15e28*8 + 7, 0xeb)
#patch_byte(start_ea + 0x15e29*8 + 7, 0xfe)

patch_byte(start_ea + 0x16d98*8 + 7, 0xb0)
patch_byte(start_ea + 0x16d99*8 + 7, 0x01)
patch_byte(start_ea + 0x16d9a*8 + 7, 0xc3)

def nop(offset):
    ea = start_ea + offset*8 + 7
    patch_byte(ea, 0x90)

def inf_loop(offset):
    ea = start_ea + offset*8 + 7
    patch_byte(ea, 0xeb)
    patch_byte(ea+8, 0xfe)

for offset in nop_offset:
    nop(offset)

#for offset in loop_offset:
#    inf_loop(offset)

print("DONE")
