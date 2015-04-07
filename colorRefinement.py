__author__ = 'Tim (& [Jeroen])'

import time
import copy

from makegraphs import disjointunion
from graphIO import *
from basicgraphs import graph


def fastrefine(g, colordictarg=-1, startcolor=-1, preproc=False):
	if colordictarg is -1:
		if g.colordict == -1:
			if not preproc:
				colordict = degcolordict(g)
			else:
				colordict = preproccolordict(g)
		else:
			if not preproc:
				colordict = g.colordict
			else:
				colordict = preproccolordict
	else:
		colordict = colordictarg

	if startcolor is -1:
		shortest = min(colordict.keys())
		for key in colordict.keys():
			if len(colordict[key]) <= len(colordict[shortest]):
				shortest = key
		queue = [shortest]
	else:
		queue = [startcolor]

	applycolors(colordict)
	nextcolor = max(colordict.keys()) + 1

	i = 0
	while i < len(queue):
		connectednodes = dict()
		for value in colordict[queue[i]]:
			for nb in value.nbs():  # make colordict of neighbours
				if nb.colornum not in connectednodes:
					connectednodes[nb.colornum] = [nb]
				elif nb not in connectednodes[nb.colornum]:
					connectednodes[nb.colornum].append(nb)

		for key in connectednodes.keys():
			colordictchanged = False
			colordict[key].sort(key=lambda x: x._label)
			connectednodes[key].sort(key=lambda x: x._label)
			if colordict[key] == connectednodes[key]:
				pass
			elif key not in queue and len(colordict[key]) < len(connectednodes[key]):
				queue.append(key)
				colordictchanged = True
			else:
				queue.append(nextcolor)
				colordictchanged = True

			if colordictchanged:
				for vertex in connectednodes[key]:
					vertex.colornum = nextcolor
				g.generatecolordict()
				colordict = g.getcolordict()
				nextcolor += 1
		i += 1
	return colordict


def degcolordict(g):
	colordict = {}  # dictionary with key=c and value=vertex array
	for v in g.V():
		v.colornum = v.deg()
		if v.colornum not in colordict:
			colordict[v.colornum] = [v]
		else:
			colordict[v.colornum].append(v)
	return colordict


def preproccolordict(g):
	colordict = {}  # dictionary with key=c and value=vertex array
	for v in g.V():
		if not v.twin:
			v.colornum = v.deg()
		if v.colornum not in colordict:
			colordict[v.colornum] = [v]
		else:
			colordict[v.colornum].append(v)
	return colordict


def getNeighbourColors(v):
	colors = []
	for i in v.nbs():
		colors.append(i.colornum)
	return colors


def compare(graphlisturl=-1, GI_only=False, gs=-1, preproc=False):
	print('Now comparing graphs in graphlist ', graphlisturl)

	if gs is -1:
		graphlist = loadgraph(graphlisturl, readlist=True)[0]
	else:
		graphlist = gs
	g = graphlist[0]
	subgraphlist = []
	subgraphlist.append(len(g.V()))
	for i in range(1, len(graphlist)):  # make one big graph from the graphlist
		h = graphlist[i]
		g = disjointunion(g, h)
		subgraphlist.append(len(h.V()))
	g.subgraphs = subgraphlist

	if preproc:
		colordict = fastrefine(g, preproc=True)
	else:
		colordict = fastrefine(g)
	graphcolors = splitColorDict(colordict, g)[0]  # is a list of colordicts
	isomorphisms = []
	undecided = []

	for i in range(len(graphcolors)):  # find isomorphisms
		for j in range(len(graphcolors)):
			if i < j:
				if graphcolors[i].keys() == graphcolors[j].keys():
					iso = True
					single = True
					for key in graphcolors[i].keys():
						if not (len(graphcolors[i][key]) is len(graphcolors[j][key])):
							iso = False
						if len(graphcolors[i][key]) > 1:
							single = False
					if iso and not single:
						undecided.append([i, j])
					elif iso and single:
						isomorphisms.append([i, j, 1])

	for tuple in undecided:
		first = tuple[0]
		second = tuple[1]
		tempgraph = disjointunion(graphlist[first], graphlist[second])
		num = countIsomorphism(tempgraph, fastrefine(tempgraph), GI_only)
		if num > 0:
			isomorphisms.append([first, second, num])

	printresult(isomorphisms)

	return colordict


