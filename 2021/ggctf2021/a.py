from malduck import unhex
from z3 import *
import sys
sys.setrecursionlimit(10**9)

mem = [b for b in unhex("2535324325730025332E31684D25332E306C45252B312E336C4D25312E346C6C5325332E316C4D25332E326C4F252D372E33430025302E3430393668684D25302E3235356C6C4925312E306C4D25312E386C6C4C25302E316C5525312E306C4D25312E31366C6C4C25302E316C5525312E3230306C6C4D25322E313738386C6C4D253743252D363134342E313730313733363330326C6C4D25302E32303068684D25302E3235356C6C4925302E33376C6C4F25303230302E3043000000000000000000000000000071607A6164646438381971647A6567666464383819716767631771647A64383819716164641771656662661771646261677A64175471657A643838195471677A64381971677A66381A71646661677A671771667A6538380771677A66381971677A67380C71677A64381B71677A6538381B71796662657A671754717F607A64381971607A663838075471657A6538381971667A663838197166626517717F6766667A651771647A6538380771657A656762646438381971657A64381B717F6767637A65175471647A643838195471647A663838025471647A6738380C71647A653838075471657A64381971657A6638381A71646064617A6517717F6065677A6517716063641771647A653838075471657A64381971657A6538381B7164676D637A6517717F60666C7A65175471667A64381971667A60646D6238380771607A663C1971607A66616138381D717F6160647A60175471667A64381971667A6638380C71667A6164646438380771667A663C1971667A66616138381D71607A66381171647A6538380771667A643819716063641771607A64380771607A66616138381D71647A66381971667A6538381B71667A60616464383807717F667A60381971616464175471647A656667606162636C6D38381971657A6438381971657A60646D6238380771657A653C1971647A65381171667A6438381971667A6C6062636C626C656C38380771667A64381171657A6438381971657A62656060383807717F657A66381971657A6038381971657A60646D6238380771657A653C1971647A65381171667A6438381971667A6560606761676C63616D38380771667A64381171657A6038381971657A62656060383807717F657A66381971657A6C38381971657A60646D6238380771657A653C1971647A65381171667A6438381971667A6564606361656161656438380771667A64381171657A6C38381971657A62656060383807717F657A66381971657A656638381971657A60646D6238380771657A653C1971647A65381171667A6438381971667A67616D606D6D61656038380771667A656366606062656C616238380771667A64381171657A656638381971657A62656060383807717F657A66381971657A656238381971657A60646D6238380771657A653C1971647A65381171667A6438381971667A66606564666064676138380771667A64381171657A656238381971657A62656060383807717F657A66381971657A666438381971657A60646D6238380771657A653C1971647A65381171667A6438381971667A66666666626363666038380771667A64381171657A666438381971657A62656060383807717F657A66381971657A666038381971657A60646D6238380771657A653C1971647A65381171667A6438381971667A6C6060646D6264656C38380771667A64381171657A666038381971657A62656060383807717F657A6638195471647A6438381971657A6438381971657A6061646438380771657A653C1971667A6438381971667A6567636061606662666138380771667A65626C626D656163666438380771667A6565666D626C626C626438380771657A66381171647A65380171657A6038381971657A6061646438380771657A653C1971667A6438381971667A6C606666656364666D38380771667A65606C676D646661626038380771657A66381171647A65380171657A6C38381971657A6061646438380771657A653C1971667A6438381971667A656C626C64656763676538380771657A66381171647A65380171657A656638381971657A6061646438380771657A653C1971667A6438381971667A616C60626D6063676638380771667A6560616767656663646438380771657A66381171647A65380171657A656238381971657A6061646438380771657A653C1971667A6438381971667A66666761606C63606038380771657A66381171647A65380171657A666438381971657A6061646438380771657A653C1971667A6438381971667A656D616C6C6C6763666238380771667A656D656264646C646D6D38380771657A66381171647A65380171657A666038381971657A6061646438380771657A653C1971667A6438381971667A656C666D6D676362646138380771667A656C6561676162646C6238380771667A6661676C6762626D6C38380771657A66381171647A65380154")]
mem += [0] * (4096 - len(mem)) # padding
mem += [ord('T')] + [104, 101, 78, 101, 119, 70, 108, 97, 103, 72, 105, 108, 108, 115, 66, 121, 84, 104, 101, 67, 116, 102, 87, 111, 111, 100, 115] + [0] * 0x1000 # input

