"""
file: Classes.py

Define the data structures used by the map system.

author: Xueman Mou
date: 2017/10/24
version: 1.0.0
modified: 2018/1/4 16:37:00 GMT+800

developing env: python 3.6.2

used by	: EMG_parse.py
NOTE	: Must confirm with the .XML data file definition.
NOTE2	: Directed Graph is used here.
NOTE3	: The Graph class only contain connectivity info.
		  Need a simple table to hold Vertex/Edge class mapping
		  to graph.vertices/edges.
"""

class Vertex():
	"""Vertex in Graph"""
	def __init__(self, key=-1, value=None):
		self.key = key
		self.value = value

	def __repr__(self):
		return "{}({})".format(self.key, self.value)

	def __eq__(self, other):
		"""Overrides the default implementation"""
		if isinstance(self, other.__class__):
			return self.__dict__ == other.__dict__
		else:
			return False

	def __ne__(self, other):
		return not self.__eq__(other)

	def getKey(self):
		return self.key

	def setValue(self, value):
		self.value = value

	def getValue(self, value):
		return self.value

class Edge():
	"""Edge in Graph"""
	def __init__(self, key=-1, value=-1, start=None, end=None):
		self.key = key
		self.value = value
		self.start = start
		self.end = end

class Graph():

	"""General Directed Graph"""
	def __init__(self):
		"""create a V-vertex graph with specified number of edges"""
		self.V = 0
		self.E = 0
		self.vertices = []	# store vertex's keys only
		self.adj = {}

	def __repr__(self):
		s = "{} vertices, {} Edges\n".format(self.V, self.E)
		for key in self.adj:
			s += "{}: ".format(key)
			for neighbor in self.adj[key]:
				s += "{} ".format(neighbor)
			s += "\n"
		return s

	def containsVertex(self, vertexKey):
		return vertexKey in self.vertices

	def readFromFile(self, filepath):
		"""fisrt two lines are number of V and E, succeeding line as one edge"""
		with open(filepath) as f:
			V = int(f.readline())
			E = int(f.readline())
			for line in f:
				print(line)
				startKey, endKey = line.split(" ")[:2].trim()
				print(startKey, endKey)
				if not self.containsVertex(startKey):
					self.addVertex(startKey)
				if not self.containsVertex(endKey):
					self.addVertex(endKey)
				self.addEdge(startKey, endKey)

	def saveToFile(self, filepath):
		pass

	def addVertex(self, vertexKey):
		if not self.containsVertex(vertexKey):
			self.vertices.append(vertexKey)
			self.V += 1
		else:
			raise ValueError("Duplicate vertex key. Already exists in graph.")
		pass

	def addEdge(self, startKey, endKey):
		if startKey in self.vertices and endKey in self.vertices:
			# First time adding associate edges
			if startKey not in self.adj:
				self.adj[startKey] = []
			if endKey not in self.adj:
				self.adj[endKey] = []

			# NOTE: not examine parallel edges with same ends
			self.adj[startKey].append(endKey)
			# This is a Directed Graph, thus comment out the next line
			# self.adj[endKey].append(startKey)

			# IF NEEDS to STORE self.edges! can be inferred from vertices and adj!
			# Update graph's edges - as of 1/4/2018, each edge is 
			# only identified by its start-end pair, meaning 
			# if parallel edges cannot be distinguish!

			# Update number of edges
			self.E = self.E + 1
		else:
			raise ValueError("Start/End vertex does not exist in graph.")

	def removeEdge(self, startKey, endKey):
		if not self.containsVertex(startKey) or not self.containsVertex(endKey):
			raise ValueError("Trying to delete an edge with vertex not in the graph!")
		else:
			for v in self.vertices:
				if v == startKey:
					if endKey in self.adj[v]:
						self.adj[v].remove(endKey)	# remove the first occurence of endKey. OK for non parallel edges!

	def removeVertex(self, vertexKey):
		"""remove a vertex"""
		if not self.containsVertex(vertexKey):
			raise ValueError("Trying to remove a vertex not in the graph.")
		else:
			# delete v that appears in other adj list
			for v in self.vertices:
				if vertexKey in self.adj[v] and v != vertexKey:
					self.adj[v].remove(vertexKey)	# assume only one occurence in list

			# delete self.adj[v] key-value pair first - https://stackoverflow.com/questions/11277432/how-to-remove-a-key-from-a-python-dictionary
			self.adj.pop(vertexKey, None)
			self.adj.update()

	def outDegree(self, vertexKey):
		"""compute the out degree of v in Directed Graph"""
		if vertexKey in self.vertices:
			return len(self.adj[vertexKey])
		else:
			return -1

	def inDegree(self, vertexKey):
		"""compute the in degree of v in Directed Graph"""
		inDeg = 0
		for v in self.vertices:
			if vertexKey in self.adj[v]:
				inDeg += 1
		return inDeg

	def numberOfSelfLoops(self):
		"""count self-loops"""
		pass

class LaneNode(object):
	"""docstring for LaneNode"""
	def __init__(self, arg):
		super(LaneNode, self).__init__()
		self.arg = arg
		
class LaneEdge(object):
	"""docstring for LaneEdge"""
	def __init__(self, arg):
		super(LaneEdge, self).__init__()
		self.arg = arg
		
class LaneGraph(object):
	"""LaneGraph is used during navigation in traffic system"""
	def __init__(self, arg):
		super(LaneGraph, self).__init__()
		self.arg = arg
		
class unitTest(object):
	"""unit test cases for above classes"""
	
	# test vertex class equality
	def vertex(self):
		v1 = Vertex(1,2)
		v2 = Vertex(1,2)
		v3 = Vertex(2,0)

		print("{},{},{}\n{}=={}: {}\n{}=={}: {}\n{}!={}: {}\n".format(
			v1, v2, v3,
			v1, v2, v1==v2,
			v2, v3, v2==v3,
			v2, v3, v2!=v3,
		))

	# test Graph class
	def graph(self):
		g = Graph()
		for i in range(4):
			g.addVertex(i + 1)

		g.addEdge(1,2)
		g.addEdge(2,1)
		g.addEdge(2,3)
		g.addEdge(3,4)
		g.addEdge(2,4)

		print(g)

		print("inDegree of vertex 2:{}, outDegree of vertex 2: {}".format(
				g.inDegree(2), g.outDegree(2)
			))

		# if adj uses a python built-in dict, successive remove VertexKey raises a key error
		# Meaning: the index of the dict does not update
		g.removeVertex(3)
		g.removeVertex(2)

		print(g)

def main():
	
	unit = unitTest()
	unit.graph()
	# unit.vertex()

if __name__ == '__main__':
	main()