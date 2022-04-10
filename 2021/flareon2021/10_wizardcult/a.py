from idc import *
import idautils
import ida_allins
from malduck import *

#table_ea = idaapi.get_name_ea(0, "wizardcult_tables_Ingredients")
def dump_table(table_name_ea):
    #table_name_ea = 0x942EC0
    table_ea = get_qword(table_name_ea)
    table_len = get_qword(table_name_ea + 8)
    table = {}

    for i in range(table_len):
        elem_ea = get_qword(table_ea)
        elem_len = get_qword(table_ea + 8)
        elem = idaapi.get_bytes(elem_ea, elem_len)
        table[elem] = i
        table_ea += 16

    print(table)

