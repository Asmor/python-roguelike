import PathFinder
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
		self.features = []
		for y, row in enumerate(self.cells):
			for x, cell in enumerate(row):
				# Neighbors are indexed starting with 0 on top and going clockwise around cell
				cell.tileset = self.style
				above = y-1
				below = y+1
				left = x-1
				right = x+1
				hasAbove = above in range(height)
				hasBelow = below in range(height)
				hasLeft  = left in range(width)
				hasRight = right in range(width)
				if hasAbove:
					if hasLeft:
						cell.neighbors[7] = self.getCell(left, above)
					cell.neighbors[0] = self.getCell(x, above)
					if hasRight:
						cell.neighbors[1] = self.getCell(right, above)
				if hasRight:
					cell.neighbors[2] = self.getCell(right, y)
				if hasBelow:
					if hasRight:
						cell.neighbors[3] = self.getCell(right, below)
					cell.neighbors[4] = self.getCell(x, below)
					if hasLeft:
						cell.neighbors[5] = self.getCell(left, below)
				if hasLeft:
					cell.neighbors[6] = self.getCell(left, y)

	@property
	def style(self):
		return self._style
	@style.setter
	def style(self, value):
		self._style = value
		for y, row in enumerate(self.cells):
			for x, cell in enumerate(row):
				cell.tileset = value

	def getCell(self, x, y):
		"""Lets us get cells in a consistent x, y order instead of having to look them up in the array in the backwards [y][x] order"""
		return self.cells[y][x]
	def setCell(self, x, y, how):
		cell = self.getCell(x, y)
		cell.setBase(how)
		return cell
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
		addFeatureToList = True
		if haveRoom:
			for deltaY, row in enumerate(mask):
				for deltaX, char in enumerate(row):
					cell = self.setCell(x+deltaX, y+deltaY, char)
					if addFeatureToList and cell.passable:
						addFeatureToList = False
						self.features.append((x+deltaX, y+deltaY))
		return haveRoom
	def blit(self, screen):
		for x in range(self.width):
			for y in range(self.height):
				self.getCell(x, y).blit(screen, x, y)
	def getRandomCell(self):
		x = Util.getRandom(0, self.width-1)
		y = Util.getRandom(0, self.height-1)
		return (self.getCell(x, y), x, y)
	def placeTerrainFeature(self, feature):
		i = 0
		while i < 10000:
			cell, x, y = self.getRandomCell()
			if cell.isOpenRoom:
				cell.setFeature(feature)
				return (True, x, y) 
			i += 1
		return (False, -1, -1)
	def dig(self, path):
		for coords in path:
			self.setCell(coords[0], coords[1], ".")
	def connectFeatures(self):
		frange = range(len(self.features))
		for i in frange:
			for j in frange[i+1:]:
				path = PathFinder.FindPath(self, self.features[i], self.features[j])
				self.dig(path)

def MakeRoom(width, height):
	floorStyle = Util.getRandom(2, 4)
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

	import MazeGenerator
	room = MazeGenerator.Maze(7, 7).getMap()
	level.applyFeature(room, 1, 1)

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
			if event.type == MOUSEBUTTONDOWN:
				x = int(event.pos[0]/24)
				y = int(event.pos[1]/24)
				if event.button == 1:
					level.setCell(x, y, "#")
				else:
					level.setCell(x, y, ".")
				draw()