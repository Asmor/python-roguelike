import random
import math

def getRandom(min, max):
	return int((random.random() * (max + 1 - min)) + min)

if __name__ == '__main__':
	print(getRandom(0, 10))