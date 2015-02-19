from graphIO import loadgraph, writeDOT


def BFS(G, startvert):
	marked = { startvert: 0 }
	queue = [startvert]
	visited = 0
	maxdist = 0

	while len(queue) > 0:
		v = queue[0]
		queue = queue[1:]
		v.label = visited  # labeled by visiting-order
		visited += 1

		for w in v.nbs():
			if not w in marked:
				marked[w] = marked[v] + 1  # for BFS: this is the *distance* to startvert
				if marked[w] > maxdist:
					maxdist = marked[w]
				queue.append(w)

	if visited < len(G.V()):
		print("G is not connected: visited", visited, "out of", len(G.V()))
	else:
		print("G is connected")
	print("Maximum distance from startvertex:", maxdist)


def DFS(G, startvert):
	marked = { }
	stack = [startvert]
	visited = 0

	while len(stack) > 0:
		v = stack.pop()
		if not v in marked:  # vertices may have been visited but still on stack!
			marked[v] = 1
			v.label = visited  # labeled by visiting-order
			visited += 1

			N = v.nbs()
			# Use this to get the same result as the recursive version!:
			# N.reverse()
			for w in N:
				stack.append(w)

	if visited < len(G.V()):
		print("G is not connected: visited", visited, "out of", len(G.V()))
	else:
		print("G is connected")


def DFSrecursive(G, startvert):
	def DFSrecurse(currentvert):
		nonlocal visited, processed

		marked[currentvert] = 1
		currentvert.label = visited
		visited += 1

		for w in currentvert.nbs():
			if not w in marked:
				DFSrecurse(w)
		currentvert.postorder = processed
		processed += 1

	marked = { }
	visited = 0
	processed = 0
	DFSrecurse(startvert)
	if visited < len(G.V()):
		print("G is not connected: visited", visited, "out of", len(G.V()))
	else:
		print("G is connected")


if __name__ == "__main__":
	G = loadgraph('examplegraph.gr')
	for v in G:
		v.colornum = v._label

	BFS(G, G[0])
	writeDOT(G, 'exgr_bfs.dot')

	DFS(G, G[0])
	writeDOT(G, 'exgr_dfs.dot')

	DFSrecursive(G, G[0])
	writeDOT(G, 'exgr_dfsrec.dot')
	for v in G:
		v.label = v.postorder
	writeDOT(G, 'exgr_dfsrec_postorder.dot')

