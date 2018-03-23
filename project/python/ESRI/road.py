'''
file: road.py

get hierachically roads/lanes specified in ESRI folder.

author: Xueman Mou
date: 2018/3/22
version: 1.0.0
modified: 2018/3/22 09:45:00 GMT+800

developing env: python 3.5.2
dependencies: pyshp, pyproj
'''

import os
import sys
import shapefile
import pyproj

class Road(object):
	def __init__(self, ID, MeshID, Owner, SHNodeID, EHNodeID, HRLength, HRType, direction, LaneNumSE, LaneNumES, InnerCJ, LCJID, LEDGEID):
		self.roadID = ID
		self.meshID = MeshID
		self.owner = Owner
		self.startRoadNodeID = SHNodeID
		self.endRoadNodeID = EHNodeID
		self.length = HRLength
		self.type = HRType
		self.direction = direction
		self.laneNumSE = LaneNumSE
		self.laneNumES = LaneNumES # valid when direction = 1 (bi-direcional)
		self.innerCJ = InnerCJ
		self.junctionID = LCJID	# valid when innerCJ = 2
		self.LEDGEID = LEDGEID # ? what it means

	def __repr__(self):
		return '''roadID\t\t{}\nmeshID\t\t{}\nowner\t\t{}\nstartRoadNode\t{}\nendRoadNode\t{}\nlength\t\t{}\ntype\t\t{}\ndirection\t{}\nlaneNumSE\t{}\nlaneNumES\t{}\ninnerCJ\t\t{}\njunctionID\t{}\nLEDGEID\t\t{}\n'''.format(
				self.roadID,
				self.meshID,
				self.owner,
				self.startRoadNodeID,
				self.endRoadNodeID,
				self.length,
				self.type,
				self.direction,
				self.laneNumSE,
				self.laneNumES,
				self.innerCJ,
				self.junctionID,
				self.LEDGEID
			)

class RoadNode(object):
	def __init__(self, HNodeID, MeshID, Owner, LHNodeID, LMeshID, LHRoadID, LJCID, CJHNFlag, LCJID, SSFlag, SSType, MergeFlag, SplitFlag):
		self.roadNodeID = HNodeID
		self.meshID = MeshID
		self.Owner = Owner
		self.LHNodeID = LHNodeID
		self.LMeshID = LMeshID
		self.LHRoadID = LHRoadID # 关联道路基准线编号序列 i.e., 该点出现在以下道路中:xxx－xxx－xxx
		self.LJCID = LJCID # 关联基础数据连接点编号 当道路基准线连接点有对应的传统二维基础数据道路连接点时，该字段有效
		self.isInJunction = CJHNFlag # 路口内道路基准线连接点标识 1否 2是
		self.junctionID = LCJID # valid if CJHNFlag == 2 
		self.SSFlag = SSFlag # 特殊结构出入口 1否 2是
		self.SSType = SSType # valid if SSFlag == 2
		self.mergeFlag = MergeFlag # 合流点标识 1否 2是
		self.splitFlag = SplitFlag # 分流点标识 1否 2是

class roadNetwork(object):
	def __init__(self):
		self.vertices = []
		self.adjList = {}

	def __repr__(self):
		graph = ''
		for nodeID in self.adjList:
			for nextID in self.adjList[nodeID]:
				graph += '%d - %d\n' % (nodeID, nextID)

		return graph

	def addRoad(self, road):
		
		startNode = road.startRoadNodeID
		endNode = road.endRoadNodeID

		if startNode not in self.vertices:
			self.vertices.append(startNode)
		if endNode not in self.vertices:
			self.vertices.append(endNode)

		if road.direction == 3: 
			# traffic flow is not of the same direction as vector startNode -> endNode
			tmp = startNode
			startNode = endNode
			endNode = tmp

		if not startNode in self.adjList:
			self.adjList[startNode] = [endNode]
		else:
			self.adjList[startNode].append(endNode)

		if road.direction == 1:
			if not endNode in self.adjList:
				self.adjList[endNode] = [startNode]
			else:
				self.adjList[endNode].append(startNode)

def readRoads(filepath):
	
	roads = []
	sf = shapefile.Reader(filepath)

	for index, sr in enumerate(sf.shapeRecords()):
		shape = sr.shape
		record = sr.record

		ID, MeshID, Owner, SHNodeID, EHNodeID, HRLength, HRType, direction, LaneNumSE, LaneNumES, InnerCJ, LCJID, LEDGEID = record
		road = Road(ID, MeshID, Owner, SHNodeID, EHNodeID, HRLength, HRType, direction, LaneNumSE, LaneNumES, InnerCJ, LCJID, LEDGEID)
		roads.append(road)

	return roads

def readRoadNodes(filepath):
	
	roadNodes = []
	sf = shapefile.Reader(filepath)
	
	for index, sr in enumerate(sf.shapeRecords()):
		shape = sr.shape
		record = sr.record

		HNodeID, MeshID, Owner, LHNodeID, LMeshID, LHRoadID, LJCID, CJHNFlag, LCJID, SSFlag, SSType, MergeFlag, SplitFlag = record
		roadNode = RoadNode(HNodeID, MeshID, Owner, LHNodeID, LMeshID, LHRoadID, LJCID, CJHNFlag, LCJID, SSFlag, SSType, MergeFlag, SplitFlag)
		roadNodes.append(roadNode)

	return roadNodes

def buildRoadNetwork(roads, filepath):
	network = roadNetwork()
	for road in roads:
		network.addRoad(road)
	print(network)

def main():
	
	pathname = '/Users/mxmcecilia/Documents/WebGL小组/modeling/GIS_PCG/data/EMG_sample_data/EMG_GZ'

	roads = readRoads(os.path.join(pathname, 'HRoad.shp'))
	buildRoadNetwork(roads, os.path.join(pathname, 'HRoadNode.shp'))

	readRoadNodes(os.path.join(pathname, 'HRoadNode.shp'))

if __name__ == "__main__":
	main()