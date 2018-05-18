"""
file: base.py

<strike>base class for a endless unit road (think of a piece of puzzle)</strike>
Graph for road networks:
Node/Vertex in the graph represents a road
Edge in the graph represents a linkage relation from one road to another road

author: Xueman Mou
date: 2018/5/9
version: 1.0.0
modified: 2018/5/16 15:00:00 GMT +0800

developing env: python 3.5.2
dependencies: leancloud
"""

import leancloud

def init():
	leancloud.init('Unn6MuUOpPaANqKgT4ogCA2K-gzGzoHsz', '1ubKWLurEO3IAjbzH9erta04')

def insertVertex(number = 2):
	Vertex = leancloud.Object.extend('Vertex')

	for i in range(number):
		vertex = Vertex()
		vertex.set('roadID', '')
		vertex.set('url', '')
		vertex.save()

def insertEdge(startRoadID='', endRoadID='', exitName='', enterName=''):
	# 相邻道路的连接方式：从哪一条道路的哪个出口，到哪一条道路的哪个入口
	Edge = leancloud.Object.extend('Edge')

	edge = Edge()
	edge.set('startRoadID', startRoadID)
	edge.set('endRoadID', endRoadID)
	edge.set('exitName', exitName)
	edge.set('enterName', enterName)
	edge.save()

def main():
	init()
	# insertVertex(3)
	insertEdge()

if __name__ == '__main__':
	main()