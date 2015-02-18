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
	print(colordict)
	print(colordict.values())
	changed = True
	while changed:
		for key in colordict.keys():
			buren = []
			andereburen = []
			for value in colordict.get(key):
				nc = getNeighbourColors(value)

	return None


def getNeighbourColors(v):
	colors = []
	for i in v.nbs():
		colors.append(i.a)
		colors.sort()
	return colors


refine(loadgraph("GI_TestInstancesWeek1/crefBM_4_7.grl", readlist=False))