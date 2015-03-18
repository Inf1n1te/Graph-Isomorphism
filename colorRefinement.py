__author__ = 'Tim (& [Jeroen])'
# herman
from makegraphs import disjointunion
from graphIO import *
import time

numberOfGraphs = 0
graphlist = []


def fastrefine(g):
    colordict = degcolordict(g)
    print(colordict)
    queue = [min(colordict.keys())]
    nextcolor = max(colordict.keys()) + 1
    i = 0
    while i < len(queue):
        connectednodes = dict()
        print("queue:     ", queue[i])
        print("colordict keys:     ", colordict.keys())
        if queue[i] not in colordict.keys():
            i += 1
            break
        for node in colordict[queue[i]]:
            for nb in node.nbs():
                color = nb.c
                if color in connectednodes and nb not in connectednodes[color]:
                    connectednodes[color].append(nb)
                else:
                    connectednodes[color] = [nb]
        for key in connectednodes.keys():
            connectednodes[key].sort(key=lambda x: x.__repr__())
            if not colordict[key] == connectednodes[key]: #then add the shortest to the queue..
                print(key, ' >> ', queue)
                if key not in queue: # and len(connectednodes[key]) > len(colordict[key])
                    print('key appended')
                    queue.append(key)
                else:
                    print('nextcolor appended')
                    queue.append(nextcolor)
                for vertex in connectednodes[key]:
                    vertex.c = nextcolor
                colordict = g.generatecolordict()
                nextcolor = max(colordict.keys()) + 1
        i += 1
    try:
        return compareColors(splitColorDict(colordict, g))
    except:
        print('its only one graph appearantly')
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
                value.c = key

    finalcolors = []
    for node in g.V():
        finalcolors.append(node.c)

    elapsed_time = time.clock() - start_time
    print('Time: {0:.4f} sec'.format(elapsed_time))
    # DUS HIER SHIT DOEN MET COLORDICT EN DUBBELE KLEUREN ENZO
    try:
        return compareColors(splitColorDict(colordict, g))
    except:
        print('its only one graph appearantly')
    return colordict


def degcolordict(g):
    colordict = {}  # dictionary with key=c and value=vertex array
    for v in g.V():
        v.c = v.deg()
        if v.c not in colordict:
            colordict[v.c] = [v]
        else:
            colordict[v.c].append(v)
    return colordict


def getNeighbourColors(v):
    colors = []
    for i in v.nbs():
        colors.append(i.c)
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
    for j in range(numberOfGraphs):
        split.append([])
    for key in colordict:
        for value in colordict.get(key):
            for e in partitions:
                if int(value.__repr__()) in e:
                    split[partitions.index(e)].append(value.c)
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

#print(fastrefine(loadgraph("GI_TestInstancesWeek1/crefBM_4_16.grl", readlist=False)))
print(compare("GI_TestInstancesWeek1/crefBM_4_16.grl"))