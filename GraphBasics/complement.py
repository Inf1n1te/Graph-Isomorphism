from basicgraphs import graph
from graphIO import loadgraph, savegraph, inputgraph, printgraph

WorkWithFiles = False


def complement(G):
	n = len(G.V())
	Gc = graph(n)
	for i in range(0, n - 1):
		for j in range(i + 1, n):
			if not G.adj(G[i], G[j]):
				Gc.addedge(Gc[i], Gc[j])
	return Gc


if WorkWithFiles:
	G = loadgraph('examplegraph.gr')
	H = complement(G)
	savegraph(H, 'examplecomplement.gr')
else:
	G = inputgraph()
	H = complement(G)
	printgraph(H)

