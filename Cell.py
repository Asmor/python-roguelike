import Tiles

class Cell:
	"""A single cell"""
	def __init__(self):
		self.base = "#"
		self.passable = False
		self.tileset = None
		self.floorType = "1"
		self.terrainFeature = None
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

	def setFeature(self, feature):
		self.terrainFeature = feature

	def blit(self, screen, x, y):
		coords = (x*Tiles.TILE_WIDTH, y*Tiles.TILE_HEIGHT)
		screen.blit(Tiles.tiles[self.tileset][self.fillType], coords)
		if self.terrainFeature != None:
			screen.blit(Tiles.tiles[self.tileset][self.terrainFeature], coords)
		if self.isEntryway:
			screen.blit(Tiles.features["door-wooden-closed"], coords)

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
		"""A wall has exactly one orthogonally-adjacent passable neighbor or exactly two on opposite sides"""
		if self.passable or self.isCorner:
			return False
		up    = self.neighbors[0] != None and self.neighbors[0].passable
		right = self.neighbors[2] != None and self.neighbors[2].passable
		down  = self.neighbors[4] != None and self.neighbors[4].passable
		left  = self.neighbors[6] != None and self.neighbors[6].passable

		if up or down:
			if left or right:
				return False
			return True
		if left or right:
			return True

	@property
	def isCorner(self):
		"""A corner is has a diagonally-adjacent passable space sandwiched between two orthogonally-adjacent unpassable spaces"""
		if self.passable:
			return False
		for i in range(4):
			first = i*2
			second = i*2+1
			third = (i*2+2) % 8
			if self.neighbors[first] != None and not self.neighbors[first].passable \
				and self.neighbors[second] != None and self.neighbors[second].passable \
				and self.neighbors[third] != None and not self.neighbors[third].passable:
					return True
		return False

	@property
	def isEarth(self):
		"""Earth is unpassable terrain completely surrounded by unpassable terrain"""
		if self.passable:
			return False
		for cell in self.neighbors:
			if cell != None and cell.passable:
				return False
		return True

	@property
	def isRoom(self):
		"""A room is space is either open room, or is passable space adjacent to an open room space"""
		# Interesting corollary: The first space dug out of a room, that you would intuitively consider a hallway
		# is considered a room space by this method. It also ends up being an entryway. This has a number of
		# cascading benefits, e.g. a 2-square "hallway" won't be filled with doors because neither is adjacent
		# to a hallway!
		if not self.passable:
			return False
		if self.isOpenRoom:
			return True
		for cell in self.neighbors:
			if cell != None and cell.isOpenRoom:
				return True
		return False

	@property
	def isNarrow(self):
		"""A narrow space has two unpassable spaces on opposite sides of it and isn't a room space"""
		if not self.passable or self.isRoom:
			return False
		for i in range(4):
			if self.neighbors[i] != None and not self.neighbors[i].passable \
				and self.neighbors[i+4] != None and not self.neighbors[i+4].passable:
					return True
			return False

	@property
	def isOpenRoom(self):
		"""A room space is open if it isn't adjacent to any walls"""
		if not self.passable:
			return False
		for cell in self.neighbors:
			if cell != None and not cell.passable:
				return False
		return True
	
	# @property
	# def isHallway(self):
	# 	"""Hallways are narrow terrain and not room spaces"""
	# 	if not self.isNarrow:
	# 		return False
	# 	for cell in self.neighbors:
	# 		if cell != None and cell.isRoom:
	# 			return True
	# 	return False

	@property
	def isEntryway(self):
		"""Entryways are narrow spaces adjacent to rooms"""
		if not self.isNarrow:
			return False
		for cell in self.neighbors[::2]:
			if cell != None and cell.isRoom:
				return True
		return False

	@property
	def digCost(self):
		if self.passable:
			return 1
		if self.isWall:
			# Make breaking through walls more expensive
			return 10
		if self.isCorner:
			# We never want to break through a corner!
			return 10000
		if self.isEarth:
			# Once we've broken through a wall, moving through earth is cheap
			# To encourage tunneling
			return 1
		# We shouldn't get down here, but if we do...
		return 10000

if __name__ == '__main__':
	print map(str, range(1, 5))
	pass