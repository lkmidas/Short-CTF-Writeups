from malduck import *
import cv2

packets = []
packets.append(bytearray(unhex("360200000a14080010c2a6b6c30318002208fffffecaaafafeca0a14080110b6bfb6c303180022082cf8fecaf3f8feca0a0e0802109efbb6c30318022202df290a0e080310abfcb6c30318022202d5230a0e08041098fdb6c30318022202dbbe0a0e080510f0ffb6c30318022202da840a0e080610dd80b7c30318022202dbe10a0e080710c882b7c30318022202c86c0a0e080810d483b7c30318022202cbd60a0e080910c094b7c30318022202dfae0a0e080a10ec95b7c30318022202d5520a0e080b10e996b7c30318022202db900a0e080c10c199b7c30318022202da490a0e080d108f9ab7c30318022202dbf10a0e080e10909fb7c30318022202c8f10a0e080f10bca0b7c30318022202cbbb0a14081010c2bdb7c3031800220807fefecafefafeca0a14081110bdc4b7c30318002208a5fffeca5ffafeca0a14081210e1cdb7c3031800220877fafecab3fbfeca0a1408131098fab7c30318002208a7fbfecabbfafeca0a140814109082b8c3031800220885fbfeca9cfafeca0a14081510a7a9b8c30318002208f4fbfecaa1fafeca0a14081610fbbcb8c30318002208c3fbfeca9bfafeca0a0e0817109dd6b8c30318022202cee90a0e081810aad7b8c30318022202d5eb0a0e081910bee0b8c30318022202ddb30a0e081a10ede5b8c3031802220286a60a0e081b10d8e7b8c30318022202dadb0a0e081c10f4e8b8c30318022202d53c0a0e081d10afeab8c3031802220286870a0e081e10c0efb8c30318022202d90c0a0e081f10fbf0b8c30318022202cb3e")))
packets.append(bytearray(unhex("6c0200000a0e082010a7f2b8c30318022202d2240a0e082110e3f3b8c30318022202d25e0a0e082210e0f4b8c30318022202860d0a0e082310b7f7b8c30318022202cd1c0a0e082410d4f8b8c30318022202d5060a0e082510aefab8c30318022202d2b70a0e082610eafbb8c30318022202ca470a0e082710a5fdb8c3031802220286de0a0e082810d881b9c30318022202d9b30a0e082910b383b9c30318022202c7120a0e082a10aa86b9c30318022202cc4d0a0e082b10c388b9c30318022202cbc80a0e082c10a293b9c30318022202d2430a0e082d10e093b9c30318022202dfbb0a14082e10f4d0b9c30318002208fefafecae1f8feca0a14082f10f0e1b9c3031800220858fafecad7fbfeca0a14083010d7f4b9c30318002208befbfecacdfbfeca0a140831108e87bac30318012208c2fbfecac7fbfeca0a14083210b893bac303180022081efbfeca11fbfeca0a14083310fea0bac30318002208cff8fecaf4fbfeca0a1408341086aebac303180022086df8feca5ffbfeca0a140835108dcbbac3031800220867fefeca4cf8feca0a14083610bbe0bac3031800220808fbfecab9f8feca0a14083710f5e7bac30318002208b7f9feca36f8feca0a14083810caf0bac303180022081efbfecaa6f8feca0a14083910f6f6bac3031800220843fbfecaa5f8feca0a14083a10c5fcbac30318002208f9f8fecafff8feca0a14083b10e282bbc303180022080ffbfecaa4f8feca0a14083c10e98abbc303180022084bf8feca3bf8feca0a14083d10e89abbc303180022085efbfeca30f8feca0a14083e1098a0bbc3031800220822f8fecabef8feca0a14083f10a6abbbc3031800220869f8feca4af8feca")))
packets.append(bytearray(unhex("ba0200000a14084010eeb2bbc3031800220807f9fecab6f8feca0a14084110e9b9bbc3031800220884fbfecae3f8feca0a140842109bbebbc30318002208c5fbfecaf9f8feca0a1408431080c2bbc30318002208dafbfecaf9f8feca0a140844109ac9bbc30318002208f6fbfecaa1f8feca0a14084510dcd2bbc30318002208f7f9fecaa6f8feca0a14084610d7d9bbc303180022084ffbfecab9f8feca0a14084710d5dfbbc3031800220862fbfecae7f8feca0a14084810b7e9bbc30318002208fbf8feca78f8feca0a140849109afdbbc30318002208a4fbfeca7cf8feca0a14084a10a589bcc3031800220878f9fecaf3f8feca0a14084b10b28fbcc30318002208e4f9fecaf9f8feca0a14084c10dc96bcc30318002208eef9fecabef8feca0a14084d10d99cbcc3031800220826f9fecaf8f8feca0a14084e10d7a2bcc30318002208edf9feca3bf8feca0a14084f1096a8bcc3031800220823f9feca3ff8feca0a14085010d2aebcc3031800220873f9fecafdf8feca0a14085110adb5bcc303180022089ff9fecafdf8feca0a14085210d7bcbcc3031800220823f9fecabdf8feca0a1408531096c2bcc3031800220878f9fecaa7f8feca0a1408541091c9bcc3031800220827f9feca35f8feca0a14085510c0cebcc30318002208def9feca79f8feca0a14085610b4e7bcc30318002208fffefeca7cfbfeca0a14085710c9fabcc3031800220885f8fecaa4f8feca0a14085810ef82bdc303180022081ff8feca8df8feca0a140859108da8bdc3031800220841fafecad0fbfeca0a14085a10ecb2bdc3031800220857fafecad6fbfeca0a14085b10a7b4bdc3031800220857fafecad6fbfeca0a14085c10a0c6bdc30318002208a9fefeca80fafeca0a14085d1099d3bdc3031800220875f8feca18f8feca0a14085e10f8ddbdc3031800220855fbfecabefafeca0a0e085f1086eebdc30318022202c9a6")))
packets.append(bytearray(unhex("300200000a0e08601082ffbdc30318022202db030a0e086110a583bec30318022202d45a0a0e0862108f85bec30318022202d97d0a0e086310dd85bec30318022202c7090a0e086410a887bec30318022202cc380a0e086510c588bec30318022202cb250a0e086610869dbec30318022202d91f0a0e086710f09ebec30318022202cb5d0a0e086810cba0bec30318022202c9d40a0e0869109da5bec30318022202dacb0a0e086a10e8a6bec30318022202d5fc0a0e086b1084a8bec30318022202d8960a0e086c10e2adbec30318022202c9f50a0e086d10dfaebec30318022202d5450a0e086e10dcafbec30318022202d33b0a0e086f10ceb9bec30318022202db130a0e087010f7bbbec30318022202d60d0a0e087110d2bdbec30318022202d2890a0e087210bcbfbec30318022202d50a0a0e08731097c1bec30318022202c71c0a0e08741084c2bec30318022202cadb0a14087510c2ecbec30318002208c9fafecaf9fafeca0a140876109989bfc30318002208cefafecadefbfeca0a14087710ec92bfc3031800220837f8fecaa4fbfeca0a14087810e39abfc3031800220846fafecaeefbfeca0a1408791097a4bfc30318002208a2f8feca6bfbfeca0a14087a10e0b0bfc3031800220887fafecadafafeca0a14087b109fcbbfc303180022086cf8fecab8fafeca0a14087c10c2d4bfc3031800220856fbfecaa4fafeca0a0e087d10d5edbfc30318022202c9ae0a0e087e10deefbfc30318022202c7320a0e087f10dcf5bfc30318022202d220")))
packets.append(bytearray(unhex("620200000a0f08800110c283c0c30318022202c9500a0f088101108a86c0c30318022202dbee0a0f08820110878cc0c30318022202d2400a0f08830110b38dc0c30318022202c7780a0f088401108b90c0c30318022202da360a0f088501108891c0c30318022202d5fd0a0f088601109592c0c30318022202d8120a1508870110b3a2c0c3031800220858f8fecaa5fafeca0a0f08880110ddaec0c30318022202cd490a0f08890110daafc0c30318022202d5320a0f088a0110b5b1c0c30318022202d2f60a0f088b0110d1b2c0c30318022202ca9e0a0f088c0110cfb8c0c30318022202867d0a0f088d0110e8bac0c30318022202d6490a0f088e0110b3bcc0c30318022202d8dc0a0f088f0110adbec0c30318022202cfad0a0f08900110a7c0c0c30318022202c94f0a0f0891011094c1c0c30318022202cb140a1508920110f9dec0c30318002208fcf8fecabbfbfeca0a150893011093e6c0c30318002208dcfefeca0bfafeca0a1508940110e3f5c0c303180022085bfafecab0fbfeca0a1508950110fbbbc1c30318002208f3f8fecabafafeca0a1508960110a2c9c1c3031800220885f9fecaa6fafeca0a1508970110c3d3c1c3031800220894f8fecaa7fafeca0a1508980110efd9c1c3031800220862f8feca81fbfeca0a0f08990110b8e1c1c3031802220297f20a0f089a011084e8c1c303180222029e440a0f089b0110dbeac1c303180222029e400a0f089c0110c3edc1c303180222029c660a15089d011098f6c1c3031800220888f9fecaaafafeca0a15089e0110d880c2c30318002208d7f8fecaaafafeca0a15089f0110a7a5c2c3031800220854f8feca14fbfeca")))
packets.append(bytearray(unhex("6e0200000a0f08a00110d4abc2c30318022202976b0a0f08a10110bbaec2c3031802220296c40a0f08a20110c5b0c2c3031802220296300a1508a30110d6bac2c303180022083ff8fecabcf8feca0a1508a40110aed7c2c30318002208aff9feca12fbfeca0a1508a50110e1e0c2c303180022084af9fecaa3fafeca0a1508a60110e8e8c2c3031800220831f9feca9ffafeca0a0f08a70110d6eec2c30318022202dbb70a0f08a80110e0f0c2c30318022202d9320a0f08a90110caf2c2c30318022202c83b0a0f08aa01108ff6c2c3031802220286a10a0f08ab0110d7f8c2c30318022202da220a0f08ac011093fac2c30318022202d5f60a0f08ad0110defbc2c3031802220286220a0f08ae0110b6fec2c30318022202dc910a0f08af01108180c3c30318022202d49d0a0f08b001108d81c3c30318022202cae10a1508b10110f7c6c3c3031800220805fefecaf6fafeca0a1508b20110bad5c3c30318002208f8fffeca52fafeca0a1508b30110c2e2c3c3031800220891fbfecad8fafeca0a1508b40110b5f6c3c30318002208adfbfeca30fafeca0a1508b501109795c4c3031800220885f9fecabbfafeca0a1508b60110cd9dc4c3031800220896f8fecaa3fafeca0a0f08b70110cba8c4c30318022202988b0a0f08b8011083abc4c30318022202991f0a0f08b90110faadc4c3031802220297da0a0f08ba0110ccb2c4c303180222029eb00a0f08bb0110b1b6c4c3031802220298ca0a1508bc01108bd2c4c3031800220801f8fecab6f8feca0a1508bd01109fdbc4c30318002208a0f9feca3bfbfeca0a0f08be0110cfe5c4c303180222029a990a1508bf0110e9ecc4c3031800220819f8fecab3f8feca")))
packets.append(bytearray(unhex("e00200000a1508c00110f295c6c303180022086df8feca82fbfeca0a1508c101108e97c6c303180022086df8feca82fbfeca0a1508c20110f39ac6c3031800220870f8feca85fbfeca0a1508c301108f9cc6c3031800220870f8feca85fbfeca0a1508c40110ab9dc6c3031800220870f8feca85fbfeca0a1508c50110d79ec6c3031800220870f8feca85fbfeca0a1508c60110a2a0c6c3031800220870f8feca85fbfeca0a1508c70110d8a3c6c3031800220858f8feca92fbfeca0a1508c80110e4a4c6c3031800220858f8feca92fbfeca0a1508c901109aa8c6c3031800220858f8feca92fbfeca0a1508ca0110e5a9c6c3031800220858f8feca92fbfeca0a1508cb0110ccacc6c3031800220858f8feca92fbfeca0a1508cc0110f8adc6c3031800220858f8feca92fbfeca0a1508cd01108eb1c6c3031800220858f8feca9dfbfeca0a1508ce0110abb2c6c3031800220858f8feca9dfbfeca0a1508cf011082b5c6c3031800220858f8feca9dfbfeca0a1508d00110cdb6c6c3031800220858f8feca9dfbfeca0a1508d10110d4b9c6c3031800220858f8feca9dfbfeca0a1508d2011090bbc6c3031800220858f8feca9dfbfeca0a1508d30110a6bec6c3031800220858f8feca9dfbfeca0a1508d40110c2bfc6c3031800220858f8feca9dfbfeca0a1508d5011087c3c6c303180022087ef8feca90fbfeca0a1508d60110b3c4c6c303180022087ef8feca90fbfeca0a1508d70110f8c7c6c3031800220848f8feca9ffbfeca0a1508d8011094c9c6c3031800220848f8feca9ffbfeca0a1508d9011085cec6c3031800220841f8feca9efbfeca0a1508da0110a2cfc6c3031800220841f8feca9efbfeca0a1508db0110f3d3c6c3031800220841f8feca9efbfeca0a1508dc0110afd5c6c3031800220841f8feca9efbfeca0a1508dd011084d9c6c3031800220841f8feca99fbfeca0a1508de0110bfdac6c3031800220841f8feca99fbfeca0a1508df0110dce0c6c30318002208d2f8feca9ffbfeca")))
packets.append(bytearray(unhex("e00200000a1508e00110aeeac6c303180022085af8feca99fbfeca0a1508e10110a1fec6c3031800220850f8feca9efbfeca0a1508e201108eaec7c30318002208d1f8feca90fbfeca0a1508e30110e7b5c7c303180022087df8feca9afbfeca0a1508e40110febdc7c303180022085bf8feca9ffbfeca0a1508e50110efc2c7c3031800220847f8feca99fbfeca0a1508e6011082c7c7c30318002208c5f8feca98fbfeca0a1508e701109fcdc7c3031800220834f8feca98fbfeca0a1508e80110a5d0c7c30318002208d0f8feca9afbfeca0a1508e90110fad3c7c3031800220867f8feca85fbfeca0a1508ea0110dae8c7c3031800220818f8feca93fbfeca0a1508eb01109fecc7c3031800220828f8feca9bfbfeca0a1508ec0110f7eec7c303180022085bf8feca99fbfeca0a1508ed011094f5c7c30318002208b7f9fecaa8fafeca0a1508ee01108ffcc7c3031800220850f9fecaaafafeca0a1508ef01109d8cc8c30318002208b4f8fecaaafafeca0a1508f00110da97c8c3031800220853f8feca92fbfeca0a1508f10110999dc8c303180022083cf8feca9efbfeca0a1508f2011084a4c8c303180022083af8feca92fbfeca0a1508f30110e8a7c8c3031800220841f8feca90fbfeca0a1508f4011096d2c8c30318002208a2fefecaf7fbfeca0a1508f50110d5d7c8c30318012208e2fefecaeffbfeca0a1508f6011088dcc8c3031800220873f9fecac4fbfeca0a1508f7011086e7c8c30318002208f9fffeca70fafeca0a1508f801108af0c8c30318002208a9fefecafefbfeca0a1508f9011092f8c8c30318002208a6fafecaa9fbfeca0a1508fa0110edfec8c3031800220866fbfeca7efafeca0a1508fb0110cc89c9c303180022086ef9fecad0fafeca0a1508fc0110e496c9c3031800220846f8feca96fbfeca0a1508fd0110e79ac9c303180022087bf9feca90fbfeca0a1508fe0110c6a0c9c30318002208b7f9fecaecfbfeca0a1508ff0110baa4c9c303180022087ff9fecaeafbfeca")))
packets.append(bytearray(unhex("560200000a150880021092c6c9c3031800220863f9feca54fbfeca0a15088102109bd8c9c303180022080cf8fecabbfafeca0a150882021089dec9c303180022080cf8fecabbfafeca0a1508830210b5e4c9c3031800220878f8fecaa4fafeca0a1508840210d2eac9c3031800220860f8fecaa7fafeca0a1508850210eff0c9c3031800220879fbfecaa1fafeca0a15088602108cfcc9c3031800220843fafecabafafeca0a1508870210af80cac3031800220844fafeca85fafeca0a0f08880210eadfcac30318022202ce9d0a0f0889021096e1cac30318022202cb490a0f088a0210e1e2cac30318022202d82c0a0f088b0210d5e6cac30318022202d5800a0f088c0210a0e8cac30318022202867e0a0f088d0210f9f4cac30318022202d5c50a0f088e0210c7f5cac30318022202cc990a0f088f02108e88cbc3031802220286d50a0f089002108f8dcbc30318022202cee90a0f08910210c191cbc30318022202cb800a0f089202108d98cbc30318022202dab20a0f089302109a99cbc30318022202ceea0a0f08940210979acbc30318022202cbc90a0f08950210ad9dcbc3031802220286cc0a0f08960210979fcbc30318022202d9530a0f0897021091a1cbc30318022202dabf0a0f08980210ffa1cbc30318022202d5670a0f08990210f3a5cbc30318022202d8d60a0f089a0210f0a6cbc30318022202d3bf0a0f089b0210f9a8cbc3031802220286140a0f089c0210faadcbc30318022202ddd60a0f089d021087afcbc30318022202da7e0a0f089e0210f4afcbc30318022202cc2d0a15089f0210aed6cbc30318002208dafbfecab7fbfeca")))
packets.append(bytearray(unhex("e00200000a1508a002108ff5cbc303180022085cfbfecacffafeca0a1508a10210c488ccc303180022085cfbfecacffafeca0a1508a20210b0cdccc30318002208fffffecaaafafeca0a1508a302108cd4ccc3031800220869fbfeca98f8feca0a1508a40210f3d6ccc303180022089cf9fecaadf8feca0a1508a502109cd9ccc303180122088df9fecaa7f8feca0a1508a60210b9dfccc30318002208c6f9feca9afbfeca0a1508a70210ade3ccc30318002208cdf9feca92fbfeca0a1508a80210e2e6ccc3031801220850fbfeca99f8feca0a1508a90210caeeccc30318002208e0f8fecacffbfeca0a1508aa0210e0f1ccc3031800220887f8feca5afbfeca0a1508ab0210f1fbccc3031800220884f8feca45fbfeca0a1508ac02109dfdccc3031800220884f8feca45fbfeca0a1508ad0210c081cdc3031801220884f8feca45fbfeca0a1508ae0210da88cdc30318002208c7f8fecab3fbfeca0a1508af0210ac8dcdc30318002208fffffecaaafafeca0a1508b002108794cdc3031800220806f8fecaf5fafeca0a1508b102109a98cdc30318002208fffffecaaafafeca0a1508b20210ae9ccdc3031800220855fbfeca76fafeca0a1508b30210f7a8cdc303180122080ffbfeca1cfafeca0a1508b402109aadcdc3031800220861fbfeca47fafeca0a1508b50210efb0cdc3031800220830fbfeca6bfafeca0a1508b60210a1b5cdc3031801220834fbfeca11fafeca0a1508b70210ffbacdc3031800220873fbfeca52fafeca0a1508b8021099bdcdc30318012208e8fbfeca1ffafeca0a1508b90210fac1cdc303180022082bfbfeca40fafeca0a1508ba021093c4cdc30318012208a3fbfecae5fafeca0a1508bb0210f2c9cdc30318002208dffbfeca3bfafeca0a1508bc0210aacccdc30318012208d0fbfecadcfafeca0a1508bd0210fcd0cdc303180022081efbfeca01fafeca0a1508be021080d5cdc30318012208b3fbfecac5fafeca0a1508bf0210e4d8cdc30318002208f0fbfeca1afafeca")))

