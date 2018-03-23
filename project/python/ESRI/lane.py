'''
file: lane.py

get hierachically roads/lanes specified in ESRI folder.

author: Xueman Mou
date: 2018/3/23
version: 1.0.0
modified: 2018/3/23 08:23:00 GMT+800

developing env: python 3.5.2
dependencies: pyshp, pyproj, mathutils, sqlite3
'''

import os
import sys
import shapefile
import pyproj
# from mathutils import Vector
import sqlite3

DB = '/Users/mxmcecilia/Documents/WebGL小组/modeling/GIS_PCG/project/python/ESRI/EMG.db'

class Lane(object):
	def __init__(self, ID, SeqNum, MeshID, Owner, SHLNode, EHLNode, LSpeed, LHRoadID, VLaneFlag, ETCFlag, SDFlag, EGFlag, RampFlag, MELType, NLaneSFlag):
		self.laneID = ID
		self.seqNum = SeqNum
		self.MeshID = MeshID
		self.Owner = Owner
		self.SHLNode = SHLNode
		self.EHLNode = EHLNode
		self.maxSpeed = LSpeed
		self.inRoadID = LHRoadID
		self.VLaneFlag = VLaneFlag
		self.ETCFlag = ETCFlag
		self.SDFlag = SDFlag
		self.RampFlag = RampFlag
		self.MELType = MELType
		self.NLaneSFlag = NLaneSFlag
		self.laneNodes = []

class LaneNode(object):
	def __init__(self, HLaneID, L, B, H, Width):
		self.laneID = HLaneID
		self.lon = L
		self.lat = B
		self.alt = H
		self.width = width

def readLanes(pathname):

	sfHLane = shapefile.Reader(os.path.join(pathname, 'HLane.shp'))
	conn = sqlite3.connect(DB)
	c = conn.cursor()

	for index, sr in enumerate(sfHLane.shapeRecords()):
		shape = sr.shape
		record = sr.record

		# new lane		
		ID, SeqNum, MeshID, Owner, SHLNode, EHLNode, LSpeed, LHRoadID, VLaneFlag, ETCFlag, SDFlag, EGFlag, RampFlag, MELType, NLaneSFlag = record
		lane = Lane(ID, SeqNum, MeshID, Owner, SHLNode, EHLNode, LSpeed, LHRoadID, VLaneFlag, ETCFlag, SDFlag, EGFlag, RampFlag, MELType, NLaneSFlag)

		# start node
		c.execute('''SELECT HLWidth FROM HLaneNode WHERE HLNodeID = ?''', (lane.SHLNode,))
		width = c.fetchone()[0]
		laneNode = LaneNode(0,)

def main():
	pathname = '/Users/mxmcecilia/Documents/WebGL小组/modeling/GIS_PCG/data/EMG_sample_data/EMG_GZ'

	lanes = readLanes(pathname)


if __name__ == '__main__':
	main()