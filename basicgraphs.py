"""
This is a module for working with *undirected* graphs (simple graphs or multigraphs).

It contains three classes: vertex, edge and graph. 

The interface of these classes is extensive and allows programming all kinds of graph algorithms.

However, the data structure used is quite basic and inefficient: a graph object stores only a vertex list and an edge list, and methods such as adjacency testing / finding neighbors of a vertex require going through the entire edge list!
"""
# version: 29-01-2015, Paul Bonsma


unsafe = False
# Set to True for faster, but unsafe listing of all vertices and edges.


class GraphError(Exception):
    def __init__(self, message):
        self.mess = message

    def __str__(self):
        return self.mess


class vertex():
    """
    Vertex objects have an attribute <_graph> pointing to the graph they are part of,
    and an attribute <_label> which can be anything: it is not used for any methods,
    except for __repr__.
 """
    colornum = None
    twin = False
    twinsize = None
    nbl = -1
    incl = -1

    def __init__(self, graph, label=0):
        """
        Creates a vertex, part of <graph>, with optional label <label>.
        (Labels of different vertices may be chosen the same; this does
        not influence correctness of the methods, but will make the string
        representation of the graph ambiguous.)
        """
        self._graph = graph
        self._label = label

    def __repr__(self):
        return str(self._label)

    def adj(self, other):
        """
        Returns True iff vertex <self> is adjacent to <other> vertex.
        """
        return self._graph.adj(self, other)

    def inclist(self):
        """
        Returns the list of edges incident with vertex <self>.
        """
        if not self._graph.enlist:
            self._graph.makeinclist()
        return self._graph.enlist[self]

    def nbs(self):
        """
        Returns the list of neighbors of vertex <self>.
        In case of parallel edges: duplicates are not removed from this list!
        """
        if self.nbl == -1:
            self.nbl = []
            for e in self.inclist():
                self.nbl.append(e.otherend(self))
        return self.nbl


    def fastnbs(self):
        """
        Sneller maar je moet zelf makenbsdict aanroepen als de nbs veranderen
        """
        if self._graph.nbsdict == -1:
            self._graph.makenbsdict()
        return self._graph.nbsdict[self]

    def deg(self):
        """
        Returns the degree of vertex <self>.
        """
        try:
            deg = len(self._graph.nbsdict[self])
        except KeyError:
            deg = 0
        return deg


class edge():
    """
    Edges have attributes <_tail> and <_head> which point to the end vertices
    (vertex objects). The order of these is arbitrary (undirected edges).
    """

    def __init__(self, tail, head):
        """
        Creates an edge between vertices <tail> and <head>.
        """
        # tail and head must be vertex objects.
        if not tail._graph == head._graph:
            raise GraphError(
                'Can only add edges between vertices of the same graph')
        self._tail = tail
        self._head = head

    def __repr__(self):
        return '(' + str(self._tail) + ',' + str(self._head) + ')'

    def tail(self):
        return self._tail

    def head(self):
        return self._head

    def otherend(self, oneend):
        """
        Given one end vertex <oneend> of the edge <self>, this returns
        the other end vertex of <self>.
        """
        # <oneend> must be either the head or the tail of this edge.
        if self._tail == oneend:
            return self._head
        elif self._head == oneend:
            return self._tail
        raise GraphError(
            'edge.otherend(oneend): oneend must be head or tail of edge')

    def incident(self, vertex):
        """
        Returns True iff the edge <self> is incident with the
        vertex <vertex>.
        """
        if self._tail == vertex or self._head == vertex:
            return True
        else:
            return False


