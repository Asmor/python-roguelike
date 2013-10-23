import pygame
import pygame.locals

def load_tile_table(filename, width, height):
	image = pygame.image.load(filename).convert()
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
_table = load_tile_table("images/oryx_16bit_fantasy_world_trans.png", TILE_WIDTH, TILE_HEIGHT)

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
		# tiles[tileStyle][tileType] = (col, row)
		tiles[tileStyle][tileType] = _table[col][row]
		# print("Assigned %s-%s: (%d, %d)" % (tileStyle, tileType, col, row))

# # tileStyleIndex = getRandom(1, len(Tiles.tileStyles))
# tileStyleIndex = getRandom(1, 15)
# tileStyle = Tiles.tileStyles[tileStyleIndex]
# for x in range(FIELD_WIDTH):
# 	for y in range(FIELD_HEIGHT):
# 		if field[y][x] == "#":
# 			up = 0
# 			down = 0
# 			left = 0
# 			right = 0
# 			if y-1 >= 0 and field[y-1][x] == "#":
# 				up = 1
# 			if y+1 < FIELD_HEIGHT and field[y+1][x] == "#":
# 				down = 1
# 			if x-1 >= 0 and field[y][x-1] == "#":
# 				left = 1
# 			if x+1 < FIELD_WIDTH and field[y][x+1] == "#":
# 				right = 1
# 			style = Tiles.wallTypes[up][right][down][left]
# 		else:
# 			style = "floor-1"
# 		tileLocation = Tiles.tiles[tileStyle][style];
# 		screen.blit(table[tileLocation[0]][tileLocation[1]], (x*TILE_WIDTH, y*TILE_HEIGHT))
# pygame.display.flip()
# done = False
# while not done:
# 	for event in pygame.event.get():
# 		if event.type in [KEYDOWN, QUIT, JOYBUTTONDOWN]:
# 			done = True