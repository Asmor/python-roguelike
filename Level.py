import NewDungeonGenerator
import PathFinder
import Cell
import Tiles
from Tiles import TILE_WIDTH, TILE_HEIGHT
import Util

class Level(object):
	"""A dungeon level"""
	def __init__(self, numberOfRooms):
		self.dungeon = NewDungeonGenerator.Dungeon(numberOfRooms) 
		self.width = self.dungeon.mapWidth
		self.height = self.dungeon.mapHeight
		self.cells = [[Cell.Cell(self, (x, y)) for x in range(self.width)] for y in range(self.height)]
		self.style = "grey"
		self.features = []
		self._dirtyCells = []
		self._map = None
		for y, row in enumerate(self.cells):
			for x, cell in enumerate(row):
				# Neighbors are indexed starting with 0 on top and going clockwise around cell
				cell.tileset = self.style
				above = y-1
				below = y+1
				left = x-1
				right = x+1
				hasAbove = above in range(self.height)
				hasBelow = below in range(self.height)
				hasLeft  = left in range(self.width)
				hasRight = right in range(self.width)
				if hasAbove:
					if hasLeft:
						cell.neighbors[7] = self.getCell((left, above))
					cell.neighbors[0] = self.getCell((x, above))
					if hasRight:
						cell.neighbors[1] = self.getCell((right, above))
				if hasRight:
					cell.neighbors[2] = self.getCell((right, y))
				if hasBelow:
					if hasRight:
						cell.neighbors[3] = self.getCell((right, below))
					cell.neighbors[4] = self.getCell((x, below))
					if hasLeft:
						cell.neighbors[5] = self.getCell((left, below))
				if hasLeft:
					cell.neighbors[6] = self.getCell((left, y))

		for y in range(len(self.dungeon.map)):
			for x in range(len(self.dungeon.map[0])):
				self.setCell((x, y), self.dungeon.map[y][x], True)

		self.connect()

	@property
	def style(self):
		return self._style
	@style.setter
	def style(self, value):
		self._style = value
		for row in self.cells:
			for cell in row:
				cell.tileset = value

	def setMap(self, scrolling_map):
		self._map = scrolling_map

	def getCell(self, coords):
		"""Lets us get cells in a consistent x, y order instead of having to look them up in the array in the backwards [y][x] order"""
		return self.cells[coords[1]][coords[0]]

	def setCell(self, coords, how, ignoreNeighbors=False):
		cell = self.getCell((coords[0], coords[1]))
		cell.setBase(how)
		self.markDirty(cell, ignoreNeighbors)
		return cell

	def markDirty(self, cell, noNeighbors=False):
		# When drawing the entire map, trying to mark neighbors is both redundant
		# and very, very slow
		if noNeighbors:
			self._dirtyCells.append(cell)
			return
		# When a cell is marked dirty, we also mark its neighbors dirty
		# As a cell with walls draws its walls based on neighbors
		# Need to grab extended neighbors as well, for doors
		cells = cell.extendedNeighbors
		for c in cells:
			if c and c not in self._dirtyCells:
				self._dirtyCells.append(c)

	def _checkOverlap(self, mask, x, y):
		if y + len(mask) > self.height:
			return False
		if x + len(mask[0]) > self.width:
			return False
		for deltaY, row in enumerate(mask):
			for deltaX, char in enumerate(row):
				if char == " ":
					continue
				if self.getCell((x+deltaX, y+deltaY)).base != "#":
					return False
		return True
	def applyFeature(self, mask, x, y):
		"""Mask should have a space for any spot it doesn't want to affect"""
		haveRoom = self._checkOverlap(mask, x, y)
		addFeatureToList = True
		if haveRoom:
			for deltaY, row in enumerate(mask):
				for deltaX, char in enumerate(row):
					cell = self.setCell((x+deltaX, y+deltaY), char)
					if addFeatureToList and cell.passable:
						addFeatureToList = False
						self.features.append((x+deltaX, y+deltaY))
		return haveRoom

	def getCellBlits(self):
		if not self._map:
			return

		cellBlits = []

		for cell in self._dirtyCells:
			cellBlits.append(cell.getBlits())

		self._dirtyCells = []

		return cellBlits

	def getRandomCell(self):
		x = Util.getRandom(0, self.width-1)
		y = Util.getRandom(0, self.height-1)
		return (self.getCell((x, y)), x, y)
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
			self.setCell((coords[0], coords[1]), ".", True)

	def connect(self):
		for path in self.dungeon.connectedRooms:
			plan = PathFinder.FindPath(self, path[0], path[1])
			if plan:
				self.dig(plan)

	@property
	def entranceCoords(self):
		return self.dungeon.entrance

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
	screen = pygame.display.set_mode((FIELD_WIDTH * TILE_WIDTH, FIELD_HEIGHT * TILE_HEIGHT))
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