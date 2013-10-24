import Tiles
import Level
import Util
import PathFinder
import os
import pygame
import pygame.event
import pygame.locals
from pygame.locals import *

LEVEL_WIDTH		= 40
LEVEL_HEIGHT	= 20

def randomizeLevel(level):
	for y in range(level.height):
		for x in range(level.width):
			if Util.getRandom(0, 1) == 0:
				level.setCell(x, y, ".")
			else:
				level.setCell(x, y, "#")

def insertRandomRoom(level):
	x = Util.getRandom(0, LEVEL_WIDTH-1)
	y = Util.getRandom(0, LEVEL_HEIGHT-1)
	width = Util.getRandom(3, 6)
	height = Util.getRandom(3, 6)
	room = Level.MakeRoom(width, height)
	level.applyFeature(room, x, y)

if __name__=='__main__':
	pygame.init()
	screen = pygame.display.set_mode((LEVEL_WIDTH * Tiles.TILE_WIDTH, LEVEL_HEIGHT * Tiles.TILE_HEIGHT))
	level = Level.Level(LEVEL_WIDTH, LEVEL_HEIGHT)
	# level.style = Tiles.tileStyles[Util.getRandom(1, 15)]
	level.style = Tiles.tileStyles[2]
	# randomizeLevel(level)
	for i in range(100):
		insertRandomRoom(level)

	stairsUp, upX, upY = level.placeTerrainFeature(".", "stairs-up")
	stairsDown, downX, downY = level.placeTerrainFeature(".", "stairs-down")

	# path = PathFinder.FindPath(level, (upX, upY), (downX, downY))

	# level.dig(path)

	level.connectFeatures()

	def draw():
		screen.fill((255, 255, 255))
		level.blit(screen)
		pygame.display.flip()
	draw()
	done = False
	while not done:
		for event in pygame.event.get():
			if event.type in [KEYDOWN, QUIT, JOYBUTTONDOWN]:
				done = True
			if event.type == 5:
				x = int(event.pos[0]/24)
				y = int(event.pos[1]/24)
				if event.button == 1:
					level.setCell(x, y, "#")
				else:
					level.setCell(x, y, ".")
				draw()