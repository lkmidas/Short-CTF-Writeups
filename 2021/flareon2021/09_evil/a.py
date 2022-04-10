from idc import *
import idautils
import ida_allins
from malduck import *

def patch_api_resolve(ea):
    func_ea = idaapi.get_name_ea(0, "resolve_API")
    offset = func_ea - ea - 5
    call_insn = b"\xe8" + p32(offset) + b"\xff\xd0"
    idaapi.patch_bytes(ea, call_insn)
    patch_byte(ea - 2, 0x55)
    patch_byte(ea - 5, 0x4d)