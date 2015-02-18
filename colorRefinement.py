__author__ = 'Tim'

from graphIO import *


def refine(g):
	colordict = {}
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


def compare(x):
	a = x[0]
	b = []
	d = []
	r = []
	for i in range(len(a)):
		b.append(refine(a[i]).sort())

	for j in range(len(b)):
		if j not in d:
			d.append(j)
			l = []
			for k in range(len(b)):
				if k not in d and b[k] == b[j]:
					l.append(b(k))
					d.append(b(k))
			if len(l) is not 0:
				r.append(l)
	return r


compare(loadgraph("GI_TestInstancesWeek1/crefBM_4_16.grl", readlist=True))
# refine(loadgraph("GI_TestInstancesWeek1/crefBM_4_16.grl", readlist=False))