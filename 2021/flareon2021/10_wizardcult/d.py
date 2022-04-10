from malduck import *

table = {b'Eldritch Blast': 0, b'Mass Heal': 1, b'Fireball': 2, b'Dominate Monster': 3, b'Detect Magic': 4, b'Stone Shape': 5, b'Clairvoyance': 6, b'Aid': 7, b'Detect Thoughts': 8, b'Shapechange': 9, b'Fire Shield': 10, b'Pass without Trace': 11, b'Antipathy/Sympathy': 12, b'Sleet Storm': 13, b'Dominate Person': 14, b'Tree Stride': 15, b'Passwall': 16, b'Shatter': 17, b'Giant Insect': 18, b'Revivify': 19, b'Circle of Death': 20, b'Divination': 21, b'Comprehend Languages': 22, b'Faerie Fire': 23, b'True Polymorph': 24, b'Searing Smite': 25, b'Dimension Door': 26, b'Shield': 27, b'Enlarge/Reduce': 28, b'Illusory Script': 29, b'Resistance': 30, b'Earthquake': 31, b'Contagion': 32, b'Bless': 33, b'Raise Dead': 34, b'Guidance': 35, b'Expeditious Retreat': 36, b'Grease': 37, b'Message': 38, b'Elemental Weapon': 39, b'Fear': 40, b'Clone': 41, b'Wrathful Smite': 42, b'Astral Projection': 43, b'Flaming Sphere': 44, b'Disguise Self': 45, b'Maze': 46, b'Slow': 47, b'Polymorph': 48, b'Weird': 49, b'Finger of Death': 50, b'Protection from Energy': 51, b'Nondetection': 52, b'Animal Friendship': 53, b'Spike Growth': 54, b'Goodberry': 55, b'Calm Emotions': 56, b'Antilife Shell': 57, b'Cone of Cold': 58, b'Identify': 59, b'Power Word Stun': 60, b'Control Water': 61, b'Thorn Whip': 62, b'Power Word Kill': 63, b'Blink': 64, b'Locate Creature': 65, b'Command': 66, b'Contingency': 67, b'Prismatic Wall': 68, b'Blade Ward': 69, b'Scrying': 70, b'Dominate Beast': 71, b'Sacred Flame': 72, b'Guards and Wards': 73, b'Arcane Eye': 74, b'Mirage Arcane': 75, b'Magic Mouth': 76, b'Glyph of Warding': 77, b'Friends': 78, b'Sending': 79, b'Stinking Cloud': 80, b'Compulsion': 81, b'Dancing Lights': 82, b'Darkness': 83, b'Invisibility': 84, b'Spare the Dying': 85, b'Wall of Fire': 86, b'Flame Blade': 87, b'Feather Fall': 88, b'Magic Weapon': 89, b'Purify Food and Drink': 90, b'Spirit Guardians': 91, b'Witch Bolt': 92, b'Animate Objects': 93, b'Gaseous Form': 94, b'Lightning Bolt': 95, b'Move Earth': 96, b'Disintegrate': 97, b'Mass Healing Word': 98, b'Meld into Stone': 99, b'Hellish Rebuke': 100, b'Aura of Life': 101, b'Augury': 102, b'Conjure Elemental': 103, b'Spider Climb': 104, b'Hold Person': 105, b'Project Image': 106, b'Heroism': 107, b'Crown of Madness': 108, b'Mirror Image': 109, b'Ray of Sickness': 110, b'Bane': 111, b'Wish': 112, b'Contact Other Plane': 113, b'Etherealness': 114, b'Blinding Smite': 115, b'Shield of Faith': 116, b'Vampiric Touch': 117, b'Shillelagh': 118, b'Programmed Illusion': 119, b'Remove Curse': 120, b'Major Image': 121, b'Insect Plague': 122, b'Color Spray': 123, b'Prismatic Spray': 124, b'Charm Person': 125, b'Arms of Hadar': 126, b'Dream': 127, b'Dissonant Whispers': 128, b'Teleport': 129, b'Dispel Magic': 130, b'Forbiddance': 131, b'Misty Step': 132, b'Cloud of Daggers': 133, b'Gentle Repose': 134, b'Phantasmal Force': 135, b'Circle of Power': 136, b'Stoneskin': 137, b'Sunbeam': 138, b'Fire Storm': 139, b'Gust of Wind': 140, b'Find Steed': 141, b'Druidcraft': 142, b'Confusion': 143, b'Bestow Curse': 144, b'Flesh to Stone': 145, b'Arcane Gate': 146, b'Ray of Frost': 147, b'Greater Invisibility': 148, b'Regenerate': 149, b'Burning Hands': 150, b'Wall of Ice': 151, b'True Strike': 152, b'Silence': 153, b'Banishing Smite': 154, b'Commune with Nature': 155, b'Time Stop': 156, b'Conjure Celestial': 157, b'Magic Jar': 158, b'True Seeing': 159, b'Transport via Plants': 160, b'Teleportation Circle': 161, b'Spiritual Weapon': 162, b'Prayer of Healing': 163, b'Awaken': 164, b'Conjure Woodland Beings': 165, b'Cloudkill': 166, b'Imprisonment': 167, b'Branding Smite': 168, b'Ray of Enfeeblement': 169, b'See Invisibility': 170, b'Word of Recall': 171, b'Silent Image': 172, b'Eyebite': 173, b'Cordon of Arrows': 174, b'Globe of Invulnerability': 175, b'Wind Walk': 176, b'Continual Flame': 177, b'Power Word Heal': 178, b'Web': 179, b'Protection from Poison': 180, b'Grasping Vine': 181, b'Telekinesis': 182, b'Heat Metal': 183, b'Harm': 184, b'Antimagic Field': 185, b'Jump': 186, b'Greater Restoration': 187, b'Chain Lightning': 188, b'Knock': 189, b'Blade Barrier': 190, b'Scorching Ray': 191, b'Zone of Truth': 192, b'Moonbeam': 193, b'Light': 194, b'Magic Circle': 195, b'Hail of Thorns': 196, b'Heal': 197, b'Blur': 198, b'Water Breathing': 199, b'Cure Wounds': 200, b'Enhance Ability': 201, b'Suggestion': 202, b'Water Walk': 203, b'Conjure Barrage': 204, b'Arcane Lock': 205, b'Reverse Gravity': 206, b'Planar Ally': 207, b'Mass Suggestion': 208, b'False Life': 209, b'Longstrider': 210, b'Detect Evil and Good': 211, b'Guiding Bolt': 212, b'Glibness': 213, b'Speak with Dead': 214, b'Call Lightning': 215, b'Death Ward': 216, b'Create Undead': 217, b'Beacon of Hope': 218, b'Alter Self': 219, b'Acid Splash': 220, b'Phantom Steed': 221, b'Planar Binding': 222, b'Prestidigitation': 223, b'Animate Dead': 224, b'Mind Blank': 225, b'Sleep': 226, b'Divine Favor': 227, b'Telepathy': 228, b'Vicious Mockery': 229, b'Blight': 230, b'Barkskin': 231, b'Counterspell': 232, b'Conjure Fey': 233, b'Find Traps': 234, b'Animal Shapes': 235, b'Speak with Plants': 236, b'True Resurrection': 237, b'Warding Bond': 238, b'Flame Strike': 239, b'Healing Word': 240, b'Wall of Thorns': 241, b'Wind Wall': 242, b'Seeming': 243, b'Chill Touch': 244, b'Lesser Restoration': 245, b'Guardian of Faith': 246, b'Meteor Swarm': 247, b'Shocking Grasp': 248, b'Commune': 249, b'Destructive Wave': 250, b'Staggering Smite': 251, b'Create or Destroy Water': 252, b'Sunburst': 253, b'Forcecage': 254, b'Tongues': 255, b'Legend Lore': 256, b'Find Familiar': 257, b'Thaumaturgy': 258, b'Incendiary Cloud': 259, b'Storm of Vengeance': 260, b'Holy Aura': 261, b'Levitate': 262, b'Inflict Wounds': 263, b'Compelled Duel': 264, b'Haste': 265, b'Resurrection': 266, b'Feign Death': 267, b'Delayed Blast Fireball': 268, b'Armor of Agathys': 269, b'Reincarnate': 270, b'Thunderous Smite': 271, b'Protection from Evil and Good': 272, b'Hex': 273, b'Lightning Arrow': 274, b'Find the Path': 275, b'Modify Memory': 276, b'Simulacrum': 277, b'Mage Armor': 278, b'Demiplane': 279, b'Hunger of Hadar': 280, b'Tsunami': 281, b'Speak with Animals': 282, b'Produce Flame': 283, b'Animal Messenger': 284, b'Hypnotic Pattern': 285, b'Mending': 286, b'Darkvision': 287, b'Gate': 288, b'Freedom of Movement': 289, b'Plant Growth': 290, b'Banishment': 291, b'Fire Bolt': 292, b'Aura of Vitality': 293, b'Wall of Stone': 294, b'Magic Missile': 295, b'Fly': 296, b'Conjure Animals': 297, b'Fog Cloud': 298, b'Sequester': 299, b'Detect Poison and Disease': 300, b'Aura of Purity': 301, b'Enthrall': 302, b'Beast Sense': 303, b'Ensnaring Strike': 304, b'Blindness/Deafness': 305, b'Fabricate': 306, b'Foresight': 307, b'Conjure Volley': 308, b'Symbol': 309, b'Control Weather': 310, b'Alarm': 311, b'Dispel Evil and Good': 312, b'Mislead': 313, b'Create Food and Water': 314, b'Locate Object': 315, b'Chromatic Orb': 316, b'Entangle': 317, b'Geas': 318, b'Locate Animals or Plants': 319, b'Rope Trick': 320, b'Hold Monster': 321, b'Poison Spray': 322, b'Sanctuary': 323, b'Swift Quiver': 324, b'Mage Hand': 325, b'Ice Storm': 326, b'Plane Shift': 327, b'Minor Illusion': 328, b'Divine Word': 329, b'Phantasmal Killer': 330, b'Creation': 331, b'Wall of Force': 332, b'Conjure Minor Elementals': 333, b'Mass Cure Wounds': 334, b'Hallucinatory Terrain': 335, b'Feeblemind': 336, b'Unseen Servant': 337, b'Daylight': 338, b'Thunderwave': 339, b'Hallow': 340}

