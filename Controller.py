from pygame.locals import *

UP = 0
UP_RIGHT = 1
RIGHT = 2
DOWN_RIGHT = 3
DOWN = 4
DOWN_LEFT = 5
LEFT = 6
UP_LEFT = 7

class Controller(object):
	def __init__(self, s_map, pc):
		self.map = s_map
		self.pc = pc
		self.currentlyDragging = False
		self.hasDragged = False

	def dispatch(self, event):
		# Return true = quit
		if event.type == QUIT:
			return True
		elif event.type == KEYDOWN:
			if event.key == K_ESCAPE:
				return True
			elif event.key == K_KP5:
				# TODO: This is the 'wait' command
				pass
			elif event.key == K_KP8:
				self.pc.move(UP)
			elif event.key == K_KP9:
				self.pc.move(UP_RIGHT)
			elif event.key == K_KP6:
				self.pc.move(RIGHT)
			elif event.key == K_KP3:
				self.pc.move(DOWN_RIGHT)
			elif event.key == K_KP2:
				self.pc.move(DOWN)
			elif event.key == K_KP1:
				self.pc.move(DOWN_LEFT)
			elif event.key == K_KP4:
				self.pc.move(LEFT)
			elif event.key == K_KP7:
				self.pc.move(UP_LEFT)

			self.map.blit()
		elif event.type == MOUSEBUTTONDOWN and event.button == 1:
			# Left mouse button depressed; may be dragging, or may be setting something into a wall
			self.currentlyDragging = True
			self.hasDragged = False
		elif event.type == MOUSEBUTTONUP and event.button == 1:
			# Left mouse button released. If we haven't dragged, set it to a wall
			self.currentlyDragging = None
			if not self.hasDragged:
				coords = self.map.getClickedCoords(event.pos)
				self.map.setCell(coords, "#")
		elif event.type == MOUSEBUTTONUP and event.button == 3:
			# Right mouse button released; set it to floor
			coords = self.map.getClickedCoords(event.pos)
			self.map.setCell(coords, ".")
		elif self.currentlyDragging and event.type == MOUSEMOTION:
			# Mouse move with left button held down
			self.map.scroll(event.rel)
			self.hasDragged = True
		elif event.type == MOUSEBUTTONDOWN and event.button == 4:
			# Scroll wheel up, zoom in (enhance!)
			self.map.scale(True, event.pos)
		elif event.type == MOUSEBUTTONDOWN and event.button == 5:
			# Scroll wheel down, zoom out
			self.map.scale(False, event.pos)

		return False
