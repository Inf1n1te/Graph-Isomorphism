__author__ = 'Tim (& [Jeroen])'

import time

from makegraphs import disjointunion
from graphIO import *


numberOfGraphs = 0
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
			newcolor = max(colordict.keys()) + 1
			buren = tuple()
			for value in colordict[key]:
				nc = sorted(tuple(getNeighbourColors(value)))
				if len(buren) == 0:
					buren = nc

				if buren != nc:
					done = False
					if newcolor in tempcolordict:
						tempcolordict[newcolor].append(value)
					else:
						tempcolordict[newcolor] = [value]

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
	return compareColors(splitColorDict(colordict, g))


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
	for j in range(numberOfGraphs):
		split.append([])
	for key in colordict:
		for value in colordict.get(key):
			for e in partitions:
				if int(value.__repr__()) in e:
					split[partitions.index(e)].append(value.colornum)
	# print(split)
	return split


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


# Alleen False Twins werkt nog
def preprocessing(g):  # Maakt modules van (False) Twins (improvement 2)
	falsetwins = {}
	twins = {}
	for i in range(len(g.V())):
		vertex1 = g.V()[i]
		nbs1 = vertex1.nbs()
		# nbs1ext = nbs1[:]
		#nbs1 = tuple(nbs1)
		#nxt = next((x for x in nbs1ext if x._label > vertex1._label), None)
		#print(nxt, type(nxt))
		#nbs1ext.insert(nxt-1, vertex1)
		#nbs1ext = tuple(nbs1ext)
		for vertex2 in g.V()[i + 1:]:
			nbs2 = vertex2.nbs()
			# nbs2ext = nbs2[:]
			#nbs2ext.append(vertex2)
			#nbs2 = tuple(nbs2)
			#nbs2ext.sort(key=lambda x: x._label)
			#nbs2ext = tuple(nbs2ext)
			# print(nbs1,nbs2,nbs1ext, nbs2ext)
			if nbs1 == nbs2:  #False twins
				if nbs1 in falsetwins.keys():
					falsetwins[nbs1].append(vertex1)
					falsetwins[nbs1].append(vertex2)
				else:
					falsetwins[nbs1] = [vertex1, vertex2]
				# elif nbs1ext == nbs2ext:  # Twins
				#	if nbs1ext not in twins.keys():
				#		twins[nbs1ext] = nbs1ext
	return list(falsetwins.keys())  #, list(twins.keys())


# test preprocessing
print('start while')
start_time = time.clock()
aa = loadgraph("GI_TestInstancesWeek1/crefBM_4_4098.grl", readlist=False)
print(preprocessing(aa))
elapsed_time = time.clock() - start_time
print('a: {0:.4f} sec'.format(elapsed_time))


#print(compare("GI_TestInstancesWeek1/crefBM_4_16.grl"))
