import random

class MazeCell:
	def __init__(self, x, y):
		self.id = (x,y)
		self.group = [self.id]
		self.connections = [False for i in range(4)]
	def connect(self, other, direction):
		# print ""
		# print "I am %s, he is %s" % (self.id, other.id)
		if other.id in self.group:
			# print "already in group"
			return False
		self.connections[direction] = True
		other.connections[(direction + 2) % 4] = True
		# print "%s + %s = %s" % (self.group, other.group, self.group + other.group)
		self.group = self.group + other.group
		return True
class Maze:
	def __init__(self, x, y):
		self.width = x
		self.height = y
		self.limit = x*y
		self.cells = [[MazeCell(i, j) for j in range(x)] for i in range(y)]
		self.cellList = []
		for i in range(x):
			for j in range(y):
				self.cellList.append((i, j))
		self.build()

	def getMap(self):
		textMap = [["#" for j in range(self.width*2+1)] for i in range(self.height*2+1)]
		for y in range(self.height):
			for x in range(self.width):
				mapX = x*2+1
				mapY = y*2+1
				textMap[mapY][mapX] = "F"
				textMap[mapY+1][mapX+1] = "W"
				if self.cells[y][x].connections[1]:
					textMap[mapY][mapX+1] = "F"
				else:
					textMap[mapY][mapX+1] = "W"
				if self.cells[y][x].connections[2]:
					textMap[mapY+1][mapX] = "F"
				else:
					textMap[mapY+1][mapX] = "W"
			textMap[y*2+1][self.width*2] = "#"
			textMap[y*2+2][self.width*2] = "#"
		textMap[self.width*2] = ["#" for i in range(self.height*2+1)]
		return textMap

	def build(self):
		done = False
		i = 0
		newList = self.cellList[:]
		while not done and i < 100:
			i += 1
			oldList = newList
			newList = []
			random.shuffle(oldList)
			while len(oldList):
				coords = oldList[0]
				oldList = oldList[1:]
				x = coords[0]
				y = coords[1]
				cell = self.cells[y][x]
				neighbors = range(4)
				random.shuffle(neighbors)
				neighbor = None
				for direction in neighbors:
					if (cell.connections[direction]):
						continue
					if direction == 0 and y > 0:
						neighbor = self.cells[y-1][x]
						break
					elif direction == 1 and x < (self.width-1):
						neighbor = self.cells[y][x+1]
						break
					elif direction == 2 and y < (self.height-1):
						neighbor = self.cells[y+1][x]
						break
					elif direction == 3 and x > 0:
						neighbor = self.cells[y][x-1]
						break

				if neighbor != None:
					cell.connect(neighbor, direction)
					for updateCoords in cell.group:
						self.cells[updateCoords[0]][updateCoords[1]].group = cell.group
						# print "Updating %s to %s" % (updateCoords, self.cells[updateCoords[1]][updateCoords[0]].group)
					newList.append(coords)
			if not len(newList):
				break


if __name__ == '__main__':
	rows = 10
	cols = 10
	m = Maze(cols, rows)
	maze = m.getMap()
	for row in maze:
		print "".join(row)
	pass