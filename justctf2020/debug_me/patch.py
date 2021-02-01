import ida_bytes

patches_main = [
    (0x1800 , 0x45c748fffff84be8),
    (0x1871 , 0x89e0458b48000000),
    (0x18e5 , 0x1ebfffff7b5e8c7),
    (0x1838 , 0x8948d8458b48c289),
    (0x18a8 , 0x775fff883fffffd)
]

patches_read_file = [
    (0x16db , 0xe8c78948000009ab),
    (0x174b , 0x8348008b48d8458b),
    (0x17bd , 0x1ebfffff93de8c7),
    (0x1712 , 0xe8c7894800000000),
    (0x1781 , 0xf975e8c78948f845)
]

patches_check_key = [
    (0x140b , 0xc700000000f845c7),
    (0x1494 , 0xbaf0458b1c7501f8),
    (0x151f , 0x1eb9004ebffffff),
    (0x144f , 0xbe0fef458800b60f),
    (0x14d7 , 0xf44539c0b60f1004)
]

patches_compare_char = [
    (0x13b9 , 0xb04a5b749d359b75),
    (0x13bd , 0x28c197b658b3b38d),
    (0x13c4 , 0x1ebfc4589ffc1d0),
    (0x13ba , 0x3bc43e2f0001b807),
    (0x13be , 0xffffffb805eb0000)
]

patches_calculate = [
    (0x1373 , 0x17e27f613f63871),
    (0x1376 , 0x1ebfc453a63b257),
    (0x1372 , 0x89d001e4458bc289)
]

# Patch the irrelevant 0xCC bytes
rip = [0x17f9, 0x16d4, 0x17cb, 0x1404, 0x13b2, 0x13d2, 0x136b, 0x1384, 0x152d]
CC = [0x17dc, 0x16b7, 0x17c6, 0x13E7, 0x1399, 0x13cd, 0x1352, 0x137f, 0x1528]

for i in range(len(rip)):
    ida_bytes.patch_bytes(CC[i], '\x90'*(rip[i] - CC[i])

# Patch the encrypted bytes
def patch(patches):
    for i in patches:
        print(hex(i[0]))
        ida_bytes.patch_qword(i[0], i[1])

patch(patches_main)
patch(patches_read_file)
patch(patches_check_key)
patch(patches_compare_char)
patch(patches_calculate)
