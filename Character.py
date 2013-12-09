import Tiles
import Util

class Character(object):
	def __init__(self, name, image, level):
		self.name = name
		# Image is currently a tuple with multiple frames.
		# Only using first image for now, to keep it simple.
		self.image = image[0]
		self.level = level
		self.visibleSpaces = []
		self.sightRange = 5

	def move(self, direction):
		if self.cell.moveCharacter(direction):
			self.clearVisibility()
			self.checkVisibility()

	def clearVisibility(self):
		for cell in self.visibleSpaces:
			cell.visible = False
		self.visibleSpaces = []

	def checkVisibility(self):
		xMin = self.position[0] - self.sightRange
		xMax = self.position[0] + self.sightRange + 1
		yMin = self.position[1] - self.sightRange
		yMax = self.position[1] + self.sightRange + 1
		for x in range(xMin, xMax):
			for y in range(yMin, yMax):
				cell = self.level.getCell((x, y))
				if cell:
					cell.visible = self.sees(cell)

	def sees(self, cell):
		line = Util.getLine(self.position, cell.coords)
		blocked = False
		first = True
		for point in line:
			if first:
				# Don't evaluate the point we're standing on
				first = False
				continue
			if blocked:
				# Only fails if the blocking piece ISN'T the last piece
				return False
			if self.level.getCell(point).blocksSight:
				blocked = True
		self.visibleSpaces.append(cell)
		return True

	@property
	def cell(self):
		return self._cell
	@cell.setter
	def cell(self, value):
		self._cell = value
	
	@property
	def position(self):
		return self.cell.coords

class NPC(Character):
	def __init__(self, name, image, level):
		super(NPC, self).__init__(name, image, level)
		self.state = "sleeping"

	@classmethod
	def Dragon_Red(cls, level):
		return cls("Red Dragon", Tiles.mobs["red-dragon"], level)

if __name__ == '__main__':
	foo = Character("Name", "not really an image", "not really a level")
	bar = NPC("Name", "not really an image", "not really a level")
	dragon = NPC.Dragon_Red("not really a level")
	print dragon.state
	pass