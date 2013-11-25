import pygame
import pygame.event
import pygame.locals
from pygame.locals import *

class Scrolling_Map(object):
	def __init__(self, screen, image, tileWidth, tileHeight):
		self.screen = screen
		self.xOff = 0
		self.yOff = 0
		self._scale = 1
		self._maxScale = 1
		self._minScale = .1
		self._tileWidth = tileWidth
		self._tileHeight = tileHeight

		black = (0, 0, 0)
		self.terrainLayer = image
		self.miscLayer = pygame.Surface((image.get_width(), image.get_height()))
		self.miscLayer.set_colorkey(black)

		self.layers = [
			self.terrainLayer,
			self.miscLayer
		]

		self.blit()

	def scroll(self, relative):
		self.xOff += relative[0]
		self.yOff += relative[1]
		self.blit()

	def scale(self, amt, centerPosition):
		newScale = self._scale + amt
		if newScale >= self._minScale and newScale <= self._maxScale:
			oldSize = self._scaledImageSize
			centerXDelta = centerPosition[0] - self.xOff
			centerYDelta = centerPosition[1] - self.yOff
			centerXDeltaPerc = centerXDelta / float(oldSize[0])
			centerYDeltaPerc = centerYDelta / float(oldSize[1])
			self._scale = newScale
			newSize = self._scaledImageSize
			newXDelta = int(centerXDeltaPerc * newSize[0])
			newYDelta = int(centerYDeltaPerc * newSize[1])
			self.xOff += centerXDelta - newXDelta
			self.yOff += centerYDelta - newYDelta
			self.blit()

	def blit(self):
		self.screen.fill(0)
		self.screen.blit(self._scaledImage, self._imageOffset)
		pygame.display.flip()

	def getClickedCoords(self, pos):
		imageX = pos[0] - self.xOff
		imageY = pos[1] - self.yOff

		xCoord = float(imageX) / (self._tileWidth * self._scale)
		yCoord = float(imageY) / (self._tileHeight * self._scale)

		return (int(xCoord), int(yCoord))

	def tileToPixelCenter(self, coords):
		pixelX = coords[0] * self._tileWidth + self._tileWidth/2
		pixelY = coords[1] * self._tileHeight + self._tileHeight/2
		return (pixelX, pixelY)

	def drawLine(self, color, start, end):
		# Takes tile coordinates and draws a line from center of one to center of other
		startPixel = self.tileToPixelCenter(start)
		endPixel = self.tileToPixelCenter(end)

		pygame.draw.line(self.miscLayer, color, startPixel, endPixel, 10)

	@property
	def _scaledImage(self):
		return pygame.transform.scale(self._flatImage, self._scaledImageSize)

	@property
	def _flatImage(self):
		w = self.terrainLayer.get_width()
		h = self.terrainLayer.get_height()
		flat = pygame.Surface((w, h))
		for layer in self.layers:
			flat.blit(layer, (0, 0))
		return flat

	@property
	def _imageOffset(self):
		return (self.xOff, self.yOff)

	@property
	def _scaledImageSize(self):
		width = int(self.terrainLayer.get_width() * self._scale)
		height = int(self.terrainLayer.get_height() * self._scale)

		return (width, height)
	

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
