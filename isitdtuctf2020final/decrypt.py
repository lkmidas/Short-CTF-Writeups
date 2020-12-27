MAP = {'H':'!', 'U':'*', 'N':'>', 'G':')', 'X':'e', 'I':'j', 'O':'v', 'A':'u', 'W':' ', 'T':'#', 'M':'/', 'L':'-', 'Y':'{', 'Z':'(', 'J':':', 'P':'^', 'C':'|', 'Q':'\\'}

def decrypt(str):
    result = ""
    i = len(str) - 1
    while True:
        c = str[i]
        if c in MAP.keys():
            c = chr(ord(MAP[str[i]]) - 1)
        else:
            c = chr(ord(str[i]) - 1)
        result += c
        i -= 1
        if i < 0:
            break
    return result


buf = "XofHUUXofHHHU2.U72HLYGsfcnOopAGsbidMhoIsAtHosOAfsHHHHHUYGHopIAdoOgHLZMMZGcOth;ggOcGHosOAfsHHHUggOcGhoIybHopIAdoOg"
print(decrypt(buf))
buf = "XofHqnfAHosOAfsHXofHUPIQoIhfcHLPIQAtbmHLqnfAGcOthMhoIsAtHNHqnfAHpXHoIhfc$L2NIHspgHggOcHNHqnfAHmbdpmHXofHZ1ZHosOAfsHo"
buf += "fiAHmIoHNNHggOcHgIHUHggOcHGsdfXHopIAdoOgH~ZlZLZxZLZIZLZnZLZoZLZYZLZzZLZsZLZrZLZhZLZwZLZqZLZtZLZiZLZOZLZyZCHNHAtbmH~Z"
buf += "gZHLZfZHLZXZHLZdZHLZcZHLZbZHLZJZHLZ9ZHLZ8ZHLZ7ZHLZ6ZHLZ5ZLZ4ZLZ3ZHLZ2ZLZ1ZCHNHoIhfc"
print(decrypt(buf))
buf = "XofHAyAHosOAfsHXofHdHMMHAyAHNHAyAHUUILsAtGfAzcMhoIsAtGsbidMhoIsAtHNHdHmbdpmHpXH2.L2LsAt$NIHspgHZZHNHAyAHmbdpmHXofHZ1"
buf += "ZHosOAfsHofiAHmIoHNNHsAtHgIHUHsAtHGsftfwfsHopIAdoOg"
print(decrypt(buf))
buf = "XofHqnfAHosOAfsHUTXTHLTYTHLqnfAGcOthMhoIsAtHNHqnfAHUT7THLTXTHLqnfAGcOthMhoIsAtHNHqnfAHUTYTHLT7THLggOcGcOthMhoIsAtHNH"
buf += "qnfAHUTgTHLTYTHLqnfAGcOthMhoIsAtHNHqnfAHUT6THLTgTHLqnfAGcOthMhoIsAtHNHqnfAHUTYTHLT6THLggOcGcOthMhoIsAtHNHqnfAHmbdpmH"
buf += "UggOcGhobIybHopIAdoOg"
print(decrypt(buf))
buf = "XofHUUUUUsAtGsftfwfsGsdfXGhobIybGhoIybGsftfwfsHosOAfsHUsAtGhobIyhoIyHopIAdoOg"
print(decrypt(buf))

print("---------------------------------------")

buf = "hobIyhoIy"
print(decrypt(buf))

print("---------------------------------------")


def axing(buff):
    return ''.join(chr(int(buff[i:i+2],16)-1) for i in range(0, len(buff), 2))

begin = [ '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f' ]
last = [ 'x', 'u', 'h', 's', 'p', 'v', 'g', 'q', 'r', 'y', 'z', 'n', 'm', 'i', 'w','k']

def decr(buff):
    temp = buff[::]
    for i in range(16):
        temp = temp.replace(last[i], begin[i])
    return temp

def reveser(s):
    return s[::-1]

def axiang(buff):
    temp = buff.replace('5', 'z')
    temp = temp.replace('f', '5')
    temp = temp.replace('z', 'f')
    temp = buff.replace('6', 'z')
    temp = temp.replace('d', '6')
    temp = temp.replace('z', 'd')
    return temp

def xingxiang(s):
    return reveser(axing(axiang(decr(reveser(s)))))


