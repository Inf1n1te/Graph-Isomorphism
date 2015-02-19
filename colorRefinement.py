__author__ = 'Tim'

from graphIO import *
from GraphBasics.makegraphs import disjointunion


def refine(g):
	colordict = { }
	for v in g.V():
		v.colorNum = v.deg()
		if v.colorNum not in colordict:
			colordict[v.colorNum] = [v]
		else:
			colordict[v.colorNum].append(v)
	print(colordict)
	changed = True
	newcolor = max(colordict.keys()) + 1
	while changed:
		tempcolordict = colordict.copy()
		for key in tempcolordict.keys():
			buren = { }
			for value in tempcolordict.get(key):
				nc = tuple(getNeighbourColors(value))
				if len(buren) == 0:
					buren[nc] = value.colorNum
				elif nc not in buren:
					colordict[key].remove(value)
					# value.colorNum = newcolor
					buren[nc] = newcolor
					colordict[newcolor] = [value]
					newcolor += 1
				else:
					colordict[value.colorNum].remove(value)
					# value.colorNum = buren[nc]
					colordict[buren[nc]].append(value)
			print(colordict, '\n')
		for key in colordict:
			for value in colordict[key]:
				value.colorNum = key
		if tempcolordict == colordict:
			changed = False
			print(colordict)
	finalcolors = []
	for node in g.V():
		finalcolors.append(node.colorNum)

	return finalcolors


def getNeighbourColors(v):
	colors = []
	for i in v.nbs():
		colors.append(i.colorNum)
		colors.sort()
	return colors


def compare(x):
	graphs = x[0][0]
	for y in range(1, len(x[0])):
		graphs = disjointunion(graphs, x[0][y])
	print(sorted(refine(graphs)))


# for i in x[0]:
# for j in x[0][i].V():



# a = x[0]
# b = []
# d = []
# r = []
# for i in range(len(a)):
# b.append(sorted(refine(a[i])))
# for j in range(len(b)):
# d.append(j)
# l = []
# 	for k in range(len(b)):
# 		if b[k] == b[j]:
# 			l.append(k)
# 			d.append(k)
# 	if len(l) is not 0:
# 		r.append(l)
# return removeDuplicates(r)


def removeDuplicates(original):
	new = []
	for element in original:
		if not new.__contains__(element):
			new.append(element)
	return new


print(compare(loadgraph("GI_TestInstancesWeek1/crefBM_4_9.grl", readlist=True)))