spells_1 = open("spells_1.txt", "r").readlines()
out_1 = b""
for line in spells_1:
    line = line[25:]
    spell_name = line.split(' on the ')[0].encode()
    out_1 += p8(table[spell_name] ^ 162)
    if ' damage!' in line:
        dmg =  line.split(' on the ')[1].split(' for ')[1].split(' damage!')[0].split('d')
        out_1 += p8(int(dmg[0]) ^ 162)
        out_1 += p8(int(dmg[1]) ^ 162)
print(out_1)

rom_0 = [90, 132, 6, 69, 174, 203, 232, 243, 87, 254, 166, 61, 94, 65, 8, 208, 51, 34, 33, 129, 32, 221, 0, 160, 35, 175, 113, 4, 139, 245, 24, 29, 225, 15, 101, 9, 206, 66, 120, 62, 195, 55, 202, 143, 100, 50, 224, 172, 222, 145, 124, 42, 192, 7, 244, 149, 159, 64, 83, 229, 103, 182, 122, 82, 78, 63, 131, 75, 201, 130, 114, 46, 118, 28, 241, 30, 204, 183, 215, 199, 138, 16, 121, 26, 77, 25, 53, 22, 125, 67, 43, 205, 134, 171, 68, 146, 212, 14, 152, 20]
rom_1 = [185, 155, 167, 36, 27, 60, 226, 58, 211, 240, 253, 79, 119, 209, 163, 12, 72, 128, 106, 218, 189, 216, 71, 91, 250, 150, 11, 236, 207, 73, 217, 17, 127, 177, 39, 231, 197, 178, 99, 230, 40, 54, 179, 93, 251, 220, 168, 112, 37, 246, 176, 156, 165, 95, 184, 57, 228, 133, 169, 252, 19, 2, 81, 48, 242, 105, 255, 116, 191, 89, 181, 70, 23, 194, 88, 97, 153, 235, 164, 158, 137, 238, 108, 239, 162, 144, 115, 140, 84, 188, 109, 219, 44, 214, 227, 161, 141, 80, 247, 52]
rom_2 = [213, 249, 1, 123, 142, 190, 104, 107, 85, 157, 45, 237, 47, 147, 21, 31, 196, 136, 170, 248, 13, 92, 234, 86, 3, 193, 154, 56, 5, 111, 98, 74, 18, 223, 96, 148, 41, 117, 126, 173, 233, 10, 49, 180, 187, 186, 135, 59, 38, 210, 110, 102, 200, 76, 151, 198]
rom_3 = [97, 49, 49, 95, 109, 89, 95, 104, 111, 109, 49, 101, 115, 95, 104, 52, 116, 51, 95, 98, 52, 114, 100, 115]

