import random
import math

def getXYByDist(distance, direction):
	"""Given an angle in radians and a distance, gives an integer (x, y) tuple"""
	y = int(distance * math.sin(direction))
	x = int(distance * math.cos(direction))
	return (x, y)

def getRandomAngle():
	"""Returns a random angle between 0 and 2pi radians"""
	return random.random() * math.pi * 2

# via http://roguebasin.roguelikedevelopment.org/index.php?title=Bresenham%27s_Line_Algorithm#Python
def getLine(start, end):
	x1 = start[0]
	y1 = start[1]
	x2 = end[0]
	y2 = end[1]
	points = []
	issteep = abs(y2-y1) > abs(x2-x1)
	if issteep:
		x1, y1 = y1, x1
		x2, y2 = y2, x2
	rev = False
	if x1 > x2:
		x1, x2 = x2, x1
		y1, y2 = y2, y1
		rev = True
	deltax = x2 - x1
	deltay = abs(y2-y1)
	error = int(deltax / 2)
	y = y1
	ystep = None
	if y1 < y2:
		ystep = 1
	else:
		ystep = -1
	for x in range(x1, x2 + 1):
		if issteep:
			points.append((y, x))
		else:
			points.append((x, y))
		error -= deltay
		if error < 0:
			y += ystep
			error += deltax
	# Reverse the list if the coordinates were reversed
	if rev:
		points.reverse()
	return points

if __name__ == '__main__':
	print getXYByDist(math.pi*2, 10)
	pass