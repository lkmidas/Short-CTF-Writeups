from malduck import *
import pygob

table = {b'bone': 0, b'undead eyeball': 1, b'spider': 2, b'fish tail': 3, b'adamantine': 4, b'tentacle of giant octopus or giant squid': 5, b'ice': 6, b'coal': 7, b'food morsel': 8, b'bitumen (a drop)': 9, b'giant slug bile': 10, b'jade dust': 11, b'rotten egg': 12, b'silver powder': 13, b'artistic representation of caster': 14, b'oils and unguents': 15, b'soil mixture in a small bag': 16, b'gem-encrusted bowl': 17, b'magic item': 18, b'makeup': 19, b'talcum powder': 20, b'black silk square': 21, b'licorice root shaving': 22, b'tears': 23, b'salt': 24, b'dirt': 25, b'silver mirror': 26, b'wire of fine silver': 27, b'parchment with holy word written upon it': 28, b'gauze': 29, b'bone dust': 30, b'dust': 31, b'quartz': 32, b'lodestone': 33, b'sponge': 34, b'rope': 35, b'shamrock': 36, b'firefly': 37, b'iron': 38, b'soot': 39, b'forked twig': 40, b'distilled spirits': 41, b'mercury': 42, b'opaque glass': 43, b'marked sticks or bones': 44, b'ink': 45, b'niter': 46, b'corn': 47, b'hot pepper': 48, b'pebble': 49, b'stone': 50, b'wychwood': 51, b'miniature hand sculpted from clay': 52, b'amber': 53, b'brimstone': 54, b'pickled tentacle': 55, b'jade circlet': 56, b'sacrificial offering appropriate to deity': 57, b'fur of bloodhound': 58, b'jeweled horn': 59, b'lime': 60, b'vessel to contain a medium-sized creature': 61, b'cloth wad': 62, b'stem of a thorny plant': 63, b'pitch': 64, b'chalks and inks infused with precious gems': 65, b'tallow': 66, b'silk square': 67, b'earth': 68, b'molasses (a drop)': 69, b'feldspar': 70, b'jewel': 71, b'mandrake root': 72, b'focus': 73, b'eyeball': 74, b'silver bar': 75, b'fur': 76, b'glass sliver': 77, b'ivory portal (miniature)': 78, b'crystal bead': 79, b'ash': 80, b'sand': 81, b'feather of owl': 82, b'tuft of fur': 83, b'ink lead-based': 84, b"feather from any bird's wing": 85, b'mistletoe': 86, b'chrysolite powder': 87, b'lead': 88, b'phosphorescent moss': 89, b'blood': 90, b'quiver': 91, b'ointment for the eyes': 92, b'butter': 93, b'wisp of smoke': 94, b'magnifying glass': 95, b'incense': 96, b'honeycomb': 97, b'spiderweb': 98, b'snaketongue': 99, b'humanoid blood': 100, b'herbs': 101, b'string': 102, b'rose petals': 103, b'gilded skull': 104, b'pearl': 105, b'obsidian': 106, b'sweet oil': 107, b'twig from a tree that has been struck by lightning': 108, b'phosphorus': 109, b'polished marble stone': 110, b'gold-inlaid vial': 111, b'gum arabic': 112, b'twig': 113, b'silver rod': 114, b'fur of bat': 115, b'mistletoe sprig': 116, b'an item distasteful to the target': 117, b'moonseeds': 118, b'iron blade': 119, b'rock chip': 120, b'sumac leaf': 121, b'fleece': 122, b'sunstone': 123, b'granite': 124, b'quill plucked from a sleeping bird': 125, b'diamond': 126, b'bell (tiny)': 127, b'thorns': 128, b'silver spoon': 129, b'tarts': 130, b"adder's stomach": 131, b'reed': 132, b'jewel-encrusted dagger': 133, b'caterpillar cocoon': 134, b'clay pot of grave dirt': 135, b'gem as powder': 136, b'iron filings or powder': 137, b'flesh': 138, b'tiny piece of target matter': 139, b'ammunition': 140, b'clay and water': 141, b'sulfur': 142, b'black pearl (as crushed powder)': 143, b'ruby (as dust)': 144, b'gilded acorn': 145, b'leather loop': 146, b'cloak': 147, b'spheres of glass': 148, b'cured leather': 149, b'snakeskin glove': 150, b'alum soaked in vinegar': 151, b'cork': 152, b'crystal sphere': 153, b'flame': 154, b'eggshells': 155, b'silver cage': 156, b'prayer wheel': 157, b'copper piece': 158, b'crystal vial of phosphorescent material': 159, b'feather of hummingbird': 160, b"red dragon's scale": 161, b'forked metal rod': 162, b'snow': 163, b'eggshell': 164, b'engraving of symbol of the outer planes': 165, b'black onyx stone': 166, b'petrified eye of newt': 167, b'silver whistle': 168, b'charcoal': 169, b'hand mirror': 170, b'lockbox of ornate stone and metal': 171, b'glass eye': 172, b'silver and iron': 173, b'glass or crystal bead': 174, b'rotten food': 175, b'clay model of a ziggurat': 176, b'diamond and opal': 177, b'skunk cabbage leaves': 178, b'ashes of mistletoe and spruce': 179, b'nut shells': 180, b'statue of the caster': 181, b'exquisite chest': 182, b'clay': 183, b'thread': 184, b"hen's heart": 185, b'knotted string': 186, b'rhubarb leaf': 187, b'sesame seeds': 188, b'ruby': 189, b"grasshopper's hind leg": 190, b'ivory strips': 191, b'paper or leaf funnel': 192, b'oak bark': 193, b'crystal or glass cone': 194, b'water': 195, b'agate': 196, b'holy water': 197, b'mica chip': 198, b'weapon': 199, b'club': 200, b'bull hairs': 201, b'reliquary containing a sacred relic': 202, b'crystal hemisphere': 203, b'holly berry': 204, b'divinatory tools': 205, b'yew leaf': 206, b'gum arabic hemisphere': 207, b'eyelash in gum arabic': 208, b'leather strap': 209, b'silver pins': 210, b'platinum sword': 211, b'legume seed': 212, b'detritus from the target creature': 213, b'copper wire': 214, b'gilded flower': 215, b'guano': 216, b'artistic representation of target': 217, b'flea (living)': 218, b'cricket': 219, b'oil': 220, b'parchment as a twisted loop': 221, b'glowworm': 222, b'golden reliquary': 223, b'umber hulk blood': 224, b'jacinth': 225, b'holy symbol': 226, b'graveyard dirt (just a pinch)': 227, b'wood': 228, b'fur wrapped in cloth': 229, b'honey drop': 230, b'platinum-inlaid vial': 231, b'fan': 232, b'straw': 233, b'sapphire': 234, b'sunburst pendant': 235, b'green plant': 236, b'golden wire': 237, b'clay pot of brackish water': 238, b'platinum rings': 239, b'air': 240, b'colored sand ': 241, b'gem or other ornamental container': 242, b'sugar': 243, b'holy/unholy water': 244, b'gold dust': 245, b'copper pieces': 246, b'pork rind or other fat': 247, b'silver rings': 248, b'pickled octopus tentacle': 249, b'gem': 250, b'dried carrot': 251, b'melee weapon': 252, b'feather': 253, b'ruby vial': 254, b'kernels of grain': 255}
opcodes = ["NOP", "MOV", "MOV_PC", "INVALID 3", "INVALID 4", "TEQ", "TGT", "TLT", "TCP", "ADD", "SUB", "MUL", "DIV", "NEG", "INVALID_14", "INVALID_15", "AND", "OR", "XOR", "SHL", "SHR"]

