import pygame
import pygame.event
import pygame.locals
from pygame.locals import *

TERRAIN_LAYER   = 0
FEATURE_LAYER   = 1
CHARACTER_LAYER = 2
MISC_LAYER      = 3

black = (0, 0, 0)

zoomLevels = [ .1, .2, .3, .4, .5, .6, .8, 1, 1.2, 1.4, 1.7, 2, 2.4, 3, 4 ]

class Scrolling_Map(object):
	def __init__(self, screen, tileWidth, tileHeight):
		self.screen = screen
		self.xOff = 0
		self.yOff = 0
		self.level = None
		self._zoomLevel = 7 # index for a scale of '1'
		self._tileWidth = tileWidth
		self._tileHeight = tileHeight
		self._dirty = True
		self._scaleDirty = True

	@property
	def level(self):
		return self._level
	@level.setter
	def level(self, level):
		if not level:
			self._level = None
			return

		self._level = level
		self._level.setMap(self)
		
		width = self._level.dungeon.mapWidth * self._tileWidth
		height = self._level.dungeon.mapHeight * self._tileHeight
		
		self.terrainLayer = pygame.Surface((width, height))
		# Note not setting color key for terrain layer, as it doesn't want transparency
		self.featureLayer = pygame.Surface((width, height))
		self.featureLayer.set_colorkey(black)
		self.characterLayer = pygame.Surface((width, height))
		self.characterLayer.set_colorkey(black)
		self.miscLayer = pygame.Surface((width, height))
		self.miscLayer.set_colorkey(black)

		self.layers = [
			self.terrainLayer,
			self.featureLayer,
			self.characterLayer,
			self.miscLayer
		]

		self._dirty = True

	def scroll(self, relative):
		self.xOff += relative[0]
		self.yOff += relative[1]
		self.blit()

	def scale(self, bigger, centerPosition):
		oldScale = self._scale
		oldSize = self._scaledImageSize

		if bigger:
			if self._zoomLevel + 1 < len(zoomLevels):
				self._zoomLevel += 1
			else:
				return
		else:
			if self._zoomLevel > 0:
				self._zoomLevel -= 1
			else:
				return

		newScale = zoomLevels[self._zoomLevel]

		centerXDelta = centerPosition[0] - self.xOff
		centerYDelta = centerPosition[1] - self.yOff
		centerXDeltaPerc = centerXDelta / float(oldSize[0])
		centerYDeltaPerc = centerYDelta / float(oldSize[1])
		newSize = self._scaledImageSize
		newXDelta = int(centerXDeltaPerc * newSize[0])
		newYDelta = int(centerYDeltaPerc * newSize[1])
		self.xOff += centerXDelta - newXDelta
		self.yOff += centerYDelta - newYDelta
		self._scaleDirty = True
		self.blit()

	def blit(self):
		self._blitTiles()
		self.screen.fill(black)
		self.screen.blit(self.scaledImage, self._imageOffset)
		pygame.display.flip()

	def _blitTiles(self):
		cellBlits = self._level.getCellBlits()
		for cellBlit in cellBlits:
			self.clearTile(cellBlit["coords"])
			for blit in cellBlit["blits"]:
				self._blitTile(blit["tile"], cellBlit["coords"], blit["layer"])

	def _blitTile(self, tile, coords, layer):
		self._dirty = True
		target = self.layers[layer]
		width = tile.get_width()
		height = tile.get_height()
		pixCoords = self.tileToPixelTopLeft(coords)
		rect = (pixCoords[0], pixCoords[1], width, height)
		target.fill(black, rect)
		target.blit(tile, pixCoords)

	def clearTile(self, coords):
		pixCoords = self.tileToPixelTopLeft(coords)
		rect = (pixCoords[0], pixCoords[1], self._tileWidth, self._tileHeight)
		for layer in self.layers:
			if layer != self.miscLayer:
				layer.fill(black, rect)

	def getClickedCoords(self, pos):
		imageX = pos[0] - self.xOff
		imageY = pos[1] - self.yOff

		xCoord = float(imageX) / (self._tileWidth * self._scale)
		yCoord = float(imageY) / (self._tileHeight * self._scale)

		return (int(xCoord), int(yCoord))

	def centerOn(self, coords):
		xDelta = (coords[0] * self._tileWidth + self._tileWidth / 2) * self._scale
		yDelta = (coords[1] * self._tileHeight + self._tileHeight / 2) * self._scale
		screenWidth = self.screen.get_width()
		screenHeight = self.screen.get_height()

		self.xOff = (screenWidth / 2) - xDelta
		self.yOff = (screenHeight / 2) - yDelta

	def tileToPixelTopLeft(self, coords):
		pixelX = coords[0] * self._tileWidth
		pixelY = coords[1] * self._tileHeight
		return (pixelX, pixelY)

	def tileToPixelCenter(self, coords):
		pixelX = coords[0] * self._tileWidth + self._tileWidth/2
		pixelY = coords[1] * self._tileHeight + self._tileHeight/2
		return (pixelX, pixelY)

	def drawLine(self, color, start, end):
		# Takes tile coordinates and draws a line from center of one to center of other
		startPixel = self.tileToPixelCenter(start)
		endPixel = self.tileToPixelCenter(end)

		pygame.draw.line(self.miscLayer, color, startPixel, endPixel, 10)

		self._dirty = True

	def setCell(self, coords, how):
		self.level.setCell(coords, how)
		self.blit()

	@property
	def scaledImage(self):
		if self._dirty or self._scaleDirty or not self._scaledImage:
			self._scaledImage = pygame.transform.scale(self.flatImage, self._scaledImageSize)
			self._scaleDirty = False
		return self._scaledImage

	@property
	def flatImage(self):
		if self._dirty or not self._flatImage:
			w = self.terrainLayer.get_width()
			h = self.terrainLayer.get_height()
			flat = pygame.Surface((w, h))
			for layer in self.layers:
				flat.blit(layer, (0, 0))
			self._flatImage = flat
			self._dirty = False
		return self._flatImage

	@property
	def _imageOffset(self):
		return (self.xOff, self.yOff)

	@property
	def _scaledImageSize(self):
		width = int(self.terrainLayer.get_width() * self._scale)
		height = int(self.terrainLayer.get_height() * self._scale)

		return (width, height)

	@property
	def _scale(self):
		return zoomLevels[self._zoomLevel]

	@property
	def entranceCoords(self):
		return self._level.entranceCoords

	def placeCharacter(self, character, coords):
		cell = self._level.getCell(coords)
		cell.placeCharacter(character)
		character.checkVisibility()

if __name__ == '__main__':
	pygame.init()
	screen = pygame.display.set_mode((1000, 1000))
	filename = "images/oryx_16bit_fantasy_world_trans.png"
	image = pygame.image.load(filename).convert()

	s_map = Scrolling_Map(screen, image, 24, 24)

	done = False

	currentlyDragging = False

	while not done:
		for event in pygame.event.get():
			if event.type in [KEYDOWN, QUIT, JOYBUTTONDOWN]:
				done = True
			elif event.type == MOUSEBUTTONDOWN and event.button == 1:
				currentlyDragging = True
			elif event.type == MOUSEBUTTONUP and event.button == 1:
				currentlyDragging = None
			elif currentlyDragging and event.type == MOUSEMOTION:
				s_map.scroll(event.rel)
			elif event.type == MOUSEBUTTONDOWN and event.button == 4:
				s_map.scale(.1, event.pos)
			elif event.type == MOUSEBUTTONDOWN and event.button == 5:
				s_map.scale(-.1, event.pos)
