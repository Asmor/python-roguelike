import Tiles

class Cell:
	"""A single cell"""
	def __init__(self):
		self.base = "#"
		self.passable = False
		self.tileset = None
		self.floorType = "1"
		self.terrainFeature = None
		self.isRoom = False
		# neighbors will have 8 elements; element 0 is the neighbor above this cell
		# and the rest go clockwise around so that element 7 is the upper left neighbor
		# Each neighbor will either be a Cell object or None
		self.neighbors = [None for i in range(8)]

	def setBase(self, newType):
		self.base = newType
		self.passable = (newType != "#")
		if newType in map(str, range(1, 5)):
			self.floorType = newType
			self.base = "."
			self.isRoom = True

	def setFeature(self, feature):
		self.terrainFeature = feature

	def blit(self, screen, x, y):
		screen.blit(Tiles.tiles[self.tileset][self.fillType], (x*Tiles.TILE_WIDTH, y*Tiles.TILE_HEIGHT))
		if self.terrainFeature != None:
			screen.blit(Tiles.tiles[self.tileset][self.terrainFeature], (x*Tiles.TILE_WIDTH, y*Tiles.TILE_HEIGHT))

	@property
	def fillType(self):
		if self.base == "#":
			up = 0
			down = 0
			left = 0
			right = 0
			if self.neighbors[0] != None and self.neighbors[0].base == "#":
				up = 1
			if self.neighbors[2] != None and self.neighbors[2].base == "#":
				right = 1
			if self.neighbors[4] != None and self.neighbors[4].base == "#":
				down = 1
			if self.neighbors[6] != None and self.neighbors[6].base == "#":
				left = 1
			return Tiles.wallTypes[up][right][down][left]
		else:
			return "floor-" + self.floorType

	@property
	def isWall(self):
		"""A wall has exactly one orthogonally-adjacent passable neighbor"""
		if self.passable:
			return False
		# Only check the even indices--0, 2, 4, 6--which are orthogonally-adjacent neighbors
		passableNeighbors = 0
		for cell in self.neighbors[::2]:
			if cell != None and cell.passable:
				passableNeighbors += 1
		return passableNeighbors == 1

	@property
	def isCorner(self):
		"""A corner is not a wall, but has at least one adjacent passable neighbor"""
		if self.passable or self.isWall:
			return False
		# Only check the odd indices--1, 3, 5, 7--which are diagonally-adjacent neighbors
		for cell in self.neighbors:
			if cell != None and cell.passable:
				return True
		return False

	@property
	def isRoom(self):
		"""A room is passable space placed by a room"""
		return self._isRoom
	@isRoom.setter
	def isRoom(self, value):
		self._isRoom = value

	@property
	def isOpenRoom(self):
		"""A room space is open if it isn't adjacent to any walls"""
		if not self.isRoom:
			return False
		for cell in self.neighbors:
			if not cell.passable:
				return False
		return True
	
	@property
	def isHallway(self):
		"""Hallways are any open terrain that aren't part of a room"""
		return self.passable and not self.isRoom

	@property
	def isEntryway(self):
		"""Entryways are hallways which are adjacent to rooms"""
		if not self.isHallway:
			return False
		for cell in self.neighbors:
			if cell.isRoom:
				return True
		return False

if __name__ == '__main__':
	print map(str, range(1, 5))
	pass