# DW 2 practicum, Ex1 solution
from builtins import print

from basicgraphs import graph


def path(n):
    P = graph(n)
    for i in range(n - 1):
        P.addedge(P[i], P[i + 1])
    return P


def cycle(n):
    C = graph(n)
    for i in range(n):
        C.addedge(C[i], C[(i + 1) % n])
    return C


def complete(n):
    K = graph(n)
    for i in range(n - 1):
        for j in range(i + 1, n):
            K.addedge(K[i], K[j])
    return K


def disjointunion(G, H):
    vmap = {}
    K = graph()
    for v in G.V() + H.V():
        vmap[v] = K.addvertex()
    for e in G.E() + H.E():
        K.addedge(vmap[e.tail()], vmap[e.head()])
    return K


if __name__ == "__main__":
    P = path(5)
    C = cycle(5)
    K = complete(4)
    print(P)
    print(C)
    print(K)
    print(disjointunion(disjointunion(P, C), K))
