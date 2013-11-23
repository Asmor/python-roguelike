def getEdges(points):
	edges = []
	rng = range(len(points))
	for i in rng:
		p = points[i]
		for j in rng[i+1:]:
			q = points[j]
			if neighbors(p, q, points):
				edges.append((p, q))
	return edges

def neighbors(p, q, points):
	d = distSq(p, q)
	for r in points:
		if r == p or r == q:
			continue
		if distSq(p, r) < d and distSq(q, r) < d:
			return False
	return True

def distSq(p, q):
	return (p[0] - q[0])**2 + (p[1] - q[1])**2

if __name__ == '__main__':
	points = (
		(1, 1),
		(3, 4),
		(7, -2),
		(12, 0),
		(13, 7)
	)

	print getEdges(points)
