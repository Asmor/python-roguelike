from pygame.locals import *

class Controller(object):
	def __init__(self, s_map):
		self.map = s_map
		self.currentlyDragging = False
		self.hasDragged = False

	def dispatch(self, event):
		if event.type in [QUIT]:
			return True
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
