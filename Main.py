import NewDungeonGenerator
import Level
import Cell
import ScrollingMap
import Tiles
import pygame
import pygame.locals
from pygame.locals import *

dungeon = NewDungeonGenerator.Dungeon(150)
level = Level.Level.FromGrid(dungeon.map)

# for row in dungeon.map:
# 	print "".join(row)

pygame.init()
screen = pygame.display.set_mode((1000, 1000))
level.style = Tiles.tileStyles[2]

canvas = pygame.Surface((
	dungeon.mapWidth * Tiles.TILE_WIDTH,
	dungeon.mapHeight * Tiles.TILE_HEIGHT
))

s_map = ScrollingMap.Scrolling_Map(screen, canvas, Tiles.TILE_WIDTH, Tiles.TILE_HEIGHT)

def draw():
	screen.fill((255, 255, 255))
	level.blit(s_map.image)
	s_map.blit()
draw()

# Main game loop and related variables
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