def decode_program(potion_file):
    potion = open(potion_file, "rb").read().replace(b".", b"").split(b", ")
    prog = b""
    for elem in potion:
        if elem[:4] == b"and ":
            elem = elem[4:]
        prog += p8(table[elem])

    return pygob.load(prog)
    
#print(decode_program("potion_1.txt"))
#print(decode_program("potion_2.txt"))

def choose_reg(n):
    if n == 0:
        return "REG_0"
    elif n == 1:
        return "REG_1"
    elif n == 2:
        return "REG_2"
    elif n == 3:
        return "REG_3"
    elif n == 4:
        return "ACC"
    elif n == 5:
        return "DAT"
    elif n == 6:
        return "ZERO"
    else:
        return "INVALID_REG"

def mov(ins):
    if ins.Bm & 1:
        print("MOV\t{} -> {}".format(choose_reg(ins.A0), choose_reg(ins.A1)), end="")
    else:
        print("MOV\t{} -> {}".format(ins.A0, choose_reg(ins.A1)), end="")

def test(ins):
    if ins.Bm & 1:
        first = choose_reg(ins.A0)
    else:
        first = ins.A0
    if ins.Bm & 2:
        second = choose_reg(ins.A1)
    else:
        second = ins.A1
    if ins.Opcode == 5:
        print("TEQ\t{} == {}".format(first, second), end="")
    elif ins.Opcode == 6:
        print("TGT\t{} > {}".format(first, second), end="")
    elif ins.Opcode == 7:
        print("TLT\t{} < {}".format(first, second), end="")
    elif ins.Opcode == 8:
        print("TCP\t{} ? {}".format(first, second), end="")