regs = [0] * 32 * 8

LEN = 28
s = Solver()
v = [0] * LEN



def store32(where, addr, val):
    where[addr] = val & 0xff
    where[addr+1] = (val >> 8) & 0xff
    where[addr+2] = (val >> 16) & 0xff
    where[addr+3] = (val >> 24) & 0xff

def load32(where, addr):
    return where[addr] + (where[addr+1] << 8) + (where[addr+2] << 16) + (where[addr+3] << 24)

def parse_fmt(fmt):
    fmt = fmt[1:]
    
    typ = None
    prec = -1
    width = 0
    pad = ord(' ')
    left = False
    showsign = False
    L = False
    h = False
    l = False
    hh = False
    
    if fmt[0] == "+":
        showsign = True
        fmt = fmt[1:]

    elif fmt[0] == "-":
        left = True
        fmt = fmt[1:]

    if fmt[0] == "0":
        pad = ord("0")

    if "hh" in fmt:
        hh = True
    elif "h" in fmt:
        h = True
    elif ("ll" in fmt) or ("L" in fmt):
        L = True
    elif "l" in fmt:
        l = True

    typ = fmt[-1]

    if "." in fmt:
        fmt1, fmt2 = fmt.split('.')
        if len(fmt1) > 0:
            width = int(fmt1)
        while not fmt2[-1].isdigit():
            fmt2 = fmt2[:-1]
        prec = int(fmt2)
    else:
        while not fmt[-1].isdigit():
            fmt = fmt[:-1]
        width = int(fmt)

    return (typ, prec, width, pad, left, showsign, l, h, L, hh)


def exec_calc(typ, prec, width, pad, left, showsign, l, h, L, hh, solve):
    addr = 0
    where = 0
    val = 0
    dbg_cmd = ""
    dbg_where = ""
    dbg_addr = ""
    dbg_val = ""

    if left:
        addr = width
        where = mem
        dbg_where = "MEM"
        dbg_addr = str(addr)
    elif showsign:
        addr = load32(regs, width*8)
        where = mem
        dbg_where = "MEM"
        dbg_addr = "REGS[{}]".format(str(width))
    else:
        addr = width*8
        where = regs
        dbg_where = "REGS"
        dbg_addr = str(width)

    if hh:
        val = load32(mem, prec)
        dbg_val = "MEM[{}]".format(prec)
    elif h:
        val = load32(mem, load32(regs, prec*8))
        dbg_val = "MEM[REGS[{}]]".format(prec)
    elif L:
        val = prec
        dbg_val = str(prec)
    elif l:
        val = load32(regs, prec*8)
        dbg_val = "REGS[{}]".format(prec)

    left = load32(where, addr)
    right = val

    if typ == "M":
        val = val
        dbg_cmd = "LOAD"
    elif typ == "S":
        val = (load32(where, addr) + val) & 0xffffffff
        dbg_cmd = "ADD"
    elif typ == "O":
        val = (load32(where, addr) - val) & 0xffffffff
        dbg_cmd = "SUB"
    elif typ == "X":
        val = (load32(where, addr) * val) & 0xffffffff
        dbg_cmd = "MULT"
    elif typ == "V":
        val = load32(where, addr) // val
        dbg_cmd = "DIV"
    elif typ == "N":
        val = load32(where, addr) % val
        dbg_cmd = "MOD"
    elif typ == "L":
        val = (load32(where, addr) << val) & 0xffffffff
        dbg_cmd = "LSHIFT"
    elif typ == "R":
        val = (load32(where, addr) >> val) & 0xffffffff
        dbg_cmd = "RSHIFT"
    elif typ == "E":
        val = load32(where, addr) ^ val
        dbg_cmd = "XOR"
    elif typ == "I":
        val = load32(where, addr) & val
        dbg_cmd = "AND"
    elif typ == "U":
        val = load32(where, addr) | val
        dbg_cmd = "OR"
    else:
        print("UNKNOWN TYPE", typ)
        sys.exit(-1)

    store32(where, addr, val)
    
    if not solve:
        print("{} {}[{}], {}".format(dbg_cmd, dbg_where, dbg_addr, dbg_val).ljust(30, " "), end="")
        print("# addr = {}, val_1 = {}, val_2 = {}, result = {}".format(hex(addr), hex(left), hex(right), hex(val)))


