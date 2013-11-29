from Level import Level
from ScrollingMap import Scrolling_Map
from Tiles import TILE_WIDTH, TILE_HEIGHT, tileStyles
from Controller import Controller
import pygame

pygame.init()
screen = pygame.display.set_mode((1000, 1000))

s_map = Scrolling_Map(screen, TILE_WIDTH, TILE_HEIGHT)
level = Level(30)
s_map.level = level

canvas = pygame.Surface((
	level.dungeon.mapWidth * TILE_WIDTH,
	level.dungeon.mapHeight * TILE_HEIGHT
))

if False:
	# Overlays a diagram of the connections on the map. Looks pretty.
	color = (255, 0, 0)
	for path in level.dungeon.connectedRooms:
		start = path[0]
		end = path[1]
		s_map.drawLine(color, start, end)

s_map.blit()

# Main game loop and related variables
controller = Controller(s_map)

done = False
while not done:
	for event in pygame.event.get():
		done = done or controller.dispatch(event)
