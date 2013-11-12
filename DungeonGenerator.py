import MazeGenerator
import Tiles
import Level
import Util
import PathFinder
import ScrollingMap
import os
import pygame
import pygame.event
import pygame.locals
from pygame.locals import *

LEVEL_WIDTH		= 41
LEVEL_HEIGHT	= 41

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
	screen = pygame.display.set_mode((300, 300))
	level = Level.Level(LEVEL_WIDTH, LEVEL_HEIGHT)
	# level.style = Tiles.tileStyles[Util.getRandom(1, 15)]
	level.style = Tiles.tileStyles[2]
	# randomizeLevel(level)

	canvas = pygame.Surface((LEVEL_WIDTH * Tiles.TILE_WIDTH, LEVEL_HEIGHT * Tiles.TILE_HEIGHT))

	s_map = ScrollingMap.Scrolling_Map(screen, canvas, Tiles.TILE_HEIGHT, Tiles.TILE_WIDTH)

	maze = MazeGenerator.Maze(10,10).getMap()
	level.applyFeature(maze, 10, 10)

	for i in range(100):
		insertRandomRoom(level)

	stairsUp, upX, upY = level.placeTerrainFeature("stairs-up")
	stairsDown, downX, downY = level.placeTerrainFeature("stairs-down")

	level.connectFeatures() # This really slows things down; need to optimize it. Recommend turning it off while testing

	def draw():
		screen.fill((255, 255, 255))
		level.blit(s_map.image)
		s_map.blit()
	draw()
	done = False
	currentlyDragging = False
	hasDragged = False
	while not done:
		for event in pygame.event.get():
			if event.type in [KEYDOWN, QUIT, JOYBUTTONDOWN]:
				done = True
			elif event.type == MOUSEBUTTONDOWN and event.button == 1:
				# Left mouse button depressed; may be dragging, or may be setting something into a wall
				currentlyDragging = True
				hasDragged = False
			elif event.type == MOUSEBUTTONUP and event.button == 1:
				# Left mouse button released. If we haven't dragged, set it to a wall
				currentlyDragging = None
				if not hasDragged:
					coords = s_map.getClickedCoords(event.pos)
					level.setCell(coords, "#")
					draw()
			elif event.type == MOUSEBUTTONUP and event.button == 3:
				# Right mouse button released; set it to floor
				coords = s_map.getClickedCoords(event.pos)
				level.setCell(coords, ".")
				draw()
			elif currentlyDragging and event.type == MOUSEMOTION:
				# Mouse move with left button held down
				s_map.scroll(event.rel)
				hasDragged = True
			elif event.type == MOUSEBUTTONDOWN and event.button == 4:
				# Scroll wheel up, zoom in (enhance!)
				s_map.scale(.1, event.pos)
			elif event.type == MOUSEBUTTONDOWN and event.button == 5:
				# Scroll wheel down, zoom out
				s_map.scale(-.1, event.pos)