def exec_call(typ, prec, width, pad, left, showsign, l, h, L, hh, solve):

    if typ != "C":
        print("UNKNOWN TYPE", typ)
        sys.exit(-1)
    
    cmp_flag = True
    dbg_cmd = ""
    dbg_reg = prec
    dbg_addr = width

    # Hackish way to trap z3
    try:

        if left:
            cmp_flag = load32(regs, prec*8) > 0x7fffffff
            dbg_cmd = "CLZ"
        elif showsign:
            cmp_flag = (load32(regs, prec*8) < 0x80000000) and (load32(regs, prec*8) > 0)
            dbg_cmd = "CGZ"
        elif pad == ord('0'):
            cmp_flag = load32(regs, prec*8) == 0
            dbg_cmd = "CEZ"
        else:
            cmp_flag = True
            dbg_cmd = "CALL"
    
    except Z3Exception: # we want the comparison with z3 values to always true
        execute(width, solve)
        return

    if not solve:
        print("{} REGS[{}], {}".format(dbg_cmd, dbg_reg, dbg_addr).ljust(30, " "), end="")
        print("# val = {}, cmp_flag = {}".format(load32(regs, prec*8), cmp_flag))

    if cmp_flag:
        execute(width, solve)



def execute(init_pc, solve=False):
    global regs, mem, s, v, first
    pc = init_pc
    while True:
        
        if solve:
            if pc == 200: # start of the main code
                for i in range(1, LEN):
                    v[i] = BitVec("INPUT{}".format(i), 32)
                    s.add(And(v[i] >= 0x20, v[i] <= 0x7f))
                    mem[4096 + i] = v[i]


            if pc == 244: # check address
                s.add(load32(regs, 0) == 0)
                break

        try:
            next_pc = mem[pc+1:].index(ord("%")) + 1 + pc
            fmt = ''.join([chr(b) for b in mem[pc:next_pc]])
            null = mem[pc+1:].index(ord("\0")) + 1 + pc
        except: # At the end no more %
            null = mem[pc+1:].index(ord("\0")) + 1 + pc
            fmt = ''.join([chr(b) for b in mem[pc:null]])
            next_pc = null + 1

        fmt = fmt.strip('\0')

        if not solve:
            print("{}".format(pc).ljust(10, " "), end="")
            print("{}".format(fmt).ljust(30, " "), end="")
        
        pc = next_pc
        typ, prec, width, pad, left, showsign, l, h, L, hh = parse_fmt(fmt)
        if typ == "C":
            exec_call(typ, prec, width, pad, left, showsign, l, h, L, hh, solve)
        else:
            exec_calc(typ, prec, width, pad, left, showsign, l, h, L, hh, solve)

        if (next_pc - 1 >= null):
            if not solve:
                print("{}".format(null).ljust(10) + "RET")
            break




