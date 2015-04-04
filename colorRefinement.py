__author__ = 'Tim (& [Jeroen])'

import time

from makegraphs import disjointunion
from graphIO import *


def fastrefine(g, colordict=-1, startcolor=-1):
	if colordict is -1:
		colordict = degcolordict(g)

	if startcolor is -1:
		shortest = min(colordict.keys())
		for key in colordict.keys():
			if len(colordict[key]) <= len(colordict[shortest]):
				shortest = key
		queue = [shortest]
	else:
		queue = [startcolor]

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
				colordict = g.getcolordict()
				nextcolor += 1
		i += 1
	# try:
	# return compareColors(splitColorDict(colordict, g)[0])
	# except:
	# print('its only one graph apparently')
	return colordict


def refine(g):
	# initialize
	colordict = degcolordict(g)

	done = False
	start_time = time.clock()
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
	try:
		result = compareColors(splitColorDict(colordict, g)[0])
		if len(undecidedGraphs) > 0:
			print(undecidedGraphs)
			findDuplicates(splitColorDict(colordict, g)[1])
		return result
	except:
		print('its only one graph apparently')
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


def getNeighbourColors(v):
	colors = []
	for i in v.nbs():
		colors.append(i.colornum)
	return colors


def compare(graphlisturl=-1, gs=-1):
	assert graphlisturl != -1 or gs != -1

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

	colordict = fastrefine(g)
	graphcolors = splitColorDict(colordict, g)[0]

	isomorphisms = []
	undecided = []
	for i in range(len(graphcolors)):  # find isomorphisms
		if len(list(set(graphcolors[i]))) != len(graphcolors[i]):
			undecided.append(i)
		else:
			for j in range(i + 1, len(graphcolors)):
				if graphcolors[i] == graphcolors[j]:
					isomorphisms.append([i, j])

	if not undecided:  # status update
		if isomorphisms:
			print("Isomorphisms found: ", isomorphisms)
		else:
			print("No Isomorphisms found.")
		return colordict
	else:
		print('Isomorphisms found: ', isomorphisms)
		print('There are still undecided graphs left: ', undecided)
		print('Continuing search...')

	# if len(undecided) > 0:  #########################################uncomment this to activate individualization again
	# 	for first in undecided:
	# 		for second in undecided:
	# 			if second > first:
	# 				print("First: ", first, ", Second: ", second)
	# 				num = countIsomorphism(disjointunion(graphlist[first], graphlist[second]))

	return colordict


def countIsomorphism(graph, hasColordict=False):
	print("CountIsomorphism bruh!")
	if hasColordict is False:
		colordict = fastrefine(graph)
	else:
		colordict = fastrefine(graph, hasColordict)
	isomorphism = True
	colors = []
	print("Colordict: ", colordict)
	for c in colordict.keys():
		length = len(colordict[c])
		if length >= 4:  # if there are more than 4 elemts in colordict[c], it means there are duplicates
			colorlength = len(colors)
			if colorlength == 0 or length <= colorlength:
				colors = colordict[c]  # add these to colors.
				isomorphism = False  # meaning we found no isomorphism again
		if length % 2 == 1:  # if there is an uneven number, it means we have no isomorphism (since there are unequal amount of colors in each graph)
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
			newcolor = max(graph.getcolordict().keys()) + 1  # assign a new color
			colordict[c].remove(x)
			colordict[c].remove(y)
			colordict[newcolor] = [x]
			colordict[newcolor].append(y)
			print("Print colordict: ", colordict)
			num += countIsomorphism(graph, colordict)
			colordict.pop(newcolor, None)
			colordict[c].append(x)
			colordict[c].append(y)
			# todo: permenantly change colors of nodes.. Instead of resetting them :(
			# what needs to be done is basically change a nodes color in one graph and one in the other and then use countIsomorphisms on that.
	return num

	return 0


#
#
# def disjoint(graphnumbers=-1):
# if not graphnumbers:
# return None
#
# subgraphlist = []
#
# for graph in graphlist[0]:
# 		subgraphlist.append(len(graph.V()))
# 	print(subgraphlist)
#
# 	graphs = graphlist[0][0]
# 	global numberOfGraphs
#
# 	if graphnumbers == -1:
# 		for y in range(1, len(graphlist[0])):
# 			numberOfGraphs = len(graphlist[0])
# 			graphs = disjointunion(graphs, graphlist[0][y])
# 	else:
# 		numberOfGraphs = len(graphnumbers)
# 		graphs = graphlist[0][graphnumbers.pop(0)]
# 		for y in graphnumbers:
# 			graphs = disjointunion(graphs, graphlist[0][y])
# 	graphs.subgraphs = subgraphlist
# 	return graphs


def splitColorDict(colordict, g):
	subgraphsl = g.subgraphs
	number = 0
	partitions = []
	split = []
	split2 = []
	for i in range(len(subgraphsl)):
		partitions.append(list(range(number, number + subgraphsl[i])))
		number += subgraphsl[i]
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


def preprocessing(g):
	nbs = []
	nbs2 = []
	for vertex in g.V():
		nb = vertex.nbs()[:]
		nb.sort(key=lambda x: x._label)
		nbs.append(tuple(nb))
		nb.append(vertex)
		nb.sort(key=lambda x: x._label)
		nbs2.append(tuple(nb))
	falsetwins = {}
	twins = {}
	for i, item in enumerate(nbs):
		if item in falsetwins.keys():
			falsetwins[item].append(i)
		else:
			falsetwins[item] = [i]
	for i, item in enumerate(nbs2):
		if item in twins.keys():
			twins[item].append(i)
		else:
			twins[item] = [i]
	falsetwins = {k: v for k, v in falsetwins.items() if len(v) > 1}
	twins = {k: v for k, v in twins.items() if len(v) > 1}
	return list(falsetwins.values()), list(twins.values())  # values zijn twins


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


def individualizationRefinement():
	return 0


# print(fastrefine(loadgraph("GI_TestInstancesWeek1/crefBM_4_16.grl", readlist=False)))
compare("GI_TestInstancesWeek1/crefBM_4_9.grl")
# print(compare("GI_TestInstancesWeek1/threepaths10240.gr"))


# test preprocessing
# start_time = time.clock()
# aa = loadgraph("GI_TestInstancesWeek1/hugecographs.grl", readlist=False)
# print(preprocessing(aa))
# elapsed_time = time.clock() - start_time
# print('a: {0:.4f} sec'.format(elapsed_time))