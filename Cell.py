import Tiles
from ScrollingMap import TERRAIN_LAYER, FEATURE_LAYER, CHARACTER_LAYER

class Cell(object):
	"""A single cell"""
	def __init__(self, level, coords):
		self.base = "#"
		self.passable = False
		self.tileset = None
		self.floorType = "1"
		self.terrainFeature = None
		self.immutable = False
		self.coords = coords
		self.level = level
		self._visible = False
		self._seen = False
		# neighbors will have 8 elements; element 0 is the neighbor above this cell
		# and the rest go clockwise around so that element 7 is the upper left neighbor
		# Each neighbor will either be a Cell object or None
		self.neighbors = [None for i in range(8)]
		self.character = None

	def setBase(self, newType):
		if self.immutable:
			return
		self.base = newType
		self.passable = (newType not in ("#", "W"))
		if newType in map(str, range(1, 5)):
			self.floorType = newType
			self.base = "."
		if newType in "WFdu":
			self.immutable = True
			self.base = "."
			if newType == "W":
				self.base = "#"
			elif newType == "d":
				self.setFeature("stairs-down-red-carpet")
			elif newType == "u":
				self.setFeature("stairs-up-red-carpet")

	def setFeature(self, feature):
		self.terrainFeature = feature

	def placeCharacter(self, character):
		if self.character:
			return False

		self.character = character
		self.character.cell = self
		self.level.markDirty(self, True)

	def moveCharacter(self, direction):
		target = self.neighbors[direction]

		if target.character or not target.passable:
			return False

		target.placeCharacter(self.character)
		self.character = None
		self.level.markDirty(self, True)

		return True

	def getBlits(self):
		if self.isEarth or not self.seen:
			return {
				"coords": self.coords,
				"blits": []
			}
		blits = []

		if self.visible:
			blits.append({
				"tile": Tiles.tiles[self.tileset][self.fillType],
				"layer": TERRAIN_LAYER
			})

			if self.terrainFeature != None:
				blits.append({
					"tile": Tiles.features[self.terrainFeature],
					"layer": FEATURE_LAYER
				})

			if self.character != None:
				blits.append({
					"tile": self.character.image,
					"layer": CHARACTER_LAYER
				})
		else:
			terrainTile = Tiles.darken(Tiles.tiles[self.tileset][self.fillType])

			blits.append({
				"tile": terrainTile,
				"layer": TERRAIN_LAYER
			})

			if self.terrainFeature != None:
				featureTile = Tiles.darken(Tiles.features[self.terrainFeature])
				blits.append({
					"tile": featureTile,
					"layer": FEATURE_LAYER
				})

		return {
			"coords": self.coords,
			"blits": blits
		}

	@property
	def terrainFeature(self):
		if self.isEntryway:
			return "door-wooden-closed"
		return self._terrainFeature
	@terrainFeature.setter
	def terrainFeature(self, value):
		self._terrainFeature = value
	

	@property
	def fillType(self):
		if self.base == "#":
			up = 0
			down = 0
			left = 0
			right = 0
			if self.neighbors[0] != None and (self.neighbors[0].isWall or self.neighbors[0].isCorner):
				up = 1
			if self.neighbors[2] != None and (self.neighbors[2].isWall or self.neighbors[2].isCorner):
				right = 1
			if self.neighbors[4] != None and (self.neighbors[4].isWall or self.neighbors[4].isCorner):
				down = 1
			if self.neighbors[6] != None and (self.neighbors[6].isWall or self.neighbors[6].isCorner):
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
	def blocksSight(self):
		return self.isEntryway or not self.passable

	@property
	def seen(self):
		return self._seen

	@property
	def visible(self):
		return self._visible
	@visible.setter
	def visible(self, value):
		if value != self._visible:
			self._visible = value
			self.level.markDirty(self, True)
			if value:
				self._seen = True

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

	@property
	def extendedNeighbors(self):
		# Gets all neighbors within 2 squares, including self
		cells = [self]
		for neighbor in self.neighbors:
			if not neighbor:
				continue
			cells.append(neighbor)
			for extNeighbor in neighbor.neighbors:
				if extNeighbor and extNeighbor not in cells:
					cells.append(extNeighbor)
		return cells

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