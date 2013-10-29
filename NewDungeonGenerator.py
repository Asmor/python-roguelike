import random

class Dungeon:
	def __init__(self, targetRooms):
		self.rooms = []
		self.spread = int(targetRooms/10)
		self._fillRooms(targetRooms)
		spreads = 0
		while spreads < 10:
			if self._spreadRooms() < 10:
				break
			spreads += 1

	def _fillRooms(self, targetRooms):
		for i in range(targetRooms):
			x = random.randint(-self.spread, self.spread)
			y = random.randint(-self.spread, self.spread)
			width = random.randint(1, 5) + random.randint(1, 5)
			height = random.randint(1, 5) + random.randint(1, 5)
			self.rooms.append(RoomPlaceholder(width, height, x, y))

	def _spreadRooms(self):
		size = range(len(self.rooms))
		overlaps = 0
		comparisons = 0
		biggestChange = 0
		for i in size:
			for j in size[i:]:
				comparisons += 1
				vector = self.rooms[i].getOverlapVector(self.rooms[j]);
				if vector != (0, 0):
					overlaps += 1
					self.rooms[i].move(vector)
					magnitude = abs(vector[0]) + abs(vector[1])
					if magnitude > biggestChange:
						print self.rooms[i]
						print self.rooms[j]
						print vector
						biggestChange = magnitude
		print "Comparisons: %s. Overlaps: %s. Biggest change: %s." % (comparisons, overlaps, biggestChange)
		return overlaps


class RoomPlaceholder:
	def __init__(self, width, height, x, y):
		self.width = width
		self.height = height
		self.x = x
		self.y = y

	@property
	def xRange(self):
		return range(self.x, self.x + self.width)
	@property
	def yRange(self):
		return range(self.y, self.y + self.height)

	def getOverlapVector(self, otherRoom):
		xOverlap = 0
		otherXRange = otherRoom.xRange
		for x in self.xRange:
			if x in otherXRange:
				xOverlap += 1

		if xOverlap == 0:
			return (0, 0)

		yOverlap = 0
		otherYRange = otherRoom.yRange
		for y in self.yRange:
			if y in otherYRange:
				yOverlap += 1

		if yOverlap == 0:
			return (0, 0)

		if self.x < otherRoom.x:
			xOverlap *= -1
		if self.y < otherRoom.y:
			yOverlap *= -1

		return (xOverlap, yOverlap)

	def move(self, vector):
		self.x += vector[0]
		self.y += vector[1]

	def __repr__(self):
		return "[%sx%s] @ (%s, %s)" % (self.width, self.height, self.x, self.y)


if __name__ == "__main__":
	dungeon = Dungeon(150)
	# for room in Dungeon.rooms:
	# 	print room
	pass