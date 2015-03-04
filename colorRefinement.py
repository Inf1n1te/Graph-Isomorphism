__author__ = 'Tim108'

from makegraphs import disjointunion
from graphIO import *

numberOfGraphs = 0
graphlist = []


def refine(g):
	# initialize
	colordict = { }  # dictionary with key=colornum and value=vertex array
	for v in g.V():
		v.colornum = v.deg()
		if v.colornum not in colordict:
			colordict[v.colornum] = [v]
		else:
			colordict[v.colornum].append(v)
	# print(colordict)

	changed = True
	newcolor = max(colordict.keys()) + 1

	while changed:
		tempcolordict = dict()
		for key in colordict.keys():
			buren = tuple()
			for value in colordict[key]:
				nc = sorted(tuple(getNeighbourColors(value)))
				if len(buren) == 0:
					buren = nc
				elif nc != buren:
					tempcolordict[value] = tuple([value.colornum, newcolor])
			# print('step', colordict)
			newcolor = max(colordict.keys()) + 1
		if len(tempcolordict) == 0:
			changed = False
		# print(colordict)
		for value in tempcolordict:
			old = tempcolordict[value][0]
			new = tempcolordict[value][1]
			colordict[old].remove(value)
			value.colornum = new
			if new in colordict:
				colordict[new].append(value)
			else:
				colordict[new] = [value]
	# print(colordict)
	finalcolors = []
	for node in g.V():
		finalcolors.append(node.colornum)

	# DUS HIER SHIT DOEN MET COLORDICT EN DUBBELE KLEUREN ENZO

	# split > compareColor > recursive refine
	done, todo = compareColors(splitColorDict(colordict, g))
	h = disjoint(todo)
	if h is not None:
		return done.extend(refine(h))
	else:
		return done


def getNeighbourColors(v):
	colors = []
	for i in v.nbs():
		colors.append(i.colornum)
	return colors


def compareOLD(x):  # OLD
	graphs = x[0][0]
	global numberOfGraphs
	numberOfGraphs = len(x[0])
	for y in range(1, len(x[0])):
		graphs = disjointunion(graphs, x[0][y])
	coloredgraphs = refine(graphs)
	nrofgraphs = len(x[0])
	partitions = splitlist(range(len(graphs.V())), int(len(graphs.V()) / nrofgraphs))
	split = []
	for j in range(nrofgraphs):
		split.append([])
	for key in coloredgraphs:
		for value in coloredgraphs.get(key):
			for list in partitions:
				if int(value.__repr__()) in list:
					split[partitions.index(list)].append(value.colornum)
	# print(split)
	return split


def compare(graphlisturl):
	global graphlist
	graphlist = loadgraph(graphlisturl, readlist=True)
	return refine(disjoint())


def disjoint(graphnumbers=-1):
	if not graphnumbers:
		return None

	graphs = graphlist[0][0]
	global numberOfGraphs

	if graphnumbers == -1:
		for y in range(1, len(graphlist[0])):
			numberOfGraphs = len(graphlist[0])
			graphs = disjointunion(graphs, graphlist[0][y])
	else:
		numberOfGraphs = len(graphnumbers)
		print("---", numberOfGraphs, graphnumbers)
		graphs = graphlist[0][graphnumbers.pop(0)]
		for y in graphnumbers:
			graphs = disjointunion(graphs, graphlist[0][y])
	return graphs


def splitColorDict(colordict, g):
	partitions = splitlist(range(len(g.V())), int(len(g.V()) / numberOfGraphs))
	print(numberOfGraphs, len(partitions))
	split = []
	for j in range(numberOfGraphs):
		split.append([])
	for key in colordict:
		for value in colordict.get(key):
			for e in partitions:
				if int(value.__repr__()) in e:
					split[partitions.index(e)].append(value.colornum)
	# print(split)
	return split


def comparegraphs(x):  # OLD
	r = []
	ccs = compare(x)
	undecided = []
	for i in range(len(ccs)):
		if len(ccs[i]) > len(set(ccs[i])):
			undecided.append(i)
	for i in range(len(ccs)):
		for j in range(len(ccs)):
			if i != j and i < j:
				if ccs[i] == ccs[j] and i not in undecided:
					r.append([i, j])
	return r, "-----", undecided


def compareColors(split):
	r = []
	undecided = []
	for i in range(len(split)):
		if len(split[i]) > len(set(split[i])):
			undecided.append(i)
	for i in range(len(split)):
		for j in range(len(split)):
			if i != j and i < j:
				if split[i] == split[j] and i not in undecided:
					r.append([i, j])
	return r, undecided


def splitlist(l, n):
	return [l[i:i + n] for i in range(0, len(l), n)]


# print(splitList([1, 2, 3, 4, 5, 6, 7, 8], 3))
print(compare("GI_TestInstancesWeek1/crefBM_4_7.grl"))
