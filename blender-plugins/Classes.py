"""
file: Classes.py

Define the data structures used by the map system.

author: Xueman Mou
date: 2017/10/24
version: 1.0.0
modified: 2017/10/24 17:18:00 GMT+800

developing env: python 3.6.2

used by	: EMG_parse.py
NOTE	: Must confirm with the .XML data file definition.
"""

class Node():
	"""Node in Graph"""
	def __init__(self, index=-1, value=None):
		self.index = index
		self.value = value

	def getIndex(self):
		pass

	def setValue(self, value):
		pass

	def getValue(self, value):
		pass

class Edge():
	"""Edge in Graph"""
	def __init__(self, index=-1, start=None, end=None):
		self.index = index
		self.start = start
		self.end = end

class Graph():
	"""General Directed Graph"""
	def __init__(self):
		"""create a V-vertex graph with no edges"""
		self.nodes = []
		self.edges = []
		self.adj = {}

	def __repr__(self):
		pass

	def readFromFile(self, filepath):
		pass

	def saveToFile(self, filepath):
		pass

	def addNode(self, node):
		pass

	def addEdge(self, start, end):
		pass

	def removeEdge(self, edgeIndex):
		pass

	def removeNode(self, nodeIndex):
		pass

	def degree(self, nodeIndex):
		"""compute the degree of v"""
		pass

	def maxDegree(self):
		"""compute maximum degree"""
		pass

	def avgDegree(self):
		"""compute average degree """
		pass

	def numberOfSelfLoops(self):
		"""count self-loops"""
		pass

	def toString(self):
		"""string representation of the graph’s adjacency lists (instance method in Graph)"""
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
		
def main():
	pass

if __name__ == '__main__':
	main()