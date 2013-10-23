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
			if self.getCell(x, y).base == "#":
				up = 0
				down = 0
				left = 0
				right = 0
				if y-1 >= 0 and self.getCell(x, y-1).base == "#":
					up = 1
				if y+1 < self.height and self.getCell(x, y+1).base == "#":
					down = 1
				if x-1 >= 0 and self.getCell(x-1, y).base == "#":
					left = 1
				if x+1 < self.width and self.getCell(x+1, y).base == "#":
					right = 1
				self.getCell(x, y).fillType = Tiles.wallTypes[up][right][down][left]
			else:
				self.getCell(x, y).fillType = "floor-" + self.getCell(x, y).floorType
	def getCell(self, x, y):
		"""Lets us get cells in a consistent x, y order instead of having to look them up in the array in the backwards [y][x] order"""
		return self.cells[y][x]
	def setCell(self, x, y, how):
		self.getCell(x, y).setBase(how)
		self._setCellStyle(x, y)
		if y-1 >= 0:
			self._setCellStyle(x, y-1)
		if y+1 < self.height:
			self._setCellStyle(x, y+1)
		if x-1 >= 0:
			self._setCellStyle(x-1, y)
		if x+1 < self.width:
			self._setCellStyle(x+1, y)
	def _checkOverlap(self, mask, x, y):
		if y + len(mask) > self.height:
			return False
		if x + len(mask[0]) > self.width:
			return False
		for deltaY, row in enumerate(mask):
			for deltaX, char in enumerate(row):
				if char == " ":
					continue
				if self.getCell(x+deltaX, y+deltaY).base != "#":
					return False
		return True
	def applyFeature(self, mask, x, y):
		"""Mask should have a space for any spot it doesn't want to affect"""
		haveRoom = self._checkOverlap(mask, x, y)
		if haveRoom:
			for deltaY, row in enumerate(mask):
				for deltaX, char in enumerate(row):
					self.setCell(x+deltaX, y+deltaY, char)
		return haveRoom
	def blit(self, screen):
		for x in range(self.width):
			for y in range(self.height):
				self.getCell(x, y).blit(screen, self.style, x, y)
	def getRandomCell(self):
		x = Util.getRandom(0, self.width-1)
		y = Util.getRandom(0, self.height-1)
		return (self.getCell(x, y), x, y)
	def placeTerrainFeature(self, mask, feature):
		i = 0
		while i < 10000:
			cell, x, y = self.getRandomCell()
			if cell.base == mask:
				cell.setFeature(feature)
				return (True, x, y) 
			i += 1
		return (False, -1, -1)

def MakeRoom(width, height):
	floorStyle = Util.getRandom(1, 4)
	room = [[str(floorStyle) for i in range(width+2)] for i in range(height+2)]
	right = width+1
	bottom = height+1
	for x in range(0, right+1):
		room[0][x] = "#"
		room[bottom][x] = "#"
	for y in range(0, bottom+1):
		room[y][0] = "#"
		room[y][right] = "#"
	return room

# Test the Level class
if __name__=='__main__' and True:
	import pygame
	from pygame.locals import *
	pygame.init()
	FIELD_WIDTH = 30
	FIELD_HEIGHT = 20
	screen = pygame.display.set_mode((FIELD_WIDTH * Tiles.TILE_WIDTH, FIELD_HEIGHT * Tiles.TILE_HEIGHT))
	level = Level(FIELD_WIDTH, FIELD_HEIGHT)
	level.style = Tiles.tileStyles[Util.getRandom(1, 15)]

	room = MakeRoom(9, 6)
	shouldBeFalse = level.applyFeature(room, FIELD_WIDTH - 8, FIELD_WIDTH - 5)
	shouldBeTrue = level.applyFeature(room, FIELD_WIDTH - 10, FIELD_WIDTH - 7)
	shouldBeTrue = level.applyFeature(room, 1, 1)
	print "This should be false: %s" % shouldBeFalse
	print "This should be true: %s" % shouldBeTrue

	def draw():
		screen.fill((255, 255, 255))
		level.blit(screen)
		pygame.display.flip()
	draw()
	done = False
	while not done:
		for event in pygame.event.get():
			if event.type in [KEYDOWN, QUIT, JOYBUTTONDOWN]:
				done = True
			if event.type == 5:
				x = int(event.pos[0]/24)
				y = int(event.pos[1]/24)
				if event.button == 1:
					level.setCell(x, y, "#")
				else:
					level.setCell(x, y, ".")
				draw()