clicks = []

def parse(data):
    global clicks
    length = u32(data[0:4])
    data = data[4:]
    i = 0
    while i < length:
        if data[i:i+3] == b"\x0a\x14\x08":
            seq_num = data[i+3]
            timestamp = u64(data[i+4:i+11] + b"\0")
            point_x = u32(data[i+14:i+18]) ^ 0xCAFEFAAA
            point_y = u32(data[i+18:i+22]) ^ 0xCAFEFAAA
            print("{} \t {} \t Mouse x = {}, y = {}".format(seq_num, timestamp, point_x, point_y))
            clicks.append((point_x, point_y))
            i += 22
        elif data[i:i+3] == b"\x0a\x0e\x08":
            seq_num = data[i+3]
            timestamp = u64(data[i+4:i+11] + b"\0")
            key_enc = data[i+14]
            if key_enc >= 0x96 and key_enc <= 0x9f:
                key = chr(key_enc - 0x66)
            elif key_enc >= 0xbb and key_enc <= 0xe0:
                key = chr(key_enc + 0x7a - 0x100)
            elif key_enc == 0x86:
                key = " "
            else:
                key = "unknown"
            print("{} \t {} \t Key = {}".format(seq_num, timestamp, key))
            i += 16
        elif data[i:i+3] == b"\x0a\x0f\x08":
            seq_num = u16(data[i+3:i+5]) - 0x100
            timestamp = u64(data[i+5:i+12] + b'\0')
            key_enc = data[i+15]
            if key_enc >= 0x96 and key_enc <= 0x9f:
                key = chr(key_enc - 0x66)
            elif key_enc >= 0xbb and key_enc <= 0xe0:
                key = chr(key_enc + 0x7a - 0x100)
            elif key_enc == 0x86:
                key = " "
            else:
                key = "unknown"
            print("{} \t {} \t Key = {}".format(seq_num, timestamp, key))
            i += 17
        elif data[i:i+3] == b"\x0a\x15\x08":
            seq_num = u16(data[i+3:i+5]) - 0x100
            timestamp = u64(data[i+5:i+12] + b'\0')
            point_x = u32(data[i+15:i+19]) ^ 0xCAFEFAAA
            point_y = u32(data[i+19:i+23]) ^ 0xCAFEFAAA
            print("{} \t {} \t Mouse x = {}, y = {}".format(seq_num, timestamp, point_x, point_y))
            clicks.append((point_x, point_y))
            i += 23
        else:
            print("Unknown sequence")
            return


for i in range(len(packets)):
    parse(packets[i])

# Plot the clicks on screenshot with OSK
cnt = 1
for i in range(16, 37):
    img = cv2.imread("./keyboard.png")
    cv2.circle(img, clicks[i], 6, (0,0,255), -1)
    cv2.imwrite("./imgs/tmp{}.jpg".format(cnt), img)
    cnt += 1


for i in range(37, 50):
    img = cv2.imread("./keyboard2.png")
    cv2.circle(img, clicks[i], 6, (0,0,255), -1)
    cv2.imwrite("./imgs/tmp{}.jpg".format(cnt), img)
    cnt += 1