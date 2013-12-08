import string
import random
import Util
import NaiveRelativeNeighborhood
import MazeGenerator

class Dungeon:
	def __init__(self, targetRooms):
		self.rooms = []
		self.spread = int(targetRooms/10)
		self._fillRooms(targetRooms)
		self._buildMap()
		self._findPaths()

	def _fillRooms(self, targetRooms):
		self._placeRoom(Room.Entrance())
		while len(self.rooms) < targetRooms-1:
			roomType = random.randint(1, 20)
			# if roomType == 1:
			# 	self._placeRoom(Room.Maze())
			# elif roomType < 12:
			if roomType < 12:
				self._placeRoom(Room.Corridor())
			else:
				self._placeRoom(Room.OpenRoom())
		self._placeRoom(Room.Exit())

	def _placeRoom(self, room):
		placed = False
		while not placed:
			foundOverlap = False
			for otherRoom in self.rooms:
				while room.overlaps(otherRoom):
					# Push the room out until it no longer overlaps this room
					room.distance += 1
					foundOverlap = True
			if not foundOverlap:
				self.rooms.append(room)
				placed = True

	def _buildMap(self):
		self._getMapSize()
		self._setupGrid()
		for room in self.rooms:
			self._overlayRoom(room)

	def _getMapSize(self):
		self.minX = 0;
		self.minY = 0;
		self.maxX = 0;
		self.maxY = 0;

		for room in self.rooms:
			minX = room.x
			minY = room.y
			maxX = room.x + room.width
			maxY = room.y + room.height

			self.minX = min(self.minX, minX)
			self.minY = min(self.minY, minY)
			self.maxX = max(self.maxX, maxX)
			self.maxY = max(self.maxY, maxY)

		self.minX -= 1
		self.minY -= 1
		self.maxX += 1
		self.maxY += 1

		# print "X range: %s - %s. Y range: %s - %s" % (self.minX, self.maxX, self.minY, self.maxY)

	def _setupGrid(self):
		self.mapWidth = self.maxX - self.minX
		self.mapHeight = self.maxY - self.minY
		self.map = [["#" for x in range(self.mapWidth)] for y in range(self.mapHeight)]

	def _overlayRoom(self, room):
		for x in range(room.width):
			mapX = x + room.x - self.minX
			for y in range(room.height):
				mapY = y + room.y - self.minY
				tile = room.layout[y][x]
				self.map[mapY][mapX] = tile
				if tile == "u":
					self.entrance = (mapX, mapY)


	def _findPaths(self):
		points = []
		for room in self.rooms:
			c = room.center
			x = c[0]
			y = c[1]
			p = (x - self.minX, y - self.minY)
			points.append(p)
		self.connectedRooms = NaiveRelativeNeighborhood.getEdges(points)

class Room(object):
	def __init__(self, layout):
		self.layout = layout
		self.height = len(layout)
		self.width = len(layout[0])
		self.angle = Util.getRandomAngle()
		self.distance = 0

	def __repr__(self):
		return "%s: [%sx%s] @ (%s, %s) Distance: %s. Angle: %s." % (self.id, self.width, self.height, self.x, self.y, self.distance, self.angle)

	@property
	def center(self):
		x = self.x + (self.width/2)
		y = self.y + (self.height/2)
		return (x, y)

	@property
	def distance(self):
		return self._distance
	@distance.setter
	def distance(self, value):
		self._distance = value
		coords = Util.getXYByDist(value, self.angle)
		self._x = coords[0]
		self._y = coords[1]

	@property
	def x(self):
		return self._x
	@property
	def y(self):
		return self._y

	@property
	def xRange(self):
		return range(self.x, self.x + self.width)
	@property
	def yRange(self):
		return range(self.y, self.y + self.height)
	@property
	def xRangeWithBuffer(self):
		return range(self.x - 1, self.x + self.width + 1)
	@property
	def yRangeWithBuffer(self):
		return range(self.y - 1, self.y + self.height + 1)

	def overlaps(self, otherRoom):
		xOverlap = 0
		otherXRange = otherRoom.xRange
		for x in self.xRangeWithBuffer:
			if x in otherXRange:
				xOverlap += 1

		if xOverlap == 0:
			return False

		yOverlap = 0
		otherYRange = otherRoom.yRange
		for y in self.yRangeWithBuffer:
			if y in otherYRange:
				yOverlap += 1

		if yOverlap == 0:
			return False

		# We overlap on both the X and Y axes, so we DO overlap with other room
		return True
	@classmethod
	def OpenRoom(cls):
		width = random.randint(3, 6)
		height = random.randint(3, 6)
		layout = [["." for x in range(width)] for y in range(height)]

		return cls(layout)

	@classmethod
	def Corridor(cls):
		width = random.randint(4, 8)
		height = random.randint(4, 8)
		if random.randint(0, 1):
			width = 3
		else:
			height = 3
		layout = [["#" for x in range(width)] for y in range(height)]

		return cls(layout)

	@classmethod
	def Maze(cls):
		width = random.randint(5,10)
		height = random.randint(5,10)
		maze = MazeGenerator.Maze(width, height)
		return cls(maze.getMap())

	@classmethod
	def Entrance(cls):
		rm = Room.OpenRoom()
		x = random.randint(1, rm.width-2)
		y = random.randint(1, rm.height-2)
		rm.layout[y][x] = "u"

		return rm

	@classmethod
	def Exit(cls):
		rm = Room.OpenRoom()
		x = random.randint(1, rm.width-2)
		y = random.randint(1, rm.height-2)
		rm.layout[y][x] = "d"

		return rm

if __name__ == "__main__":
	rm = Room.Exit()
	for row in rm.layout:
		print "".join(row)
	pass