# auto_9yin
buf = "qqiisqpqzixqkiuhwsuhrhsskhpsvskpspqvqprhnx"
print(xingxiang(buf))
buf =  "qiiqkipivqzixqkiuhriiivqqviisqpqzixqkiyhuhkhkhkhuhzhnxuhuhsqiivqiqsqkiuhqqiisqpqzixqkinxiikivinxnxsqiihqiqzisqiiyhrhrqsizivqrhzhnx"
print(xingxiang(buf))
buf =  "sqiihqiqzisqiiyhrhhiiqvqxqxiqiiqkipivqzixqkipqrhzhnxviiigihizqxisqiihiviuhwsuhusnxviiigivqhiuhwsuhusyqzsippsrsrszssp"
buf += "zsnxnxwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwh"
buf += "whwhwhwhwhwhwhwhwhwhwhwhwhwhnxwhwhuhppxqkiqqiisqpqzixqkinxwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwh"
buf += "whwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhnxnx"
print(xingxiang(buf))
buf =  "qiiqkipivqzixqkiuhpixqkiqqiisqvqpvvqsqzikirivvxqspzqvqiipqyhpqvqsqzhnxuhuhgixqpihigiuhsizqvqiipquhwsuhmqwqnxuhuhgixq"
buf += "pihigiuhpqvqsqgpiikirivqyiuhwsuhpqvqsqzikirikhgiiikiyhpqvqsqzhnxuhuhqixqsquhziwshsghpqvqsqgpiikirivqyiuhvixqnxuhuhuh"
buf += "uhvqhisigiiikhzikipqiisqvqyhsizqvqiipqghuhpqvqsqzikirikhsizqvqiiyhpqvqsqghuhzizhzhnxuhuhiikivinxnxuhuhsqiivqiqsqkiuh"
buf += "sizqvqiipqnxiikivinxnx"
print(xingxiang(buf))
buf =  "qiiqkipivqzixqkiuhpixqkiqqiisqvqspzqvqiipqvvxqpvvqsqzikiriyhsizqvqiipqzhnxuhuhgixqpihigiuhpqvqsquhwsuhrhrhnxuhuhziqi"
buf += "uhsizqvqiipquhkqwsuhkizigiuhvqyiiikiuhuhnxuhuhgixqpihigiuhsizqvqiipqgpiikirivqyiuhwsuhvqhisigiiikhriiivqkiyhsizqvqii"
buf += "pqzhnxuhuhuhuhqixqsquhziwshsghsizqvqiipqgpiikirivqyiuhvixqnxuhuhuhuhuhuhpqvqsquhwsuhpqvqsquhkhkhuhpqvqsqzikirikhpiyi"
buf += "hisqyhsizqvqiipqmvziwvzhnxuhuhuhuhiikivinxuhuhiikivinxuhuhsqiivqiqsqkiuhpqvqsqnxiikivinxnx"
print(xingxiang(buf))
buf =  "qiiqkipivqzixqkiuhpixqkiqqiisqvqypiiyqpvvqsqzikirivvxqspzqvqiipqyhpqvqsqzhnxuhuhgixqpihigiuhsizqvqiipquhwsuhmqwqnxuh"
buf += "uhgixqpihigiuhpqvqsqgpiikirivqyiuhwsuhpqvqsqzikirikhgiiikiyhpqvqsqzhnxuhuhqixqsquhmiwsssghpqvqsqgpiikirivqyighssuhvi"
buf += "xqnxuhuhuhuhgixqpihigiuhyiiiyqpvvqsqzikiriuhwsuhrhusyqrhuhkhkhuhpqvqsqzikirikhpqiqsiyhpqvqsqghuhyhmiuhwhuhhszhghuhmi"
buf += "zhnxuhuhuhuhvqhisigiiikhzikipqiisqvqyhsizqvqiipqghuhyiiiyqkhvqxqxiviiipiyhyiiiyqpvvqsqzikirizhzhnxuhuhiikivinxnxuhuh"
buf += "sqiivqiqsqkiuhsizqvqiipqnxiikivinxnx"
print(xingxiang(buf))
buf =  "qiiqkipivqzixqkiuhpixqkiqqiisqvqspzqvqiipqvvxqypiiyqpvvqsqzikiriyhsizqvqiipqzhnxuhuhgixqpihigiuhpqvqsquhwsuhrhrhnxuh"
buf += "uhgixqpihigiuhsizqvqiipqgpiikirivqyiuhwsuhvqhisigiiikhriiivqkiyhsizqvqiipqzhnxuhuhqixqsquhziwshsghsizqvqiipqgpiikiri"
buf += "vqyiuhvixqnxuhuhuhuhgixqpihigiuhyiiiyqpvvqsqzikiriuhwsuhpqvqsqzikirikhpqiqsiyhyiiiyqkhvqxqxiyiiiyqyhsizqvqiipqmvziwv"
buf += "zhghuhpszhnxuhuhuhuhziqiuhpqvqsqzikirikhgiiikiyhyiiiyqpvvqsqzikirizhuhwswsuhhsuhvqyiiikinxuhuhuhuhuhuhyiiiyqpvvqsqzi"
buf += "kiriuhwsuhrhusrhuhkhkhuhyiiiyqpvvqsqzikirinxuhuhuhuhiikivinxuhuhuhuhpqvqsquhwsuhpqvqsquhkhkhuhyiiiyqpvvqsqzikirinxuh"
buf += "uhiikivinxnxuhuhsqiivqiqsqkiuhpqvqsqnxiikivinxnx"
print(xingxiang(buf))
buf =  "qiiqkipivqzixqkiuhpixqkiqqiisqvqspzqvqiipqvvxqivzpkivqhpsqsqhizqyhsizqvqiipqghuhzikipigiiqviiigpiikirivqyizhnxuhuhgi"
buf += "xqpihigiuhsizqvqiipqgpiikirivqyiuhwsuhvqhisigiiikhriiivqkiyhsizqvqiipqzhnxuhuhgixqpihigiuhsqiipqiqgivquhwsuhmqwqnxnx"
buf += "uhuhziqiuhzikipigiiqviiigpiikirivqyiuhvqyiiikinxuhuhuhuhgixqpihigiuhkiuhwsuhsizivqkhsisqpqyiziqivqyhsizqvqiipqgpiiki"
buf += "rivqyighuhsszhuhmhuhhsnxuhuhuhuhziqiuhsizivqkhsihikiviyhsizqvqiipqgpiikirivqyighuhpszhuhkqwsuhusuhvqyiiikinxuhuhuhuh"
buf += "uhuhkiuhwsuhkiuhmhuhhsnxuhuhuhuhiikivinxnxuhuhuhuhsqiipqiqgivqmvkiwvuhwsuhsizqvqiipqgpiikirivqyimsnxuhuhiikivinxnxuh"
buf += "uhqixqsquhziwsusghyhsizqvqiipqgpiikirivqyiuhwhuhhszhuhvixqnxuhuhuhuhgixqpihigiuhsqiipqiqgivqzpkiviiiyquhwsuhsizivqkh"
buf += "sisqpqyiziqivqyhzighuhsszhuhmhuhhsnxuhuhuhuhziqiuhsqiipqiqgivqmvsqiipqiqgivqzpkiviiiyqwvuhwswsuhkizigiuhvqyiiikinxuh"
buf += "uhuhuhuhuhsqiipqiqgivqmvsqiipqiqgivqzpkiviiiyqwvuhwsuhusnxuhuhuhuhiikivinxnxuhuhuhuhgixqpihigiuhsqiipqiqgivqqvhigiiq"
buf += "iiuhwsuhsizivqkhsigipqyiziqivqyhsizivqkhsihikiviyhusyqususususususqiqighuhsizqvqiipqmvzimhhswvzhghuhsizivqkhsigipqyi"
buf += "ziqivqyhsizivqkhsihikiviyhzighuhpszhghuhpszhzhnxuhuhuhuhsqiipqiqgivqmvsqiipqiqgivqzpkiviiiyqwvuhwsuhsizivqkhsixqsqyh"
buf += "sqiipqiqgivqmvsqiipqiqgivqzpkiviiiyqwvghuhsqiipqiqgivqqvhigiiqiizhmsnxuhuhiikivinxnxuhuhsqiivqiqsqkiuhsqiipqiqgivqnxiikivinxnx"
print(xingxiang(buf))
buf =  "qiiqkipivqzixqkiuhpixqkiqqiisqvqivzpkivqhpsqsqhizqvvxqspzqvqiipqyhvihivqhighuhzikipigiiqviiigpiikirivqyizhnxuhuhgixq"
buf += "pihigiuhvihivqhigpiikirivqyiuhwsuhvqhisigiiikhriiivqkiyhvihivqhizhnxuhuhgixqpihigiuhkiuhwsuhsizivqkhsigipqyiziqivqyh"
buf += "vihivqhigpiikirivqyighuhsszhnxuhuhgixqpihigiuhsqiipqiqgivquhwsuhmqwqnxnxuhuhziqiuhzikipigiiqviiigpiikirivqyiuhvqyiii"
buf += "kinxuhuhuhuhgixqpihigiuhwiuhwsuhvihivqhimvvihivqhigpiikirivqyiwvnxuhuhuhuhziqiuhwiuhksuhkiuhvqyiiikinxuhuhuhuhuhuhsq"
buf += "iivqiqsqkiuhkiziginxuhuhuhuhiikivinxnxuhuhuhuhkiuhwsuhwinxuhuhiikivinxnxuhuhqixqsquhziwsusghyhkiwhhszhuhvixqnxuhuhuh"
buf += "uhgixqpihigiuhqqhigiiqiiuhwsuhsizivqkhsihikiviyhsizivqkhsisqpqyiziqivqyhvihivqhimvsizivqkhsisqpqyiziqivqyhzighuhsszh"
buf += "uhmhuhhswvghuhyhsizivqkhsigipqyiziqivqyhsizivqkhsihikiviyhzighuhpszhghuhpszhzhzhghuhusyqqiqizhnxuhuhuhuhvqhisigiiikh"
buf += "zikipqiisqvqyhsqiipqiqgivqghuhqqhigiiqiizhnxuhuhiikivinxnxuhuhsqiivqiqsqkiuhsqiipqiqgivqnxiikivinxnx"
print(xingxiang(buf))
buf =  "qiiqkipivqzixqkiuhpixqkiqqiisqvqvvxqivzpkivqpsssyhqqhigiiqiizhnxuhuhziqiuhqqhigiiqiiuhgsuhusuhvqyiiikinxuhuhuhuhgixq"
buf += "pihigiuhhisipqqvhigiiqiiuhwsuhwihivqyikhhisipqyhqqhigiiqiizhnxuhuhuhuhgixqpihigiuhhiuhwsuhwihivqyikhqigixqxqsqyhhisi"
buf += "pqqvhigiiqiiuhxsuhusyqqpqpqpqpqpqpqpqpzhnxuhuhuhuhgixqpihigiuhsiuhwsuhqqhigiiqiiuhmhuhhiuhnhuhusyqqpqpqpqpqpqpqpqpnx"
buf += "uhuhuhuhgixqpihigiuhpiuhwsuhusyqqpqpqpqpqpqpqpqpuhmhuhsiuhmhuhhsnxuhuhuhuhsqiivqiqsqkiuhpinxuhuhiikivinxnxuhuhsqiivq"
buf += "iqsqkiuhwihivqyikhwixqviyhqqhigiiqiighuhusyqqpqpqpqpqpqpqpqpzhuhwhuhwihivqyikhqigixqxqsqyhqqhigiiqiiuhxsuhusyqqpqpqp"
buf += "qpqpqpqpqpzhnxiikivinxnxwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwh"
buf += "whwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhnxwhwhuhipkipisqzquqvqzixqkixsviiipisqzquqvqzixqkiuhpixqwiwixqkinxwhwh"
buf += "whwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwh"
buf += "whwhwhwhwhwhwhwhwhnxnx"
print(xingxiang(buf))
buf =  "qiiqkipivqzixqkiuhwiyqyhpqiqwighuhzqghuhnqghuhuqghuhiighuhmizhnxuhuhgixqpihigiuhhihiuhwsuhsizivqkhsisqpqyiziqivqyhnq"
buf += "ghuhiszhnxuhuhgixqpihigiuhhisiuhwsuhpixqkiqqiisqvqvvxqivzpkivqpsssyhsizivqkhsigipqyiziqivqyhzqghuhsszhzhnxuhuhgixqpi"
buf += "higiuhhipiuhwsuhsizivqkhsiyqxqsqyhhihighuhhisizhnxnxuhuhgixqpihigiuhsihiuhwsuhsizivqkhsisqpqyiziqivqyhzqghuhpszhnxuh"
buf += "uhgixqpihigiuhsisiuhwsuhpixqkiqqiisqvqvvxqivzpkivqpsssyhsizivqkhsigipqyiziqivqyhnqghuhvszhzhnxuhuhgixqpihigiuhsipiuh"
buf += "wsuhsizivqkhsiyqxqsqyhsihighuhsisizhnxuhuhgixqpihigiuhpihiuhwsuhsizivqkhsiyqxqsqyhpqiqwighuhzqzhnxnxuhuhgixqpihigiuh"
buf += "vizihiuhwsuhsizivqkhsihikiviyhuqghuhpszhnxuhuhgixqpihigiuhvizisiuhwsuhsizivqkhsiyqxqsqyhvizihighuhiizhnxuhuhgixqpihi"
buf += "giuhvihiuhwsuhmimvvizisiuhmhuhhswvnxuhuhgixqpihigiuhvisiuhwsuhsizivqkhsiyqxqsqyhvihighuhnqzhnxnxuhuhgixqpihigiuhiihi"
buf += "uhwsuhpixqkiqqiisqvqvvxqivzpkivqpsssyhpihiuhmhuhvisizhnxuhuhgixqpihigiuhqihiuhwsuhpixqkiqqiisqvqvvxqivzpkivqpsssyhhi"
buf += "piuhmhuhsipizhnxuhuhgixqpihigiuhrihiuhwsuhsizivqkhsiyqxqsqyhqihighuhiihizhnxnxuhuhsqiivqiqsqkiuhrihinxiikivinxnxwhwh"
buf += "whwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwh"
buf += "whwhwhwhwhwhwhwhwhnxwhwhuhvpiipisqzquqvqzixqkinxwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwh"
buf += "whwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhnxnx"
print(xingxiang(buf))
buf =  "qiiqkipivqzixqkiuhviiipisqzquqvqzpkivqhpsqsqhizqyhqqghuhmizhnxuhuhgixqpihigiuhkiuhwsuhvqhisigiiikhriiivqkiyhqqzhnxuh"
buf += "uhgixqpihigiuhnquhwsuhqqmvkiwvnxuhuhgixqpihigiuhzquhwsuhqqmvhswvnxuhuhgixqpihigiuhiiuhwsuhusnxuhuhgixqpihigiuhuquhws"
buf += "uhusnxnxuhuhgixqpihigiuhhquhwsuhqsuhmhuhwihivqyikhqigixqxqsqyhisssuhxsuhkizhnxuhuhgixqpihigiuhpqiqwiuhwsuhpixqkiqqii"
buf += "sqvqvvxqivzpkivqpsssyhhquhnhuhviiigivqhizhnxuhuhrqyizigiiiuhpqiqwiuhkqwsuhusuhvixqnxuhuhuhuhiiuhwsuhsizivqkhsihikivi"
buf += "yhsizivqkhsisqpqyiziqivqyhpqiqwighuhsszhghuhpszhnxuhuhuhuhqixqsquhuqwskighssghwhhsuhvixqnxuhuhuhuhuhuhnquhwsuhqqmvuq"
buf += "uhwhuhhswvnxuhuhuhuhuhuhqqmvuqwvuhwsuhpixqkiqqiisqvqvvxqivzpkivqpsssyhqqmvuqwvuhwhuhwiyqyhpqiqwighuhzqghuhnqghuhyhuq"
buf += "whhszhghuhiighuhmizhzhnxuhuhuhuhuhuhzquhwsuhqqmvuqwvnxuhuhuhuhiikivinxnxuhuhuhuhnquhwsuhqqmvkiwvnxuhuhuhuhqqmvhswvuh"
buf += "wsuhpixqkiqqiisqvqvvxqivzpkivqpsssyhqqmvhswvuhwhuhwiyqyhpqiqwighuhzqghuhnqghuhuqghuhiighuhmizhzhnxuhuhuhuhzquhwsuhqq"
buf += "mvhswvnxnxuhuhuhuhgixqpihigiuhpqiqwispiiqixqsqiiuhwsuhpqiqwinxuhuhuhuhpqiqwiuhwsuhpixqkiqqiisqvqvvxqivzpkivqpsssyhpq"
buf += "iqwiuhwhuhviiigivqhizhnxuhuhiikivinxnxuhuhsqiivqiqsqkiuhqqnxiikivinxnx"
print(xingxiang(buf))
buf =  "qiiqkipivqzixqkiuhviiipisqzquqvqyhvihivqhighuhmiiizqzhnxuhuhgixqpihigiuhvihivqhigpiikirivqyiuhwsuhpqvqsqzikirikhgiii"
buf += "kiyhvihivqhizhnxuhuhgixqpihigiuhmiiizqgpiikirivqyiuhwsuhpqvqsqzikirikhgiiikiyhmiiizqzhnxnxuhuhziqiuhmiiizqgpiikirivq"
buf += "yiuhwswsuhusuhvqyiiikinxuhuhuhuhsqiivqiqsqkiuhvihivqhinxuhuhiikivinxnxuhuhgixqpihigiuhmiiizqspzqvqiipquhwsuhpixqkiqq"
buf += "iisqvqpvvqsqzikirivvxqspzqvqiipqyhmiiizqzhnxuhuhgixqpihigiuhiikipisqzquqvqiivispzqvqiipquhwsuhpixqkiqqiisqvqypiiyqpv"
buf += "vqsqzikirivvxqspzqvqiipqyhvihivqhizhnxnxuhuhgixqpihigiuhvihivqhizpkivqhpsqsqhizquhwsuhpixqkiqqiisqvqspzqvqiipqvvxqiv"
buf += "zpkivqhpsqsqhizqyhiikipisqzquqvqiivispzqvqiipqghuhqihigipqiizhnxuhuhgixqpihigiuhmiiizqzpkivqhpsqsqhizquhwsuhpixqkiqq"
buf += "iisqvqspzqvqiipqvvxqivzpkivqhpsqsqhizqyhmiiizqspzqvqiipqghuhqihigipqiizhnxnxuhuhgixqpihigiuhviiipisqzquqvqiivizpkivq"
buf += "hpsqsqhizquhwsuhviiipisqzquqvqzpkivqhpsqsqhizqyhvihivqhizpkivqhpsqsqhizqghuhmiiizqzpkivqhpsqsqhizqzhnxuhuhgixqpihigi"
buf += "uhviiipisqzquqvqiivispzqvqiipquhwsuhpixqkiqqiisqvqivzpkivqhpsqsqhizqvvxqspzqvqiipqyhviiipisqzquqvqiivizpkivqhpsqsqhi"
buf += "zqghuhvqsqiqiizhnxuhuhgixqpihigiuhviiipisqzquqvqiivipvvqsqzikiriuhwsuhpixqkiqqiisqvqspzqvqiipqvvxqpvvqsqzikiriyhviii"
buf += "pisqzquqvqiivispzqvqiipqzhnxnxuhuhsqiivqiqsqkiuhviiipisqzquqvqiivipvvqsqzikirinxiikivinxnxwhwhwhwhwhwhwhwhwhwhwhwhwh"
buf += "whwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhnxwh"
buf += "whuhipkipisqzquqvqzixqkinxwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwh"
buf += "whwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhwhnxnx"
print(xingxiang(buf))
buf =  "qiiqkipivqzixqkiuhiikipisqzquqvqzpkivqhpsqsqhizqyhqqghuhmizhnxnxuhuhkiuhwsuhvqhisigiiikhriiivqkiyhqqzhnxuhuhziqiuhki"
buf += "uhgsuhssuhvqyiiikinxuhuhuhuhsqiivqiqsqkiuhqqnxuhuhiikivinxnxuhuhgixqpihigiuhnquhwsuhqqmvkiwvnxuhuhgixqpihigiuhzquhws"
buf += "uhqqmvhswvnxuhuhgixqpihigiuhpqiqwiuhwsuhusnxuhuhgixqpihigiuhiiuhwsuhusnxuhuhgixqpihigiuhuquhwsuhusnxuhuhgixqpihigiuh"
buf += "zikizivqhvuhwsuhqsuhmhuhwihivqyikhqigixqxqsqyhisssuhxsuhkizhnxnxuhuhqixqsquhhqwszikizivqhvghhsghwhhsuhvixqnxuhuhuhuh"
buf += "pqiqwiuhwsuhpixqkiqqiisqvqvvxqivzpkivqpsssyhpqiqwiuhmhuhviiigivqhizhmsnxuhuhuhuhiiuhwsuhsizivqkhsihikiviyhsizivqkhsi"
buf += "sqpqyiziqivqyhpqiqwighuhsszhghuhpszhmsnxuhuhuhuhqixqsquhuqwshsghyhkiwhhszhuhvixqnxuhuhuhuhuhuhzquhwsuhqqmvuquhmhuhhs"
buf += "wvmsnxuhuhuhuhuhuhqqmvuqwvuhwsuhpixqkiqqiisqvqvvxqivzpkivqpsssyhqqmvuqwvuhmhuhwiyqyhpqiqwighuhzqghuhnqghuhyhuqwhhszh"
buf += "ghuhiighuhmizhzhmsnxuhuhuhuhuhuhnquhwsuhqqmvuqwvnxuhuhuhuhiikivinxuhuhuhuhzquhwsuhqqmvhswvmsnxuhuhuhuhqqmvkiwvuhwsuh"
buf += "pixqkiqqiisqvqvvxqivzpkivqpsssyhqqmvkiwvuhmhuhwiyqyhpqiqwighuhzqghuhnqghuhyhkiwhhszhghuhiighuhmizhzhmsnxuhuhuhuhnquh"
buf += "wsuhqqmvkiwvnxuhuhiikivinxnxuhuhsqiivqiqsqkiuhqqmsnxnxiikivinxnxnxsiiqnqyizivihixquhwsuhrhkiriiqzqiikiqqziiivqyiiqki"
buf += "rihhusrszssspikirhnxmiiizqriiikiuhwsuhrhusrhnxipsvsvxvsvxihvivzpvvuhwsuhmqwqnxnx"
print(xingxiang(buf))
buf =  "qiiqkipivqzixqkiuhriiivqwphizikikphiwiiiyhuhpqvqsquhzhnxuhuhpqvqsquhwsuhrqpqvqsqvvxqivvqqiysyhpqvqsqzhnxuhuhgixqpihi"
buf += "giuhkihiwiiiuhwsuhpqvqsqnxuhuhgixqpihigiuhyquhwsuhpqvqsqzikirikhqizikiviyhpqvqsqghuhrhuprhzhnxuhuhziqiuhyquhkqwsuhki"
buf += "zigiuhvqyiiikinxuhuhuhuhkihiwiiiuhwsuhpqvqsqzikirikhpqiqsiyhpqvqsqghusghyqwhhszhnxuhuhiikivinxuhuhsqiivqiqsqkiuhiqvq"
buf += "qiysvvxqrvpqvqsqyhkihiwiiizhnxiikivinxnx"
print(xingxiang(buf))
buf =  "qiiqkipivqzixqkiuhpisqiihivqiixihiiqvqxqyhzhnxuhuhgixqpihigiuhvquhwsuhmqwqnxuhuhvqkhnpzihikippyihiuhwsuhqiiqkipivqzi"
buf += "xqkiuhyhzhnxuhuhuhuhgixqpihigiuhgixqrizikixiziviuhwsuhkiyqxiiiyqiipiiqvqiiyhrhqixqsqwixipqvqhiriiixigixqrizikigvgvqi"
buf += "xqsqwixigixqrizikirhghuhrhriiivqxigixqrizikixizivirhzhnxuhuhuhuhgixqpihigiuhzikiuqiqvqqqhisquhwsuhvqkhriiivqppxqviii"
buf += "hppivqziqqiiyhzhnxuhuhuhuhziqiuhzikiuqiqvqqqhisquhwswsuhkizigiuhxqsquhgixqrizikixiziviuhwswsuhkizigiuhvqyiiikiuhsqii"
buf += "vqiqsqkiuhqihigipqiiuhiikivinxuhuhuhuhgixqpihigiuhpqvqsqvvhisigiiiuhwsuhiqvqzigixipquqgizivqxipqvqsqzikiriyhkiyqxipq"
buf += "vqsqzikiriyhzikiuqiqvqqqhisqzhghuhrhghrhzhnxuhuhuhuhgixqpihigiuhzivighvqziwiiighkihiwiiinxuhuhuhuhziqiuhphpqvqsqvvhi"
buf += "sigiiiuhwswsuhpsuhvqyiiikinxuhuhuhuhuhuhziviuhwsuhpqvqsqvvhisigiiimvhswvnxuhuhuhuhuhuhvqziwiiiuhwsuhvqxqkiiqwisiiisq"
buf += "yhpqvqsqvvhisigiiimvsswvzhnxuhuhuhuhuhuhkihiwiiiuhwsuhkiyqxiqiiqkipivqzixqkiyhrhiiyqvqxiiqvqqiysxivqxqxirqziviiipqvq"
buf += "sqrhghuhpqvqsqvvhisigiiimvpswvzhnxuhuhuhuhiigipqiinxuhuhuhuhuhuhsqiivqiqsqkiuhqihigipqiinxuhuhuhuhiikivinxnxuhuhuhuh"
buf += "ziqiuhkihiwiiiuhkqwsuhvqkhriiivqppxqviiikphiwiiiyhzhuhvqyiiikinxuhuhuhuhuhuhsqiivqiqsqkiuhqihigipqiiuhnxuhuhuhuhiiki"
buf += "vinxnxuhuhuhuhgixqpihigiuhpiiqsqxivqziwiiiuhwsuhvqkhriiivqppiqsqvvziwiiiyhzhnxuhuhuhuhziqiuhpqvqsqzikirikhiququqiisq"
buf += "yhkiyqxipqvqsqzikiriyhgixqrizikixizivizhzhuhwswsuhpqvqsqzikirikhiququqiisqyhkiyqxipqvqsqzikiriyhzivizhzhuhhikiviuhpi"
buf += "iqsqxivqziwiiiuhgsuhvqziwiiiuhvqyiiikinxuhuhuhuhuhuhsqiivqiqsqkiuhvqsqiqiiuhnxuhuhuhuhiigipqiinxuhuhuhuhuhuhsqiivqiq"
buf += "sqkiuhqihigipqiiuhnxuhuhuhuhiikivinxuhuhiikivinxnxuhuhvqkhriiivqppxqviiikphiwiiiuhwsuhqiiqkipivqzixqkiuhyhzhnxuhuhuh"
buf += "uhgixqpihigiuhrihiwiiixipigiziiikivquhwsuhkiyqxiqqhigiiqiiyhrhrihiwiiixipigiziiikivqrhzhnxuhuhuhuhgixqpihigiuhpigizi"
buf += "iikivqxiuqgihizqiisquhwsuhrihiwiiixipigiziiikivqnsrpiivquvgihizqiisqyhzhnxuhuhuhuhziqiuhkixqvquhyhkiyqxizipqxiqqhigi"
buf += "ziviyhpigiziiikivqxiuqgihizqiisqzhzhuhvqyiiikinxuhuhuhuhuhuhsqiivqiqsqkiuhkiyqxirqziviiipqvqsqyhrhusrhzhnxuhuhuhuhii"
buf += "kivinxuhuhuhuhgixqpihigiuhuqgihizqiisqkphiwiiiuhwsuhpigiziiikivqxiuqgihizqiisqnshviqiisqzquvsqxquqyhrhkphiwiiirhzhnx"
buf += "uhuhuhuhsqiivqiqsqkiuhriiivqwphizikikphiwiiiyhkiyqxirqziviiipqvqsqyhuqgihizqiisqkphiwiiizhzhnxuhuhiikivinxnxuhuhvqkh"
buf += "riiivqppiqsqvvziwiiiuhwsuhqiiqkipivqzixqkiuhyhzhnxuhuhuhuhgixqpihigiuhwpiipqpqhiriiivpiigihizquhwsuhkiyqxiqqhigiiqii"
buf += "yhrhwpiipqpqhiriiivpiigihizqrhzhnxuhuhuhuhziqiuhkixqvquhyhkiyqxizipqxiqqhigiziviyhwpiipqpqhiriiivpiigihizqzhzhuhvqyi"
buf += "iikinxuhuhuhuhuhuhsqiivqiqsqkiuhusnxuhuhuhuhiikivinxuhuhuhuhsqiivqiqsqkiuhwpiipqpqhiriiivpiigihizqnsrpiivqpviisqqqii"
buf += "sqpviipixqkiviyhzhnxuhuhiikivinxnxuhuhvqkhriiivqppxqviiihppivqziqqiiuhwsuhqiiqkipivqzixqkiuhyhzhnxuhuhuhuhgixqpihigi"
buf += "uhgixqrizikixiziviuhwsuhkiyqxiiiyqiipiiqvqiiyhrhqixqsqwixipqvqhiriiixigixqrizikigvgvqixqsqwixigixqrizikirhghuhrhriii"
buf += "vqxigixqrizikixizivirhzhnxuhuhuhuhgixqpihigiuhqizigiiiuhwsuhkiyqxisqiipqxqiqsqpiiixiuqhivqyiyhzhuhkhkhuhrhhiiqvqxqzs"
buf += "zqzikigvgviqpqiisqgvgvrhuhkhkhuhgixqrizikixiziviuhkhkhuhrhkhzikizirhnxuhuhuhuhgixqpihigiuhpiyiiipimimiiizquhwsuhkiyq"
buf += "xipqvqsqzikiriyhzpkizisviihiviyhqizigiiighuhrhhpiqvqxqrhghuhrhmiiizqrhghuhrhusrhzhzhnxuhuhuhuhziqiuhpqvqsqzikirikhgi"
buf += "iikiyhpiyiiipimimiiizqzhuhksuhisuhvqyiiikiuhnxuhuhuhuhuhuhgixqpihigiuhmiiizquhwsuhviiipisqzquqvqyhpiyiiipimimiiizqgh"
buf += "uhsiiqnqyizivihixqzhnxuhuhuhuhuhuhsqiivqiqsqkiuhmiiizqnxuhuhuhuhiikivinxuhuhuhuhsqiivqiqsqkiuhusnxuhuhiikivinxnxnxnx"
buf += "nxnxnxnxuhuhgixqpihigiuhuqsqxqyqzquhwsuhmqwqnxuhuhgixqpihigiuhwivquhwsuhmquhuhuhuhuhuhuhwhwhuhpisqiihivqiiuhwiiivqhi"
buf += "vqhisigiiinxuhuhuhuhxixizikiviiiyquhwsuhvqghnxuhuhuhuhxixikiiirqzikiviiiyquhwsuhqiiqkipivqzixqkiuhyhvqghmighqqzhnxuh"
buf += "uhuhuhuhuhvqhisigiiikhzikipqiisqvqyhipsvsvxvsvxihvivzpvvghhszhnxuhuhuhuhiikivinxuhuhwqnxuhuhpqiivqwiiivqhivqhisigiii"
buf += "yhuqsqxqyqzqghuhwivqzhnxuhuhsqiivqiqsqkiuhuqsqxqyqzqnxiikivinxnx"
print(xingxiang(buf))
buf =  "qiiqkipivqzixqkiuhriiivqhpiqvqxqyhzhnxuhuhziqiuhhpiqvqxqzszvzikiuhwswsuhkizigiuhvqyiiikiuhnxuhuhuhuhhpiqvqxqzszvziki"
buf += "uhwsuhpisqiihivqiixihiiqvqxqyhzhuhnxuhuhuhuhkiyqxiuqhiiqpqiiyhsszhnxuhuhiikivinxuhuhsqiivqiqsqkiuhhpiqvqxqzszvzikinxiikivinxnx"
print(xingxiang(buf))
buf =  "qiiqkipivqzixqkiuhzipqgpxqrizikiyhuhkhkhkhuhzhnxuhuhgixqpihigiuhgixqrizikiuhwsuhkiyqxiqqhigiiqiiyhrhqixqsqwixipqvqhi"
buf += "riiixigixqrizikigvgvqixqsqwixigixqrizikirhzhnxuhuhziqiuhkiyqxizipqxiqqhigiziviyhgixqrizikizhuhhikiviuhgixqrizikikhqv"
buf += "zipqzisigiiiuhvqyiiikinxuhuhuhuhsqiivqiqsqkiuhvqsqiqiinxuhuhiikivinxuhuhsqiivqiqsqkiuhqihigipqiinxiikivinx"
print(xingxiang(buf))