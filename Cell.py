import Tiles

class Cell(object):
	"""A single cell"""
	def __init__(self):
		self.base = "#"
		self.passable = False
		self.tileset = None
		self.floorType = "1"
		self.terrainFeature = None
		self.immutable = False
		# neighbors will have 8 elements; element 0 is the neighbor above this cell
		# and the rest go clockwise around so that element 7 is the upper left neighbor
		# Each neighbor will either be a Cell object or None
		self.neighbors = [None for i in range(8)]

	def setBase(self, newType):
		self.base = newType
		self.passable = (newType not in ("#", "W"))
		if newType in map(str, range(1, 5)):
			self.floorType = newType
			self.base = "."
		if newType == "W":
			self.base = "#"
			self.immutable = True
		if newType == "F":
			self.base = "."
			self.immutable = True

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
		return masks["wall"].check(self)

	@property
	def isDoubleWall(self):
		'''It's desirable not to dig a 2-length hallway to connect rooms two walls apart, hence this definition'''
		return masks["doublewall"].check(self)

	@property
	def isCorner(self):
		return masks["corner"].check(self)

	@property
	def isEarth(self):
		return masks["earth"].check(self)

	@property
	def isRoom(self):
		return masks["room"].check(self)

	@property
	def isOpenRoom(self):
		return masks["openroom"].check(self)

	@property
	def isEntryway(self):
		return masks["entryway"].check(self)

	@property
	def isDoorframe(self):
		return masks["doorframe"].check(self)

	@property
	def digCost(self):
		if self.passable:
			return 1
		if self.isCorner or self.isDoorframe:
			# We never want to break through a corner or doorframe
			return 10000
		if self.isDoubleWall:
			# Want to avoid digging through two-deep walls
			return 1000
		if self.isWall:
			# Make breaking through walls more expensive
			return 10
		if self.isEarth:
			# Once we've broken through a wall, moving through earth is cheap
			# To encourage tunneling
			return 1
		# We shouldn't get down here, but if we do...
		return 10000

class CellMask:
	"""Given a 3x3 mask, creates all rotational and mirrored versions of that mask"""
	def __init__(self, mask):
		self._masks = []
		self.addMask(mask)

	def addMask(self, mask):
		rot0 = mask
		rot90 = zip(*rot0[::-1])
		rot180 = zip(*rot90[::-1])
		rot270 = zip(*rot180[::-1])
		mirrored0 = rot0[::-1]
		mirrored90 = rot90[::-1]
		mirrored180 = rot180[::-1]
		mirrored270 = rot270[::-1]

		if rot0 not in self._masks:
			self._masks.append(rot0)
			if rot90 not in self._masks:
				self._masks.append(rot90)
				if rot180 not in self._masks:
					self._masks.append(rot180)
					# if 90 and 180 are unique, 270 must be unique
					self._masks.append(rot270)

		if mirrored0 not in self._masks:
			self._masks.append(mirrored0)
			if mirrored90 not in self._masks:
				self._masks.append(mirrored90)
				if mirrored180 not in self._masks:
					self._masks.append(mirrored180)
					# if 90 and 180 are unique, 270 must be unique
					self._masks.append(mirrored270)

	def check(self, cell):
		for mask in self._masks:
			if CellMask._checkSingleMask(mask, cell):
				return True
		return False

	@staticmethod
	def _checkSingleMask(mask, cell):
		# Check the cell itself, at the center of its pattern
		if CellMask._checkCellMask(mask[1][1], cell) == False:
			return False

		# Check each of the cell's neighbors
		coordsList = [
			(0, 1, 0), # top
			(1, 2, 0), # top-right
			(2, 2, 1), # right
			(3, 2, 2), # bottom-right
			(4, 1, 2), # bottom
			(5, 0, 2), # bottom-left
			(6, 0, 1), # left
			(7, 0, 0) # top-left
		]

		for coords in coordsList:
			if not CellMask._checkSingleCell(mask, cell, coords):
				return False
		return True

	@staticmethod
	def _checkSingleCell(mask, cell, coords):
		neighbor = cell.neighbors[coords[0]]
		cellMask = mask[coords[1]][coords[2]]
		return CellMask._checkCellMask(cellMask, neighbor)

	@staticmethod
	def _checkCellMask(cellMask, cell):
		if cellMask == "?":
			return True

		if cellMask == "#":
			return cell != None and not cell.passable

		if cellMask == "w":
			return cell != None and cell.isWall

		if cellMask == "p":
			return cell != None and cell.passable
		if cellMask == "P":
			return cell == None or not cell.passable

		if cellMask == "r":
			return cell != None and cell.isRoom
		if cellMask == "e":
			return cell != None and cell.isEntryway

		# Got a mask we don't know how to handle
		return False

'''
Mask definitions:
?: ignore
#: unpassable
w: wall
p: passable
P: not passable
r: room
e: entryway
'''
masks = {}
masks["earth"] = CellMask([
	tuple("PPP"),
	tuple("P#P"),
	tuple("PPP")
])
masks["room"] = CellMask([
	tuple("pp?"),
	tuple("pp?"),
	tuple("???")
])
masks["entryway"] = CellMask([
	tuple("?r?"),
	tuple("PpP"),
	tuple("?p?")
])
masks["doorframe"] = CellMask([
	tuple("?e?"),
	tuple("?#?"),
	tuple("???")
])
masks["corner"] = CellMask([ # Concave corner
	tuple("pP?"),
	tuple("P#?"),
	tuple("???")
])
masks["corner"].addMask([ # Convex corner
	tuple("?pp"),
	tuple("p#?"),
	tuple("p??")
])
masks["wall"] = CellMask([
	tuple("?p?"),
	tuple("?#?"),
	tuple("???")
])
masks["openroom"] = CellMask([
	tuple("ppp"),
	tuple("ppp"),
	tuple("ppp")
])
masks["doublewall"] = CellMask([
	tuple("?p?"),
	tuple("?w?"),
	tuple("?w?")
])


if __name__ == '__main__':
	maskA = [
		tuple("x??"),
		tuple("???"),
		tuple("?x?")
	]
	maskB = [
		tuple("xxx"),
		tuple("xxx"),
		tuple("xxx")
	]

	print maskB == maskB[::-1]
	print maskB == zip(*maskB[::-1])
	print maskB
	print maskB[::-1]
	print zip(*maskB[::-1])

	cm = CellMask(maskA)
	cm.addMask(maskB)
	# cm = CellMask(maskB)

	for mask in cm._masks:
		print ""
		for row in mask:
			print "".join(row)
	pass