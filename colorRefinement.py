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
		b.append(sorted(refine(a[i])))

	for j in range(len(b)):
		d.append(j)
		l = []
		for k in range(len(b)):
			if b[k] == b[j]:
				l.append(k)
				d.append(k)
		if len(l) is not 0:
			r.append(l)
	return removeDuplicates(r)


def removeDuplicates(original):
	new = []
	for element in original:
		if not new.__contains__(element):
			new.append(element)
	return new


print(compare(loadgraph("GI_TestInstancesWeek1/crefBM_6_15.grl", readlist=True)))
\
