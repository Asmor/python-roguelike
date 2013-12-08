class Character(object):
	def __init__(self, name, image, coords):
		self.name = name
		# Image is currently a tuple with multiple frames.
		# Only using first image for now, to keep it simple.
		self.image = image[0]
		self.position = coords

	def move(self, direction):
		self.cell.moveCharacter(direction)

	@property
	def cell(self):
		return self._cell
	@cell.setter
	def cell(self, value):
		self._cell = value
		self.position = value.coords
	