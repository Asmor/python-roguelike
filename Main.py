from Level import Level
from ScrollingMap import Scrolling_Map
from Tiles import TILE_WIDTH, TILE_HEIGHT, tileStyles
import pygame
import pygame.locals
import time
from pygame.locals import *

level = Level(30)

pygame.init()
screen = pygame.display.set_mode((1000, 1000))

canvas = pygame.Surface((
	level.dungeon.mapWidth * TILE_WIDTH,
	level.dungeon.mapHeight * TILE_HEIGHT
))

s_map = Scrolling_Map(screen, canvas, TILE_WIDTH, TILE_HEIGHT)

def draw():
	screen.fill((255, 255, 255))
	level.blit(s_map.terrainLayer)
	s_map.blit()
draw()

if True:
	# Overlays a diagram of the connections on the map. Looks pretty.
	color = (255, 0, 0)
	for path in level.dungeon.connectedRooms:
		start = path[0]
		end = path[1]
		s_map.drawLine(color, start, end)

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

print time.clock()