spells_brute = open("spells_brute.txt", "r").readlines()
out_brute = b""
for line in spells_brute:
    line = line[14:]
    spell_name = line.split(' on the ')[0].encode()
    out_brute += p8(table[spell_name])
    if ' damage!' in line:
        dmg =  line.split(' on the ')[1].split(' for ')[1].split(' damage!')[0].split('d')
        out_brute += p8(int(dmg[0]))
        out_brute += p8(int(dmg[1]))

brute_map = [[] for i in range(24)]
for i in range(len(out_brute)):
    brute_map[i%24].append(out_brute[i])

spells_2 = open("spells_2.txt", "r").readlines()
out_2 = b""
cnt = 0
for line in spells_2:
    if len(line) < 25:
        continue
    line = line[25:]
    spell_name = line.split(' on the ')[0].encode()
    out_2 += p8(brute_map[cnt%24].index(table[spell_name]))
    cnt += 1
    if ' damage!' in line:
        dmg =  line.split(' on the ')[1].split(' for ')[1].split(' damage!')[0].split('d')
        out_2 += p8(brute_map[cnt%24].index(int(dmg[0])))
        cnt += 1
        out_2 += p8(brute_map[cnt%24].index(int(dmg[1])))
        cnt += 1

open("cool_wizard_meme.png", "wb").write(out_2)