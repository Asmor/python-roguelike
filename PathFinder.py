def FindPath(level, start, end):
	validX = range(level.width)
	validY = range(level.height)
	unvisited = [[True for i in validY] for i in validX]
	unvisited[start[0]][start[1]] = False
	paths = [{
		"cost": 0,
		"steps": [start],
		"digLength": 0
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
				cost = best["cost"] + cell.digCost
				digLength = best["digLength"]
				# if cell.passable:
				# 	if digLength == 2:
				# 		# We want to avoid tunnels exactly 2-spaces long, because it makes adjacent doors and that's ugly
				# 		cost += 10000
				# 	else:
				# 		digLength = 0
				# else:
				# 	digLength += 1
				steps = best["steps"][:]
				steps.append((x, y))
				paths.append({
					"cost": cost,
					"steps": steps,
					"digLength": digLength
				})



def computeOffset(start, end):
	return abs((start[0] - end[0])) + abs((start[1] - end[1]))

if __name__ == '__main__':
	print computeOffset((0,1), (1,0))
	pass