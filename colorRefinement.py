__author__ = 'Tim (& [Jeroen])'

import time

from makegraphs import disjointunion
from graphIO import *


def fastrefine(g, startcolor=-1, colordict=-1):
	start_time = time.clock()
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
                nextcolor = max(colordict.keys()) + 1
		i += 1
    print('end')
    print(colordict)
	elapsed_time = time.clock() - start_time
	print('Time: {0:.4f} sec'.format(elapsed_time))
	try:
        return compareColors(splitColorDict(colordict, g)[0])
	except:
		print('its only one graph apparently')
	return colordict


# def refine(g):
# # initialize
# colordict = degcolordict(g)
#
#
# done = False
# start_time = time.clock()
# counter = 0
# while not done:
#     done = True
#     counter += 1
#     if counter % 100 == 0:
#         print(counter)
#     tempcolordict = dict()
#
#     for key in colordict.keys():
#         nextcolor = max(colordict.keys()) + 1
#         buren = tuple()
#         for value in colordict[key]:
#             nc = sorted(tuple(getNeighbourColors(value)))
#             if len(buren) == 0:
#                 buren = nc
#
#             if buren != nc:
#                 done = False
#                 if nextcolor in tempcolordict:
#                     tempcolordict[nextcolor].append(value)
#                 else:
#                     tempcolordict[nextcolor] = [value]
#
#             else:
#                 if key in tempcolordict:
#                     tempcolordict[key].append(value)
#                 else:
#                     tempcolordict[key] = [value]
#
#     colordict = tempcolordict.copy()
#
#     for key in colordict.keys():
#         for value in colordict[key]:
#             value.colornum = key
#
# finalcolors = []
# for node in g.V():
#     finalcolors.append(node.colornum)
#
# elapsed_time = time.clock() - start_time
# print('Time: {0:.4f} sec'.format(elapsed_time))
# # DUS HIER SHIT DOEN MET COLORDICT EN DUBBELE KLEUREN ENZO
# try:
#     result = compareColors(splitColorDict(colordict, g)[0])
#     if len(undecidedGraphs) > 0:
#         print(undecidedGraphs)
#         findDuplicates(splitColorDict(colordict, g)[1])
#     return result
# except:
#     print('its only one graph apparently')
#     return colordict


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


def compare(graphlisturl):
    global graphlist
    graphlist = loadgraph(graphlisturl, readlist=True)
    return fastrefine(disjoint())


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


def gettwins(g):
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
    combined = falsetwinsN + twinsN
    print(combined)
    for i, twin in enumerate(falsetwins + twins):
        g.addvertex(twin[0]._label)
    labels = [l._label for l in g.V()]
    for i, twin in enumerate(falsetwins + twins):
        for j in combined[i]:
            if j._label in labels and twin[0] != j:
                g.addedge(twin[0], j)
    return g


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


def testpre(graphlisturl):
    start_time = time.clock()
    global graphlist
    graphlist = loadgraph(graphlisturl, readlist=True)
    print(preprocessing(disjoint()))
    elapsed_time = time.clock() - start_time
    print('a: {0:.4f} sec'.format(elapsed_time))

# print(fastrefine(loadgraph("GI_TestInstancesWeek1/crefBM_4_16.grl", readlist=False)))
# print(compare("GI_TestInstancesWeek1/crefBM_4_16.grl"))
# print(compare("GI_TestInstancesWeek1/threepaths10240.gr"))

print(testpre("GI_TestInstancesWeek1/crefBM_4_7copy.grl"))
