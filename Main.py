from Level import Level
from ScrollingMap import Scrolling_Map
from Tiles import TILE_WIDTH, TILE_HEIGHT, tileStyles
import pygame
import pygame.locals
import time
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((1000, 1000))

s_map = Scrolling_Map(screen, TILE_WIDTH, TILE_HEIGHT)
level = Level(30)
s_map.setLevel(level)

canvas = pygame.Surface((
	level.dungeon.mapWidth * TILE_WIDTH,
	level.dungeon.mapHeight * TILE_HEIGHT
))

def draw():
	screen.fill((255, 255, 255))
	s_map.blit()

if False:
	# Overlays a diagram of the connections on the map. Looks pretty.
	color = (255, 0, 0)
	for path in level.dungeon.connectedRooms:
		start = path[0]
		end = path[1]
		s_map.drawLine(color, start, end)
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
			s_map.scale(True, event.pos)
		elif event.type == MOUSEBUTTONDOWN and event.button == 5:
			# Scroll wheel down, zoom out
			s_map.scale(False, event.pos)

