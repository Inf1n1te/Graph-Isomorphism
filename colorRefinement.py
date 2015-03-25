__author__ = 'Tim (& [Jeroen])'

import time

from makegraphs import disjointunion
from graphIO import *


numberOfGraphs = 0
undecidedGraphs = []
graphlist = []


def refine(g):
	# initialize
	colordict = {}  # dictionary with key=colornum and value=vertex array
	for v in g.V():
		v.colornum = v.deg()
		if v.colornum not in colordict:
			colordict[v.colornum] = [v]
		else:
			colordict[v.colornum].append(v)

	done = False
	print('start while')
	start_time = time.clock()
	elapsed_time = time.clock() - start_time
	print('a: {0:.4f} sec'.format(elapsed_time))
	counter = 0
	while not done:
		done = True
		counter += 1
		if counter % 100 == 0:
			print(counter)
		tempcolordict = dict()

		for key in colordict.keys():
			nextcolor = max(colordict.keys()) + 1
			buren = tuple()
			for value in colordict[key]:
				nc = sorted(tuple(getNeighbourColors(value)))
				if len(buren) == 0:
					buren = nc

				if buren != nc:
					done = False
					if nextcolor in tempcolordict:
						tempcolordict[nextcolor].append(value)
					else:
						tempcolordict[nextcolor] = [value]

				else:
					if key in tempcolordict:
						tempcolordict[key].append(value)
					else:
						tempcolordict[key] = [value]

		colordict = tempcolordict.copy()

		for key in colordict.keys():
			for value in colordict[key]:
				value.colornum = key

	finalcolors = []
	for node in g.V():
		finalcolors.append(node.colornum)

	print('end of while')
	elapsed_time = time.clock() - start_time
	print('Time: {0:.4f} sec'.format(elapsed_time))
	# DUS HIER SHIT DOEN MET COLORDICT EN DUBBELE KLEUREN ENZO
	result = compareColors(splitColorDict(colordict, g)[0])
	if len(undecidedGraphs) > 0:
		print(undecidedGraphs)
		findDuplicates(splitColorDict(colordict, g)[1])
	return result


def getNeighbourColors(v):
	colors = []
	for i in v.nbs():
		colors.append(i.colornum)
	return colors


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
		graphs = graphlist[0][graphnumbers.pop(0)]
		for y in graphnumbers:
			graphs = disjointunion(graphs, graphlist[0][y])
	return graphs


def splitColorDict(colordict, g):
	partitions = splitlist(range(len(g.V())), int(len(g.V()) / numberOfGraphs))
	split = []
	split2 = []
	for j in range(numberOfGraphs):
		split.append([])
		split2.append([])
	for key in colordict:
		for value in colordict.get(key):
			for e in partitions:
				if int(value.__repr__()) in e:
					split[partitions.index(e)].append(value.colornum)
					split2[partitions.index(e)].append((value.colornum, value))
	# print(split)
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


def splitlist(l, n):
	return [l[i:i + n] for i in range(0, len(l), n)]


# Alleen False Twins werkt nog
def preprocessing(g):  # Maakt modules van (False) Twins (improvement 2)
	falsetwins = {}
	twins = {}
	for i in range(len(g.V())):
		vertex1 = g.V()[i]
		nbs1 = tuple(vertex1.nbs())
		nbs1app = vertex1.nbs()
		print(nbs1app, i)
		nbs1app.append(vertex1)
		nbs1ext = tuple(nbs1app)
		for vertex2 in g.V()[i + 1:]:
			nbs2 = tuple(vertex2.nbs())
			nbs2app = vertex2.nbs()
			nbs2app.append(vertex2)
			nbs2ext = tuple(nbs2app)
			# print(nbs1ext,nbs2ext)
			if nbs1 == nbs2:  # False twins
				if nbs1 in falsetwins.keys():
					falsetwins[nbs1].append(vertex1)
					falsetwins[nbs1].append(vertex2)
				else:
					falsetwins[nbs1] = [vertex1, vertex2]
			elif nbs1ext == nbs2ext:  # Twins
				if nbs1ext in twins.keys():
					twins[nbs1ext].append(vertex1)
					twins[nbs1ext].append(vertex2)
				else:
					twins[nbs1ext] = [vertex1, vertex2]
	return falsetwins, twins


def findDuplicates(split2):
	# split2: lijst met tupels (colornum, vertices)
	# IN case we do need the sort:
	# for e in split2:
	# sorted(e, key=lambda x: x[0])
	print(split2)
	result = {}
	for e in range(len(split2)):
		if e in undecidedGraphs:
			newDict = {}
			result[e] = []
			i = 0
			while i < len(split2[e]) - 1:
				if split2[e][i][0] == split2[e][i + 1][0]:
					x = 2
					newList = [split2[e][i][1], split2[e][i + 1][1]]
					while (i + x) < len(split2[e]) - 1 and split2[e][i][0] == split2[e][i + x][0]:
						newList.append(split2[e][i + x][1])
						x += 1
					newDict[split2[e][i][0]] = newList
					i += x
				else:
					i += 1
			result[e].append(newDict)
	print(result)
	return result


def f


def individualizationRefinement():
	return 0


print(compare("GI_TestInstancesWeek1/crefBM_6_15.grl"))