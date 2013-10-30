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

if __name__ == '__main__':
	print getXYByDist(math.pi*2, 10)
	pass