__author__ = 'Tim (& [Jeroen])'

import time

from makegraphs import disjointunion
from graphIO import *


def fastrefine(g, colordict=-1, startcolor=-1, preproc=False):
    if colordict is -1 and not preproc:
        colordict = degcolordict(g)
    elif colordict is -1 and preproc:
        colordict = preproccolordict(g)

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


def preproccolordict(g):
    colordict = {}  # dictionary with key=c and value=vertex array
    for v in g.V():
        if not v.twin:
            v.colornum = v.deg()
        else:
            v.colornum = -v.twinsize
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


def compare(graphlisturl=-1, gs=-1, preproc=False):
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
    # for first in undecided:
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


def gettwins(g):
    nbs = []
    nbs2 = []
    # start_time = time.clock()
    for vertex in g.V():
        nb = vertex.fastnbs()[:]
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
        combined = falsetwinsN + twinsN
        mx = 0
        for i, twin in enumerate(falsetwins):
            g.addvertex(twin[0]._label, True, len(twin))
            mx = max(mx, len(twin))
        for i, twin in enumerate(twins):
            g.addvertex(twin[0]._label, True, mx + len(twin))
        labels = [l._label for l in g.V()]
        for i, twin in enumerate(falsetwins + twins):
            for j in combined[i]:
                if j._label in labels and twin[0] != j and not g.findedge(twin[0],
                                                                          j):  # Geen loop en geen edges dubbel omgedraaid
                    g.addedge(twin[0], j)
        g._V.sort(key=lambda x: x._label)
    return g, lftwins, ltwins


def testpre(graphlisturl):
    start_time = time.clock()
    global graphlist
    graphlist = loadgraph(graphlisturl, readlist=True)
    ngraphs = len(graphlist[0])
    nfalsetwins, ntwins = [None] * ngraphs, [None] * ngraphs
    for i in range(ngraphs):
        graphlist[0][i], nfalsetwins[i], ntwins[i] = preprocessing(graphlist[0][i])
        print(graphlist[0][i])
    print(nfalsetwins, ntwins)
    elapsed_time = time.clock() - start_time
    print('total time: {0:.4f} sec'.format(elapsed_time))
    return compare(gs=graphlist[0], preproc=True)


def individualizationRefinement():
    return 0


# print(fastrefine(loadgraph("GI_TestInstancesWeek1/crefBM_4_16.grl", readlist=False)))
# compare("GI_TestInstancesWeek1/crefBM_4_9.grl")
# print(compare("GI_TestInstancesWeek1/threepaths10240.gr"))


#print(compare("GI_TestInstancesWeek1/hugecographs.grl"))
print(testpre("GI_TestInstancesWeek1/hugecographs.grl"))