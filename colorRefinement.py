__author__ = 'Tim'

from graphIO import *
from makegraphs import disjointunion


def refine(g):
	# initialize
	colordict = {}  # dictionary with key=colornum and value=vertex array
	for v in g.V():
		v.colornum = v.deg()
		if v.colornum not in colordict:
			colordict[v.colornum] = [v]
		else:
			colordict[v.colornum].append(v)
	print(colordict)

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
			print('step', colordict)
			newcolor = max(colordict.keys()) + 1
		if len(tempcolordict) == 0:
			changed = False
			print(colordict)
		for value in tempcolordict:
			old = tempcolordict[value][0]
			new = tempcolordict[value][1]
			colordict[old].remove(value)
			value.colornum = new
			if new in colordict:
				colordict[new].append(value)
			else:
				colordict[new] = [value]
	finalcolors = []
	for node in g.V():
		finalcolors.append(node.colornum)

	return finalcolors


def getNeighbourColors(v):
	colors = []
	for i in v.nbs():
		colors.append(i.colornum)
	return colors
#herman

def compare(x):
	graphs = x[0][0]
	for y in range(1, len(x[0])):
		graphs = disjointunion(graphs, x[0][y])
	print(sorted(refine(graphs)))


def removeDuplicates(original):
	new = []
	for element in original:
		if not new.__contains__(element):
			new.append(element)
	return new


compare(loadgraph("GI_TestInstancesWeek1/crefBM_4_9.grl", readlist=True))