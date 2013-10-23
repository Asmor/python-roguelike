import Tiles

class Cell:
	"""A single cell"""
	def __init__(self):
		self.base = "#"
		self.passable = False
		self.fillType = "floor-1"
		self.floorType = "1"
		self.terrainFeature = None

	def setBase(self, newType):
		self.base = newType
		self.passable = (newType == "#")
		if newType in map(str, range(1, 5)):
			self.floorType = newType
			self.base = "."

	def setFeature(self, feature):
		self.terrainFeature = feature

	def blit(self, screen, levelStyle, x, y):
		screen.blit(Tiles.tiles[levelStyle][self.fillType], (x*Tiles.TILE_WIDTH, y*Tiles.TILE_HEIGHT))
		if self.terrainFeature != None:
			screen.blit(Tiles.tiles[levelStyle][self.terrainFeature], (x*Tiles.TILE_WIDTH, y*Tiles.TILE_HEIGHT))


if __name__ == '__main__':
	print map(str, range(1, 5))
	pass