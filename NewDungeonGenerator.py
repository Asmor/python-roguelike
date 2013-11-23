import string
import random
import Util

class Dungeon:
	def __init__(self, targetRooms):
		self.rooms = []
		self.spread = int(targetRooms/10)
		self._fillRooms(targetRooms)
		self._buildMap()

	def _fillRooms(self, targetRooms):
		for i in range(targetRooms):
			width = random.randint(2, 5) + random.randint(2, 5)
			height = random.randint(2, 5) + random.randint(2, 5)
			self._placeRoom(RoomPlaceholder(width, height))

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

		# print "X range: %s - %s. Y range: %s - %s" % (self.minX, self.maxX, self.minY, self.maxY)

	def _setupGrid(self):
		self.mapWidth = self.maxX - self.minX
		self.mapHeight = self.maxY - self.minY
		self.map = [["#" for x in range(self.mapWidth)] for y in range(self.mapHeight)]

	def _overlayRoom(self, room):
		if not room.valid:
			return
		startX = room.x - self.minX
		endX = startX + room.width
		startY = room.y - self.minY
		endY = startY + room.height

		for x in range(startX, endX):
			for y in range(startY, endY):
				if x == startX or y == startY or x+1 == endX or y+1 == endY:
					# self.map[y][x] = "w"
					self.map[y][x] = "#"
				else:
					self.map[y][x] = "."

class RoomPlaceholder(object):
	def __init__(self, width, height):
		self.width = width
		self.height = height
		self.id = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(8))
		self.angle = Util.getRandomAngle()
		self.distance = 0

	@property
	def valid(self):
		# Includes walls, so <= 5 means all rooms are 4x4 or larger
		if self.width <= 5 or self.height <= 5:
			return False
		return True

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

	def overlaps(self, otherRoom):
		xOverlap = 0
		otherXRange = otherRoom.xRange
		for x in self.xRange:
			if x in otherXRange:
				xOverlap += 1

		if xOverlap == 0:
			return False

		yOverlap = 0
		otherYRange = otherRoom.yRange
		for y in self.yRange:
			if y in otherYRange:
				yOverlap += 1

		if yOverlap == 0:
			return False

		# We overlap on both the X and Y axes, so we DO overlap with other room
		return True

	def __repr__(self):
		return "%s: [%sx%s] @ (%s, %s) Distance: %s. Angle: %s." % (self.id, self.width, self.height, self.x, self.y, self.distance, self.angle)

if __name__ == "__main__":
	dungeon = Dungeon(150)
	for row in dungeon.map:
		print "".join(row)
	print "Map size: %sx%s" % (len(dungeon.map[0]), len(dungeon.map))
	distances = []
	for room in dungeon.rooms:
		distances.append(room.distance)

	def mean(numbers):
		return sum(numbers) / len(numbers)
	def median(numbers):
		numbers.sort()
		n = len(numbers) 
		if n & 1:
			return numbers[n // 2]
		else:
			return (numbers[n//2-1] + numbers[n//2]) / 2
	print max(*distances)
	print min(*distances)
	print mean(distances)
	print median(distances)

	# room = RoomPlaceholder(5,5)
	# print "%s\n" % room.distance
	# room.distance = 10
	# print "%s\n" % room.distance
	# print room
	pass