def disass_calc(typ, prec, width, pad, left, showsign, l, h, L, hh):
    addr = 0
    where = 0
    val = 0
    dbg_cmd = ""
    dbg_where = ""
    dbg_addr = ""
    dbg_val = ""

    if left:
        dbg_where = "MEM"
        dbg_addr = str(width)
    elif showsign:
        dbg_where = "MEM"
        dbg_addr = "REGS[{}]".format(str(width))
    else:
        dbg_where = "REGS"
        dbg_addr = str(width)

    if hh:
        dbg_val = "MEM[{}]".format(prec)
    elif h:
        dbg_val = "MEM[REGS[{}]]".format(prec)
    elif L:
        dbg_val = str(prec)
    elif l:
        dbg_val = "REGS[{}]".format(prec)

    if typ == "M":
        dbg_cmd = "LOAD"
    elif typ == "S":
        dbg_cmd = "ADD"
    elif typ == "O":
        dbg_cmd = "SUB"
    elif typ == "X":
        dbg_cmd = "MULT"
    elif typ == "V":
        dbg_cmd = "DIV"
    elif typ == "N":
        dbg_cmd = "MOD"
    elif typ == "L":
        dbg_cmd = "LSHIFT"
    elif typ == "R":
        dbg_cmd = "RSHIFT"
    elif typ == "E":
        dbg_cmd = "XOR"
    elif typ == "I":
        dbg_cmd = "AND"
    elif typ == "U":
        dbg_cmd = "OR"
    else:
        print("UNKNOWN TYPE", typ)
        sys.exit(-1)

    print("{} {}[{}], {}".format(dbg_cmd, dbg_where, dbg_addr, dbg_val).ljust(30, " "))


def disass_call(typ, prec, width, pad, left, showsign, l, h, L, hh):

    if typ != "C":
        print("UNKNOWN TYPE", typ)
        sys.exit(-1)
    
    cmp_flag = True
    dbg_cmd = ""
    dbg_reg = prec
    dbg_addr = width

    if left:
        dbg_cmd = "CLZ"
    elif showsign:
        dbg_cmd = "CGZ"
    elif pad == ord('0'):
        dbg_cmd = "CEZ"
    else:
        dbg_cmd = "CALL"

    print("{} REGS[{}], {}".format(dbg_cmd, dbg_reg, dbg_addr).ljust(30, " "))


def disass(init_pc):
    global regs, mem
    pc = init_pc
    while True:
        try:
            next_pc = mem[pc+1:].index(ord("%")) + 1 + pc
            fmt = ''.join([chr(b) for b in mem[pc:next_pc]])
            null = mem[pc+1:].index(ord("\0")) + 1 + pc
        except: # At the end no more %
            null = mem[pc+1:].index(ord("\0")) + 1 + pc
            fmt = ''.join([chr(b) for b in mem[pc:null]])
            next_pc = null + 1

        fmt = fmt.strip('\0')
        if (len(fmt) == 0) or (fmt[0] != "%"):
            break

        print("{}".format(pc).ljust(10, " "), end="")
        print("{}".format(fmt).ljust(30, " "), end="")
        
        pc = next_pc
        typ, prec, width, pad, left, showsign, l, h, L, hh = parse_fmt(fmt)
        if typ == "C":
            disass_call(typ, prec, width, pad, left, showsign, l, h, L, hh)
        else:
            disass_calc(typ, prec, width, pad, left, showsign, l, h, L, hh)

        if next_pc - 1 >= null:
            print("{}".format(null).ljust(10) + "RET\n")
    
        



execute(52, True)
#execute(52)
#disass(200)


sol_count = 0
solutions = []

print("Checking")

while sol_count < 5 and s.check() == sat:
    model = s.model()
    result = [model[v[i]].as_long() for i in range(1, LEN)]
    print(result)
    print('T' + ''.join([chr(x) for x in result]))
    solutions.append(result)
    sol_count += 1

    print("sol_count=", sol_count)

    cond = True
    for i in range(1, LEN):
        cond = And(cond, v[i] == result[i-1])

    s.add(Not(cond))
