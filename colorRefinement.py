__author__ = 'Tim (& [Jeroen])'

import time
import copy

from makegraphs import disjointunion
from graphIO import *


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


def refine(g):
	# initialize
	colordict = degcolordict(g)

	done = False
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

	# DUS HIER SHIT DOEN MET COLORDICT EN DUBBELE KLEUREN ENZO
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

	if preproc:
		colordict = fastrefine(g, preproc=True)
	else:
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
					isomorphisms.append([i, j, 1])

	print(undecided)
	if not undecided:  # status update
		if isomorphisms:
			print("Isomorphisms found: ", isomorphisms)
		else:
			print("No Isomorphisms found.")
		return colordict
	else:
		print('Isomorphisms found: ', isomorphisms)
		print('There are still undecided graphs left, continuing search..')

	if len(undecided) > 0:
		for first in undecided:
			for second in undecided:
				if second > first:
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
	# print("CountIsomorphism bruh!")
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

	return 0


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
	# elapsed_time = time.clock() - start_time
	# print('gettwins: {0:.4f} sec'.format(elapsed_time))
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
				if j in g.V() and twin[0] != j and not g.findedge(twin[0],
																  j):  # Geen loop en geen edges dubbel omgedraaid
					g.addedge(twin[0], j)
		g._V.sort(key=lambda x: x._label)
	return g, lftwins, ltwins


def testpre(graphlisturl, GI_only=False):
	global graphlist
	graphlist = loadgraph(graphlisturl, readlist=True)
	ngraphs = len(graphlist[0])
	for i in range(ngraphs):
		writeDOT(graphlist[0][i], 'before' + str(i) + '.dot')
	nfalsetwins, ntwins = [None] * ngraphs, [None] * ngraphs
	for i in range(ngraphs):
		graphlist[0][i], nfalsetwins[i], ntwins[i] = preprocessing(graphlist[0][i])
	# print(graphlist[0][i])
	# isgraph(graphlist[0][i])
	print('number of twins:', nfalsetwins, ntwins)
	for i in range(ngraphs):
		writeDOT(graphlist[0][i], 'after' + str(i) + '.dot')
	return compare(gs=graphlist[0], preproc=True, GI_only=False)


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


start_time = time.clock()

compare("GI_TestInstancesWeek1/crefBM_6_15.grl", False)

# testpre("GI_TestInstancesWeek1/cographs1.grl")

elapsed_time = time.clock() - start_time
print('Time: {0:.4f} sec'.format(elapsed_time))

