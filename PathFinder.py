def FindPath(level, start, end):
	validX = range(level.width)
	validY = range(level.height)
	unvisited = [[True for i in validY] for i in validX]
	unvisited[start[0]][start[1]] = False
	paths = [{
		"cost": 0,
		"steps": [start]
	}]
	while True:
		paths.sort(key=lambda path: path["cost"] + computeOffset(path["steps"][-1], end))
		if len(paths) == 0:
			return False
		best = paths[0]
		paths = paths[1:]
		lastStep = best["steps"][-1]
		if lastStep == end:
			return best["steps"]
		for neighbor in ((0, -1), (1, 0), (0, 1), (-1, 0)):
			x = lastStep[0] + neighbor[0]
			y = lastStep[1] + neighbor[1]
			if x in validX and y in validY and unvisited[x][y]:
				unvisited[x][y] = False
				cell = level.getCell(x, y)
				if cell.immutable and not cell.passable:
					# We don't want to dig through an immutable wall
					continue
				cost = best["cost"] + cell.digCost
				steps = best["steps"][:]
				steps.append((x, y))
				paths.append({
					"cost": cost,
					"steps": steps
				})



def computeOffset(start, end):
	return abs((start[0] - end[0])) + abs((start[1] - end[1]))

if __name__ == '__main__':
	print computeOffset((0,1), (1,0))
	pass