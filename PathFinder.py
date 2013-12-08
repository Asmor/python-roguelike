import heapq

def FindPath(level, start, end):
	COST = 1
	STEPS = 2
	validX = range(level.width)
	validY = range(level.height)
	unvisited = [[True for i in validY] for i in validX]
	unvisited[start[0]][start[1]] = False
	paths = []
	heapq.heappush(paths, (0, 0, [start]))
	while True:
		if len(paths) == 0:
			return False
		best = heapq.heappop(paths)
		lastStep = best[STEPS][-1]
		if lastStep == end:
			return best[STEPS]
		for neighbor in ((0, -1), (1, 0), (0, 1), (-1, 0)):
			x = lastStep[0] + neighbor[0]
			y = lastStep[1] + neighbor[1]
			if x in validX and y in validY and unvisited[x][y]:
				unvisited[x][y] = False
				cell = level.getCell((x, y))
				if cell.immutable and not cell.passable:
					# We don't want to dig through an immutable wall
					continue
				cost = best[COST] + cell.digCost
				steps = best[STEPS][:] # clone list
				steps.append((x, y))
				heapq.heappush(paths, (cost + computeOffset(steps[-1], end), cost, steps))

def computeOffset(start, end):
	return abs((start[0] - end[0])) + abs((start[1] - end[1]))

if __name__ == '__main__':
	print computeOffset((0,1), (1,0))
	pass