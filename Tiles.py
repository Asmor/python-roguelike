import pygame
import pygame.locals

def load_tile_table(filename, width, height):
	image = pygame.image.load(filename).convert()
	black = (0, 0, 0)
	image.set_colorkey(black)
	image_width, image_height = image.get_size()
	tile_table = []
	for tile_x in range(0, int(image_width/width)):
		line = []
		tile_table.append(line)
		for tile_y in range(0, int(image_height/height)):
			rect = (tile_x*width, tile_y*height, width, height)
			line.append(image.subsurface(rect))
	return tile_table

# Needed for .Convert()
pygame.init()
pygame.display.set_mode((1,1))

TILE_WIDTH	= 24
TILE_HEIGHT	= 24
_terrain_table = load_tile_table("images/oryx_16bit_fantasy_world.png", TILE_WIDTH, TILE_HEIGHT)


tileTypes = (
	"blank",
	"filled",
	"filled-cracked",
	"filled-cracked-heavy",
	"floor-1",
	"floor-2",
	"floor-3",
	"floor-4",
	"stairs-up",
	"stairs-down",
	"pillar",
	"cap-left",
	"connector-I-horizontal",
	"cap-right",
	"cap-up",
	"connector-I-vertical",
	"cap-down",
	"connector-L-right-down",
	"connector-L-left-down",
	"connector-L-right-up",
	"connector-L-left-up",
	"connector-cross",
	"connector-T-down",
	"connector-T-left",
	"connector-T-right",
	"connector-T-up",
	"connector-I-vertical-damaged",
	"connector-I-horizontal-damaged"
)

tileStyles = (
	"blank",
	"grey",
	"grey-cracked",
	"brown-disrepair",
	"brown-pyramids",
	"brown-fancy",
	"green-fancy",
	"aqua-disrepair",
	"blue-disrepair",
	"yellow",
	"grey-worked",
	"green",
	"tan",
	"overgrown",
	"orange-rock",
	"green-hedge",
	"white-snow",
	"fence",
	"grey-disrepair",
	"grey-dilapidated",
	"light-tan",
	"light-tain-ruins",
	"grey-ruins",
	"red-ruins"
)

tiles = {}

wallTypes = \
	[ # Top
		[ # Right
			[ # Bottom
				[ # Left
					"" for i in range(2)
				] for i in range(2)
			] for i in range(2)
		] for i in range(2)
	]

# wallTypes[0][0][0][0] = "pillar"
wallTypes[0][0][0][0] = "filled"

wallTypes[0][0][1][0] = "cap-up"
wallTypes[0][0][0][1] = "cap-right"
wallTypes[1][0][0][0] = "cap-down"
wallTypes[0][1][0][0] = "cap-left"

wallTypes[1][0][1][0] = "connector-I-vertical"
wallTypes[0][1][0][1] = "connector-I-horizontal"

wallTypes[1][1][0][0] = "connector-L-right-up"
wallTypes[0][1][1][0] = "connector-L-right-down"
wallTypes[0][0][1][1] = "connector-L-left-down"
wallTypes[1][0][0][1] = "connector-L-left-up"

wallTypes[1][1][0][1] = "connector-T-up"
wallTypes[1][1][1][0] = "connector-T-right"
wallTypes[1][0][1][1] = "connector-T-left"
wallTypes[0][1][1][1] = "connector-T-down"

wallTypes[1][1][1][1] = "connector-cross"

for row, tileStyle in enumerate(tileStyles):
	if row == 0:
		continue
	tiles[tileStyle] = {}
	for col, tileType in enumerate(tileTypes):
		if col == 0:
			continue
		tiles[tileStyle][tileType] = _terrain_table[col][row]

# These features start on column 29
features = {}
features["door-wooden-closed"] = _terrain_table[29][3]
features["stairs-up-red-carpet"] = _terrain_table[8][2]
features["stairs-down-red-carpet"] = _terrain_table[9][2]

_mob_table = load_tile_table("images/oryx_16bit_fantasy_creatures.png", TILE_WIDTH, TILE_HEIGHT)