def arith(ins):
    if ins.Bm & 1:
        op = choose_reg(ins.A0)
    else:
        op = ins.A0
    if ins.Opcode == 9:
        print("ADD\tACC += {}".format(op), end="")
    elif ins.Opcode == 10:
        print("SUB\tACC -= {}".format(op), end="")
    elif ins.Opcode == 11:
        print("MUL\tACC *= {}".format(op), end="")
    elif ins.Opcode == 12:
        print("DIV\tACC /= {}".format(op), end="")
    elif ins.Opcode == 16:
        print("AND\tACC &= {}".format(op), end="")
    elif ins.Opcode == 17:
        print("OR\tACC |= {}".format(op), end="")
    elif ins.Opcode == 18:
        print("XOR\tACC ^= {}".format(op), end="")
    elif ins.Opcode == 19:
        print("SHL\tACC <<= {}".format(op), end="")
    elif ins.Opcode == 20:
        print("SHR\tACC >>= {}".format(op), end="")
    

def disasm(ins_list):
    for pc in range(len(ins_list)):
        print("{}\t".format(pc), end="")
        ins = ins_list[pc]
        mne = opcodes[ins.Opcode]
        if ins.Opcode == 0:
            print("NOP")
        elif ins.Opcode == 1:
            mov(ins)
        elif ins.Opcode == 2:
            print("MOV_PC\t{}".format(ins.A0), end="")
        elif ins.Opcode in [5, 6, 7, 8]:
            test(ins)
        elif ins.Opcode in [9, 10, 11, 12, 16, 17, 18, 19, 20]:
            arith(ins)
        elif ins.Opcode == 13:
            print("NEG\t~ACC\t", end="")
        else:
            print("INVALID_{}".format(ins.Opcode), end="")
        print("\t\tcond={}".format(ins.Cond))

prog_1 = decode_program("potion_1.txt")
prog_2 = decode_program("potion_2.txt")
print(prog_1)
for i in range(len(prog_1.Cpus)):
    print("CPU {}".format(i))
    cpu = prog_1.Cpus[i]
    disasm(cpu.Instructions)

print(prog_2)
for i in range(len(prog_2.Cpus)):
    print("CPU {}".format(i))
    cpu = prog_2.Cpus[i]
    disasm(cpu.Instructions)