def printresult(isomorphims):
	print("Set of isomorphismic graphs:", "\t\t", "Number of isomorphismes")
	for tuple in isomorphims:
		print([tuple[0], tuple[1]], "\t\t\t\t\t\t\t\t", tuple[2])
	return


def countIsomorphism(graph, hasColordict=False, GI_only=False):
	if hasColordict is False:
		colordict = fastrefine(graph)
	else:
		colordict = fastrefine(graph, hasColordict)
	isomorphism = True
	colors = []
	cvar = -1
	for c in colordict.keys():
		length = len(colordict[c])
		if length >= 4:  # if there are more than 4 elemts in colordict[c], it means there are duplicates
			colorlength = len(colors)
			if colorlength == 0 or length <= colorlength:
				colors = colordict[c]  # add these to colors.
				cvar = c
				isomorphism = False  # meaning we found no isomorphism again
		if length % 2 == 1:
			return 0
	if isomorphism:
		return 1
	else:
		onehalf = colors[0:int(len(colors) / 2)]
		otherhalf = colors[int((len(colors) / 2)):(len(colors))]
		index = 0
		x = colors[index]  # we'lls tart with the first color
		num = 0
		for y in otherhalf:  # get the middle of colors[] (as it skips the first half)s
			if GI_only and num > 0:
				break
			newcolor = max(graph.getcolordict().keys()) + 1  # assign a new color
			applycolors(colordict)

			colordict[cvar].remove(x)
			colordict[cvar].remove(y)
			colordict[newcolor] = [x]
			colordict[newcolor].append(y)

			applycolors(colordict)
			graph2 = copy.deepcopy(graph)
			graph2.generatecolordict()
			colordict2 = graph2.getcolordict()

			colordict.pop(newcolor)
			colordict[cvar].append(x)
			colordict[cvar].append(y)

			num += countIsomorphism(graph2, colordict2, GI_only)
	return num


def applycolors(colordict):
	for color in colordict.keys():
		for node in colordict[color]:
			node.colornum = color


def splitColorDict(colordict, g):
	subgraphsl = g.subgraphs
	number = 0
	partitions = []
	split = []
	split2 = []
	for i in range(len(subgraphsl)):
		partitions.append(list(range(number, number + subgraphsl[i])))
		number += subgraphsl[i]
		split.append(dict())
		split2.append([])

	for key in colordict:
		for value in colordict.get(key):
			for e in partitions:
				if int(value.__repr__()) in e:
					if key in split[partitions.index(e)].keys():
						split[partitions.index(e)][key].append(value)
					else:
						split[partitions.index(e)][key] = [value]
					# split[partitions.index(e)].append(value.colornum)
					split2[partitions.index(e)].append((value.colornum, value))
	return split, split2


def compareColors(split):
	global undecidedGraphs
	r = []
	for i in range(len(split)):
		if len(split[i]) > len(set(split[i])):
			undecidedGraphs.append(i)
	for i in range(len(split)):
		for j in range(len(split)):
			if i != j and i < j:
				if split[i] == split[j] and i not in undecidedGraphs:
					r.append([i, j])
	return r, undecidedGraphs


def gettwins(g):
	nbs = []
	nbs2 = []
	# start_time = time.clock()
	for vertex in g.V():
		nb = vertex.nbs()[:]
		nb.sort(key=lambda x: x._label)
		nbs.append(tuple(nb))
		nb.append(vertex)
		nb.sort(key=lambda x: x._label)  # kan sneller?
		nbs2.append(tuple(nb))
	falsetwins = {}
	twins = {}
	for i, item in enumerate(nbs):
		if item in falsetwins.keys():
			falsetwins[item].append(g.V()[i])
		else:
			falsetwins[item] = [g.V()[i]]
	for i, item in enumerate(nbs2):
		if item in twins.keys():
			twins[item].append(g.V()[i])
		else:
			twins[item] = [g.V()[i]]
	falsetwins = {k: v for k, v in falsetwins.items() if len(v) > 1}
	twins = {k: v for k, v in twins.items() if len(v) > 1}
	return list(falsetwins.values()), list(twins.values()), list(falsetwins.keys()), list(
		twins.keys())  # value zijn twins


