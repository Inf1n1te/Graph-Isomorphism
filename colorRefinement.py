__author__ = 'Tim (& [Jeroen])'

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


print(compare("GI_TestInstancesWeek1/crefBM_4_7.grl"))
# Alleen False Twins werkt nog
def preprocessing(g):  #Maakt modules van (False) Twins (improvement 2)
	falsetwins = {}
	twins = {}
	for i in range(len(g.V())):
		vertex1 = g.V()[i]
		nbs1 = tuple(vertex1.nbs())
		nbs1app = vertex1.nbs()
		print(nbs1app, i)
		nbs1app.append(vertex1)
		nbs1ext = tuple(nbs1app)
		#print(nbs1ext)
		for vertex2 in g.V()[i + 1:]:
			nbs2 = tuple(vertex2.nbs())
			nbs2app = vertex2.nbs()
			nbs2app.append(vertex2)
			nbs2ext = tuple(nbs2app)
			# print(nbs1ext,nbs2ext)
			if nbs1 == nbs2:  #False twins
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

# print(splitList([1, 2, 3, 4, 5, 6, 7, 8], 3))
print(comparegraphs(loadgraph("GI_TestInstancesWeek1/crefBM_4_7.grl", readlist=True)))


# test preprocessing
#aa = loadgraph("GI_TestInstancesWeek1/crefBM_4_7copy.grl", readlist=False)
#print(aa)
#print(preprocessing(aa))