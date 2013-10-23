import Cell
import Tiles
import Util

class Level:
	"""A dungeon level"""
	def __init__(self, width, height):
		self.style = "grey"
		self.width = width
		self.height = height
		self.cells = [[Cell.Cell() for i in range(width)] for i in range(height)]
		for y, row in enumerate(self.cells):
			for x, cell in enumerate(row):
				self._setCellStyle(x, y)
	def _setCellStyle(self, x, y):
			if self.cells[y][x].base == "#":
				up = 0
				down = 0
				left = 0
				right = 0
				if y-1 >= 0 and self.cells[y-1][x].base == "#":
					up = 1
				if y+1 < self.height and self.cells[y+1][x].base == "#":
					down = 1
				if x-1 >= 0 and self.cells[y][x-1].base == "#":
					left = 1
				if x+1 < self.width and self.cells[y][x+1].base == "#":
					right = 1
				self.cells[y][x].fillType = Tiles.wallTypes[up][right][down][left]
			else:
				self.cells[y][x].fillType = "floor-1"
	def setCell(self, x, y, how):
		self.cells[y][x].set(how)
		self._setCellStyle(x, y)
		if y-1 >= 0:
			self._setCellStyle(x, y-1)
		if y+1 < self.height:
			self._setCellStyle(x, y+1)
		if x-1 >= 0:
			self._setCellStyle(x-1, y)
		if x+1 < self.width:
			self._setCellStyle(x+1, y)
	def getCellFillType(self, x, y):
		return self.cells[y][x].fillType


def MakeRoom(width, height):
	room = [["." for i in range(width+2)] for i in range(height+2)]
	right = width+1
	bottom = height+1
	for x in range(0, right+1):
		room[0][x] = "#"
		room[bottom][x] = "#"
	for y in range(0, bottom+1):
		room[y][0] = "#"
		room[y][right] = "#"
	return room

# Test MakeRoom
if __name__=='__main__' and True:
	level = Level(10, 5)
	room = MakeRoom(3,2)
	for i in room:
		print("".join(i))

# Test the Level class
if __name__=='__main__' and True:
	import pygame
	from pygame.locals import *
	pygame.init()
	FIELD_WIDTH = 30
	FIELD_HEIGHT = 20
	screen = pygame.display.set_mode((FIELD_WIDTH * Tiles.TILE_WIDTH, FIELD_HEIGHT * Tiles.TILE_HEIGHT))
	screen.fill((255, 255, 255))
	level = Level(FIELD_WIDTH, FIELD_HEIGHT)
	level.style = Tiles.tileStyles[Util.getRandom(1, 15)]
	for x in range(level.width):
		for y in range(level.height):
			screen.blit(Tiles.tiles[level.style][level.getCellFillType(x, y)], (x*Tiles.TILE_WIDTH, y*Tiles.TILE_HEIGHT))
	pygame.display.flip()
	done = False
	while not done:
		for event in pygame.event.get():
			if event.type in [KEYDOWN, QUIT, JOYBUTTONDOWN]:
				done = True
			if event.type == 5:
				print(event.pos)
				print(event.button)