def preprocessing(g):
	falsetwins, twins, falsetwinsN, twinsN = gettwins(g)
	lftwins = len(falsetwins)
	ltwins = len(twins)
	if lftwins != 0 or ltwins != 0:
		deledges = []
		for i, e in enumerate(g._E):
			if any(e._tail in ftwin for ftwin in falsetwins) or any(e._head in ftwin for ftwin in falsetwins) or any(
							e._tail in twin for twin in twins) or any(e._head in twin for twin in twins):
				deledges.append(i)
		deledges.sort(reverse=True)
		for i in deledges:
			g._E.pop(i)
		delnodes = []
		for i, V in enumerate(g._V):
			if any(V in ftwin for ftwin in falsetwins) or any(V in twin for twin in twins):
				delnodes.append(i)
		delnodes.sort(reverse=True)
		for i in delnodes:
			g._V.pop(i)
		# Alles opnieuw aanmaken
		combined = falsetwinsN + twinsN
		mx = 0
		for i, twin in enumerate(falsetwins):
			g.addvertexobject(twin[0], True, len(twin))
			twin[0].colornum = -twin[0].twinsize
			mx = max(mx, len(twin))
		for i, twin in enumerate(twins):
			g.addvertexobject(twin[0], True, len(twin) + mx)
			twin[0].colornum = -twin[0].twinsize - mx
		for i, twin in enumerate(falsetwins + twins):
			for j in combined[i]:
				if j in g.V() and twin[0] != j and not g.findedge(twin[0],j):
					g.addedge(twin[0], j)
		g._V.sort(key=lambda x: x._label)
	return g, lftwins, ltwins


def comparepreproc(graphlisturl, GI_only=False):
	start_time = time.clock()
	global graphlist
	graphlist = loadgraph(graphlisturl, readlist=True)
	ngraphs = len(graphlist[0])
	nfalsetwins, ntwins = [None] * ngraphs, [None] * ngraphs
	for i in range(ngraphs):
		# print(findcomponents(graphlist[0][1]))
		graphlist[0][i], nfalsetwins[i], ntwins[i] = preprocessing(graphlist[0][i])
	print('number of twins:', nfalsetwins, ntwins)
	elapsed_time = time.clock() - start_time
	print('Preprocessing: {0:.4f} sec'.format(elapsed_time))
	return compare(gs=graphlist[0], preproc=True, GI_only=True)


def connected(v, ncomponents, g):
	for vertex in v.nbs():
		if not vertex.visited:
			vertex.visited = True
			vertex.component = ncomponents
			connected(vertex, ncomponents, g)


def findcomponents(g):
	ncomponents = 0
	for vertex in g.V():
		if not vertex.visited:
			vertex.visited = True
			ncomponents += 1
			vertex.component = ncomponents
			connected(vertex, ncomponents, g)
	return ncomponents


def componentgraphs(graphlisturl):
	start_time = time.clock()
	global graphlist
	graphlist = loadgraph(graphlisturl, readlist=True)
	print(graphlist)
	ngraphs = len(graphlist[0])
	subgraphlist = []
	for i in range(ngraphs):
		ncomponents = findcomponents(graphlist[0][i])
		if i > 0:
			mincomponents = min(mincomponents, ncomponents)
		else:
			mincomponents = ncomponents
		g = graphlist[0][i]
		if ncomponents > 1:
			graphs = []
			for component in range(ncomponents + 1):
				if component != ncomponents:
					graphs.append(graph())
				for vertex in g.V():
					if vertex.component == component:
						graphs[component - 1].addvertexobject(vertex)
						for edge in vertex.inclist():
							if edge not in graphs[component - 1].E():
								graphs[component - 1].addedgeobject(edge)
		subgraphlist.append(graphs)
	# print(subgraphlist[2])



	elapsed_time = time.clock() - start_time
	print('Components: {0:.4f} sec'.format(elapsed_time))

start_time = time.clock()

# compare("GI_TestInstancesWeek1/products72.grl", False)  # #aut for product72
# compare("GI_TestInstancesWeek1/torus72.grl", False)  # #aut for torus72
# compare("GI_TestInstancesWeek1/cubes6.grl", True)  # GI for cubes6
# compare("GI_TestInstancesWeek1/bigtrees3.grl", True)  # GI for bigtrees3
#
# comparepreproc("GI_TestInstancesWeek1/cographs1.grl")  # GI for cographs1 with preprocessing
#comparepreproc("GI_TestInstancesWeek1/products72.grl")  # GI for cographs1 with preprocessing

componentgraphs("GI_TestInstancesWeek1/cographs1.grl")


elapsed_time = time.clock() - start_time
print('Time: {0:.4f} sec'.format(elapsed_time))

