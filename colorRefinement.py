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
	changed = True
	colorrangeinc = len(g.V())
	colorvalue = 0
	while changed:
		tempcolordict = colordict
		for key in colordict.keys():
			buren = []
			colorvalue += colorrangeinc
			colorinc2 = 1
			for value in colordict.get(key):
				nc = getNeighbourColors(value)
				if nc not in buren and len(buren) != 0:
					buren.append(nc)
					value.a = colorvalue + colorinc2
					colorinc2 += 1
				elif len(buren) == 0:
					buren.append(nc)
		if tempcolordict == colordict:
			changed = False
	for node in g.V():
		print(node.a, colorvalue)
	return None

def getNeighbourColors(v):
	colors = []
	for i in v.nbs():
		colors.append(i.a)
		colors.sort()
	return colors

refine(loadgraph("GI_TestInstancesWeek1/crefBM_4_7.grl", readlist=False))