class graph():
    """
    A graph object has as main attributes:
     <_V>: the list of its vertices
     <_E>: the list of its edges
    In addition:
     <_simple> is True iff the graph must stay simple (used when trying to add edges)
     <_directed> is False for now (feel free to write a directed variant of this
         module)
     <_nextlabel> is used to assign default labels to vertices.
    """

    def __init__(self, n=0, simple=False):
        """
        Creates a graph.
        Optional argument <n>: number of vertices.
        Optional argument <simple>: indicates whether the graph should stay simple.
        """
        self._V = []
        self._E = []
        self._directed = False
        # may be changed later for a more general version that can also
        # handle directed graphs.
        self.subgraphs = -1
        self._simple = simple
        self._nextlabel = 0
        for i in range(n):
            self.addvertex()
        self.enlist = []
        self.nbsdict = -1
        self.colordict = -1
        self.vertexreprmap = dict()
        for v in self._V:
            self.vertexreprmap[v.__repr__()] = v

    def getvertexbyrepr(self, repr):
        return self.vertexreprmap[repr]

    def __repr__(self):
        return 'V=' + str(self._V) + '\nE=' + str(self._E)

    def generatecolordict(self):
        colordict0 = dict()
        for v in self.V():
            if v.colornum not in colordict0:
                colordict0[v.colornum] = [v]
            else:
                colordict0[v.colornum].append(v)
        self.colordict = colordict0

    def getcolordict(self):
        self.generatecolordict()
        return self.colordict

    def makeinclist(self):
        edges = self.E()
        r = {}  # key is a node, values are the connected edges
        for edge in edges:
            head = edge.head()
            tail = edge.tail()
            for e in [head, tail]:
                if e in r:
                    r[e].append(edge)
                else:
                    r[e] = [edge]
        self.enlist = r

    def makenbsdict(self):
        nbsdict = {}  # key is a node, values are the adjacent nodes
        for edge in self.E():
            tail = edge.tail()
            head = edge.head()
            if tail in nbsdict.keys():
                nbsdict[tail].append(head)
            else:
                nbsdict[tail] = [head]
            if head in nbsdict.keys():
                nbsdict[head].append(tail)
            else:
                nbsdict[head] = [tail]
        self.nbsdict = nbsdict

    def V(self):
        """
        Returns the list of vertices of the graph.
        """
        if unsafe:  # but fast
            return self._V
        else:
            return self._V[:]  # return a *copy* of this list

    def E(self):
        """
        Returns the list of edges of the graph.
        """
        if unsafe:  # but fast
            return self._E
        else:
            return self._E[:]  # return a *copy* of this list

    def __getitem__(self, i):
        """
        Returns the <i>th vertex of the graph -- as given in the vertex list;
        this is not related to the vertex labels.
        """
        return self._V[i]

    def addvertex(self, label=-1, twin=False, twinsize=None):
        """
        Add a vertex to the graph.
        Optional argument: a vertex label (arbitrary)
        """
        if label == -1:
            label = self._nextlabel
            self._nextlabel += 1
        u = vertex(self, label)
        u.twin = twin
        u.twinsize = twinsize
        self._V.append(u)
        self.enlist = []
        return u

    def addvertexobject(self, vobject):
        self._V.append(vobject)
        self.enlist = []
        return vobject


    def addedge(self, tail, head):
        """
        Add an edge to the graph between <tail> and <head>.
        Includes some checks in case the graph should stay simple.
        """
        if self._simple:
            if tail == head:
                raise GraphError('No loops allowed in simple graphs')
            for e in self._E:
                if (e._tail == tail and e._head == head):
                    raise GraphError(
                        'No multiedges allowed in simple graphs')
                if not self._directed:
                    if (e._tail == head and e._head == tail):
                        raise GraphError(
                            'No multiedges allowed in simple graphs')
        if not (tail._graph == self and head._graph == self):
            raise GraphError(
                'Edges of a graph G must be between vertices of G')
        e = edge(tail, head)
        self._E.append(e)
        self.enlist = []
        return e

    def findedge(self, u, v):
        """
        If <u> and <v> are adjacent, this returns an edge between them.
        (Arbitrary in the case of multigraphs.)
        Otherwise this returns <None>.
        """
        for e in self._E:
            if (e._tail == u and e._head == v) or (e._tail == v and e._head == u):
                return e
        return None


    def adj(self, u, v):
        """
        Returns True iff vertices <u> and <v> are adjacent.
        """
        if self.findedge(u, v) == None:
            return False
        else:
            return True

    def isdirected(self):
        """
        Returns False, because for now these graphs are always undirected.
        """
        return self._directed


