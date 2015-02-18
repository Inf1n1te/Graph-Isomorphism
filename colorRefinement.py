__author__ = 'Tim'

from graphIO import *

def refine(g):
	colordict = { }
	for v in g.V():
		v.a = v.deg()
		if not colordict.__contains__(v.a):
			colordict[v.a] = [v]
		else:
			colordict[v.a].append(v)
	print(colordict.keys())
	changed = True
	newcolor = max(colordict.keys()) + 1
	while changed:
		tempcolordict = colordict
		for key in colordict.keys():
			buren = []
			for value in colordict.get(key):
				nc = getNeighbourColors(value)
				if nc not in buren and len(buren) != 0:
					buren.append(nc)
					value.a = newcolor
					newcolor += 1
				elif len(buren) == 0:
					buren.append(nc)
		if tempcolordict == colordict:
			changed = False
	finalcolors = []
	for node in g.V():
		finalcolors.append(node.a)
	print(finalcolors)
	return finalcolors

def getNeighbourColors(v):
	colors = []
	for i in v.nbs():
		colors.append(i.a)
		colors.sort()
	return colors


refine(loadgraph("GI_TestInstancesWeek1/crefBM_4_16.grl", readlist=False))