mobs = {
	"knight-m":                  (_mob_table[1][1],   _mob_table[1][2]),
	"thief-m":                   (_mob_table[2][1],   _mob_table[2][2]),
	"ranger-m":                  (_mob_table[3][1],   _mob_table[3][2]),
	"wizard-m":                  (_mob_table[4][1],   _mob_table[4][2]),
	"priest-m":                  (_mob_table[5][1],   _mob_table[5][2]),
	"shaman-m":                  (_mob_table[6][1],   _mob_table[6][2]),
	"berserker-m":               (_mob_table[7][1],   _mob_table[7][2]),
	"swordsman-m":               (_mob_table[8][1],   _mob_table[8][2]),
	"paladin-m":                 (_mob_table[9][1],   _mob_table[9][2]),
	"knight-f":                  (_mob_table[10][1],  _mob_table[10][2]),
	"thief-f":                   (_mob_table[11][1],  _mob_table[11][2]),
	"ranger-f":                  (_mob_table[12][1],  _mob_table[12][2]),
	"wizard-f":                  (_mob_table[13][1],  _mob_table[13][2]),
	"priest-f":                  (_mob_table[14][1],  _mob_table[14][2]),
	"shaman-f":                  (_mob_table[15][1],  _mob_table[15][2]),
	"berserker-f":               (_mob_table[16][1],  _mob_table[16][2]),
	"swordsman-f":               (_mob_table[17][1],  _mob_table[17][2]),
	"paladin-f":                 (_mob_table[18][1],  _mob_table[18][2]),
	"bandit":                    (_mob_table[1][3],   _mob_table[1][4]),
	"hooded-human":              (_mob_table[2][3],   _mob_table[2][4]),
	"human-m":                   (_mob_table[3][3],   _mob_table[3][4]),
	"human-f":                   (_mob_table[4][3],   _mob_table[4][4]),
	"merchant":                  (_mob_table[5][3],   _mob_table[5][4]),
	"butcher":                   (_mob_table[6][3],   _mob_table[6][4]),
	"chef":                      (_mob_table[7][3],   _mob_table[7][4]),
	"bishop":                    (_mob_table[8][3],   _mob_table[8][4]),
	"king":                      (_mob_table[9][3],   _mob_table[9][4]),
	"queen":                     (_mob_table[10][3],  _mob_table[10][4]),
	"prince":                    (_mob_table[11][3],  _mob_table[11][4]),
	"princess":                  (_mob_table[12][3],  _mob_table[12][4]),
	"guard-m":                   (_mob_table[13][3],  _mob_table[13][4]),
	"guard-f":                   (_mob_table[14][3],  _mob_table[14][4]),
	"knight":                    (_mob_table[15][3],  _mob_table[15][4]),
	"guard-alt-m":               (_mob_table[16][3],  _mob_table[16][4]),
	"guard-alt-f":               (_mob_table[17][3],  _mob_table[17][4]),
	"knight-alt":                (_mob_table[18][3],  _mob_table[18][4]),
	"bandit":                    (_mob_table[1][5],   _mob_table[1][6]),
	"hooded-human":              (_mob_table[2][5],   _mob_table[2][6]),
	"human-m":                   (_mob_table[3][5],   _mob_table[3][6]),
	"human-f":                   (_mob_table[4][5],   _mob_table[4][6]),
	"merchant":                  (_mob_table[5][5],   _mob_table[5][6]),
	"slave":                     (_mob_table[6][5],   _mob_table[6][6]),
	"alchemist":                 (_mob_table[7][5],   _mob_table[7][6]),
	"prophet":                   (_mob_table[8][5],   _mob_table[8][6]),
	"king":                      (_mob_table[9][5],   _mob_table[9][6]),
	"queen":                     (_mob_table[10][5],  _mob_table[10][6]),
	"prince":                    (_mob_table[11][5],  _mob_table[11][6]),
	"princess":                  (_mob_table[12][5],  _mob_table[12][6]),
	"guard-m":                   (_mob_table[13][5],  _mob_table[13][6]),
	"guard-f":                   (_mob_table[14][5],  _mob_table[14][6]),
	"knight":                    (_mob_table[15][5],  _mob_table[15][6]),
	"guard-alt-m":               (_mob_table[16][5],  _mob_table[16][6]),
	"guard-alt-f":               (_mob_table[17][5],  _mob_table[17][6]),
	"knight-alt":                (_mob_table[18][5],  _mob_table[18][6]),
	"assassin":                  (_mob_table[1][7],   _mob_table[1][8]),
	"bandit":                    (_mob_table[2][7],   _mob_table[2][8]),
	"dwarf":                     (_mob_table[3][7],   _mob_table[3][8]),
	"dwarf-alt":                 (_mob_table[4][7],   _mob_table[4][8]),
	"dwarf-priest":              (_mob_table[5][7],   _mob_table[5][8]),
	"drow-assassin":             (_mob_table[6][7],   _mob_table[6][8]),
	"drow-fighter":              (_mob_table[7][7],   _mob_table[7][8]),
	"drow-ranger":               (_mob_table[8][7],   _mob_table[8][8]),
	"drow-mage":                 (_mob_table[9][7],   _mob_table[9][8]),
	"drow-sorceress":            (_mob_table[10][7],  _mob_table[10][8]),
	"high-elf-fighter-m":        (_mob_table[11][7],  _mob_table[11][8]),
	"high-elf-shield-fighter-m": (_mob_table[12][7],  _mob_table[12][8]),
	"high-elf-ranger-m":         (_mob_table[13][7],  _mob_table[13][8]),
	"high-elf-mage-m":           (_mob_table[14][7],  _mob_table[14][8]),
	"high-elf-fighter-f":        (_mob_table[15][7],  _mob_table[15][8]),
	"high-elf-shield-fighter-f": (_mob_table[16][7],  _mob_table[16][8]),
	"high-elf-ranger-f":         (_mob_table[17][7],  _mob_table[17][8]),
	"high-elf-mage-f":           (_mob_table[18][7],  _mob_table[18][8]),
	"wood-elf-fighter-m":        (_mob_table[1][9],   _mob_table[1][10]),
	"wood-elf-shield-fighter-m": (_mob_table[2][9],   _mob_table[2][10]),
	"wood-elf-ranger-m":         (_mob_table[3][9],   _mob_table[3][10]),
	"wood-elf-druid-m":          (_mob_table[4][9],   _mob_table[4][10]),
	"wood-elf-fighter-f":        (_mob_table[5][9],   _mob_table[5][10]),
	"wood-elf-shield-fighter-f": (_mob_table[6][9],   _mob_table[6][10]),
	"wood-elf-ranger-f":         (_mob_table[7][9],   _mob_table[7][10]),
	"wood-elf-druid-f":          (_mob_table[8][9],   _mob_table[8][10]),
	"lizardman-warrior":         (_mob_table[9][9],   _mob_table[9][10]),
	"lizardman-archer":          (_mob_table[10][9],  _mob_table[10][10]),
	"lizardman-captain":         (_mob_table[11][9],  _mob_table[11][10]),
	"lizardman-shaman":          (_mob_table[12][9],  _mob_table[12][10]),
	"lizardman-high-shaman":     (_mob_table[13][9],  _mob_table[13][10]),
	"gnome-fighter":             (_mob_table[14][9],  _mob_table[14][10]),
	"gnome-fighter-alt":         (_mob_table[15][9],  _mob_table[15][10]),
	"gnome-fighter-alt":         (_mob_table[16][9],  _mob_table[16][10]),
	"gnome-wizard":              (_mob_table[17][9],  _mob_table[17][10]),
	"gnome-wizard-alt":          (_mob_table[18][9],  _mob_table[18][10]),
	"gnoll-fighter":             (_mob_table[1][11],  _mob_table[1][12]),
	"gnoll-fighter-alt":         (_mob_table[2][11],  _mob_table[2][12]),
	"gnoll-fighter-captain":     (_mob_table[3][11],  _mob_table[3][12]),
	"gnoll-shaman":              (_mob_table[4][11],  _mob_table[4][12]),
	"minotaur-axe":              (_mob_table[5][11],  _mob_table[5][12]),
	"minotaur-club":             (_mob_table[6][11],  _mob_table[6][12]),
	"minotaur-alt":              (_mob_table[7][11],  _mob_table[7][12]),
	"elder-demon":               (_mob_table[8][11],  _mob_table[8][12]),
	"fire-demon":                (_mob_table[9][11],  _mob_table[9][12]),
	"horned-demon":              (_mob_table[10][11], _mob_table[10][12]),
	"stone-golem":               (_mob_table[11][11], _mob_table[11][12]),
	"mud-golem":                 (_mob_table[12][11], _mob_table[12][12]),
	"flesh-golem":               (_mob_table[13][11], _mob_table[13][12]),
	"lava-golem":                (_mob_table[14][11], _mob_table[14][12]),
	"bone-golem":                (_mob_table[15][11], _mob_table[15][12]),
	"djinn":                     (_mob_table[16][11], _mob_table[16][12]),
	"treant":                    (_mob_table[17][11], _mob_table[17][12]),
	"mimic":                     (_mob_table[18][11], _mob_table[18][12]),
	"purple-slime":              (_mob_table[1][13],  _mob_table[1][14]),
	"green-slime":               (_mob_table[2][13],  _mob_table[2][14]),
	"black-bat":                 (_mob_table[3][13],  _mob_table[3][14]),
	"red-bat":                   (_mob_table[4][13],  _mob_table[4][14]),
	"beholder":                  (_mob_table[5][13],  _mob_table[5][14]),
	"red-spider":                (_mob_table[6][13],  _mob_table[6][14]),
	"black-spider":              (_mob_table[7][13],  _mob_table[7][14]),
	"grey-rat":                  (_mob_table[8][13],  _mob_table[8][14]),
	"brown-rat":                 (_mob_table[9][13],  _mob_table[9][14]),
	"cobra":                     (_mob_table[10][13], _mob_table[10][14]),
	"beetle":                    (_mob_table[11][13], _mob_table[11][14]),
	"fire-beetle":               (_mob_table[12][13], _mob_table[12][14]),
	"grey-wolf":                 (_mob_table[13][13], _mob_table[13][14]),
	"brown-wolf":                (_mob_table[14][13], _mob_table[14][14]),
	"black-wolf":                (_mob_table[15][13], _mob_table[15][14]),
	"dove/pigeon":               (_mob_table[16][13], _mob_table[16][14]),
	"blue-bird":                 (_mob_table[17][13], _mob_table[17][14]),
	"crow/raven":                (_mob_table[18][13], _mob_table[18][14]),
	"goblin-fighter":            (_mob_table[1][15],  _mob_table[1][16]),
	"goblin-archer":             (_mob_table[2][15],  _mob_table[2][16]),
	"goblin-captain":            (_mob_table[3][15],  _mob_table[3][16]),
	"goblin-king":               (_mob_table[4][15],  _mob_table[4][16]),
	"goblin-mystic":             (_mob_table[5][15],  _mob_table[5][16]),
	"orc-fighter":               (_mob_table[6][15],  _mob_table[6][16]),
	"orc-captain":               (_mob_table[7][15],  _mob_table[7][16]),
	"orc-mystic":                (_mob_table[8][15],  _mob_table[8][16]),
	"troll":                     (_mob_table[9][15],  _mob_table[9][16]),
	"troll-captain":             (_mob_table[10][15], _mob_table[10][16]),
	"cycops":                    (_mob_table[11][15], _mob_table[11][16]),
	"cyclops-alt":               (_mob_table[12][15], _mob_table[12][16]),
	"death-knight":              (_mob_table[13][15], _mob_table[13][16]),
	"death-knight-alt":          (_mob_table[14][15], _mob_table[14][16]),
	"death-knight-alt":          (_mob_table[15][15], _mob_table[15][16]),
	"earth-elemental":           (_mob_table[16][15], _mob_table[16][16]),
	"ice/water-elemental":       (_mob_table[17][15], _mob_table[17][16]),
	"air-elemental":             (_mob_table[18][15], _mob_table[18][16]),
	"zombie":                    (_mob_table[1][17],  _mob_table[1][18]),
	"headless-zombie":           (_mob_table[2][17],  _mob_table[2][18]),
	"skeleton":                  (_mob_table[3][17],  _mob_table[3][18]),
	"skeleton-archer":           (_mob_table[4][17],  _mob_table[4][18]),
	"skeleton-warrior":          (_mob_table[5][17],  _mob_table[5][18]),
	"shadow":                    (_mob_table[6][17],  _mob_table[6][18]),
	"ghost":                     (_mob_table[7][17],  _mob_table[7][18]),
	"mummy":                     (_mob_table[8][17],  _mob_table[8][18]),
	"pharoah":                   (_mob_table[9][17],  _mob_table[9][18]),
	"necromancer":               (_mob_table[10][17], _mob_table[10][18]),
	"dark-wizard":               (_mob_table[11][17], _mob_table[11][18]),
	"death":                     (_mob_table[12][17], _mob_table[12][18]),
	"vampire":                   (_mob_table[13][17], _mob_table[13][18]),
	"vampire-alt":               (_mob_table[14][17], _mob_table[14][18]),
	"vampire-lord":              (_mob_table[15][17], _mob_table[15][18]),
	"witch":                     (_mob_table[16][17], _mob_table[16][18]),
	"frost-witch":               (_mob_table[17][17], _mob_table[17][18]),
	"green-witch":               (_mob_table[18][17], _mob_table[18][18]),
	"red-dragon":                (_mob_table[1][19],  _mob_table[1][20]),
	"purple-dragon":             (_mob_table[2][19],  _mob_table[2][20]),
	"gold-dragon":               (_mob_table[3][19],  _mob_table[3][20]),
	"green-dragon":              (_mob_table[4][19],  _mob_table[4][20]),
	"yeti":                      (_mob_table[5][19],  _mob_table[5][20]),
	"yeti-alt":                  (_mob_table[6][19],  _mob_table[6][20]),
	"giant-leech":               (_mob_table[7][19],  _mob_table[7][20]),
	"giant-worm":                (_mob_table[8][19],  _mob_table[8][20]),
	"brown-bear":                (_mob_table[9][19],  _mob_table[9][20]),
	"grey-bear":                 (_mob_table[10][19], _mob_table[10][20]),
	"polar-bear":                (_mob_table[11][19], _mob_table[11][20]),
	"giant-scorpion":            (_mob_table[12][19], _mob_table[12][20]),
	"scorpion-alt":              (_mob_table[13][19], _mob_table[13][20]),
	"scorpion-alt":              (_mob_table[14][19], _mob_table[14][20]),
	"ettin":                     (_mob_table[15][19], _mob_table[15][20]),
	"ettin-alt":                 (_mob_table[16][19], _mob_table[16][20]),
	"pixie/fairy/sprite":        (_mob_table[17][19], _mob_table[17][20]),
	"imp/demon/devil":           (_mob_table[18][19], _mob_table[18][20]),
	"wisp":                      (_mob_table[1][21],  _mob_table[1][22]),
	"wisp-alt":                  (_mob_table[2][21],  _mob_table[2][22]),
	"turnip":                    (_mob_table[3][21],  _mob_table[3][22]),
	"rotten-turnip":             (_mob_table[4][21],  _mob_table[4][22]),
	"fire-minion":               (_mob_table[5][21],  _mob_table[5][22]),
	"ice-minion":                (_mob_table[6][21],  _mob_table[6][22]),
	"smoke-minion":              (_mob_table[7][21],  _mob_table[7][22]),
	"mud-minion":                (_mob_table[8][21],  _mob_table[8][22]),
	"eye":                       (_mob_table[9][21],  _mob_table[9][22]),
	"eyes":                      (_mob_table[10][21], _mob_table[10][22]),
	"red-specter":               (_mob_table[11][21], _mob_table[11][22]),
	"blue-specter":              (_mob_table[12][21], _mob_table[12][22]),
	"brown-specter":             (_mob_table[13][21], _mob_table[13][22]),
	"blue-jelly":                (_mob_table[14][21], _mob_table[14][22]),
	"green-jelly":               (_mob_table[15][21], _mob_table[15][22]),
	"red-jelly":                 (_mob_table[16][21], _mob_table[16][22]),
	"flame":                     (_mob_table[17][21], _mob_table[17][22]),
	"cold-flame":                (_mob_table[18][21], _mob_table[18][22])
}