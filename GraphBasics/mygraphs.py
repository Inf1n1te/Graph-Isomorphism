import basicgraphs


class graph(basicgraphs.graph):
	def deledge(self, edge):
		if edge in self._E:
			index = self._E.index(edge)
			del self._E[index]

	def delvert(self, vertex):
		if vertex._graph == self:
			for edge in vertex.inclist():
				self.deledge(edge)
			index = self._V.index(vertex)
			del self._V[index]
				
