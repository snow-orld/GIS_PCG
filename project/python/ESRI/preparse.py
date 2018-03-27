"""
file: preparse.py

Parse original ESRI files to data sets acceptable for sqlite insertion.
After calling the create table method in sqlite.py under the same folder.

author: Xueman Mou
date: 2017/11/1
version: 1.0.1
modified: 2018/3/13 09:17:00 GMT+800

developing env: python 3.6.3
dependencies  :	pyshp, pyproj
				sqlite (custom)

input :	path to EMG sample data folder
output: A local database EMG.db storing all info of the shapefile folder
"""

import os
import sys
import shapefile
import sqlite as sql

def parse_file(db, filepath):
	"""
	shape-record pair (shape is like a basic geometry or road, more
	suitably, in OpenDRIVE standard)

	input : db to write to, filepath
	output: None
	"""

	print(filepath)
	#print(os.path.splitext(os.path.basename(filepath))[0])

	sf = shapefile.Reader(filepath)
	fields = sf.fields[1:]	# ('DeletionFlag' is not specified in EMG's spec)

	# Attributes
	# ['AttributeName', 'Type', 'LengthIntegral', 'LengthFractal']
	# NOTE: EMG spec has an additional contraint 'Obl' for value that must be present
	# CHALLENGE: PK is needed when creating new tables, but shp file does not self-contains such info
	# SOLUTION: Manually create all tables in sql. Insert value during parsing.
	for field in fields:
		attribute, datatype, lenA, lenB = field
		# print('\t%s%s\t%s\t%s\t%s' % (attribute, ' '*(8 - len(attribute)), datatype, lenA, lenB))

	LMIDs = []
	HLNodeIDs = []
	LRIDs = []
	# Tuples
	for srindex, sr in enumerate(sf.shapeRecords()):
		# print('#%03d %s' % (srindex, sr.record))

		if filepath.find('HRoad.shp') > -1:
			HRoadID, MeshID, Owner, SHNodeID, EHNodeID, HRLength, HRType, Direction, LaneNumSE, LaneNumES, InnerCJ, LCJID, LEDGEID = sr.record
			db.c.execute('''INSERT INTO HRoad VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)''', (HRoadID, MeshID, Owner, SHNodeID, EHNodeID, HRLength, HRType, Direction, LaneNumSE, LaneNumES, InnerCJ, LCJID, LEDGEID))

		if filepath.find('HRoadNode.shp') > -1:
			HNodeID, MeshID, Owner, LHNodeID, LMeshID, LHRoadID, LJCID, CJHNFlag, LCJID, SSFlag, SSType, MergeFlag, SplitFlag = sr.record
			db.c.execute('''INSERT INTO HRoadNode VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)''', (HNodeID, MeshID, Owner, LHNodeID, LMeshID, LHRoadID, LJCID, CJHNFlag, LCJID, SSFlag, SSType, MergeFlag, SplitFlag))

		if filepath.find('ComplexJunction.shp') > -1:
			CJID, MeshID, Owner, CJType, CJNameC, CJNameP, CJNameE, CJGroupID = sr.record
			db.c.execute('''INSERT INTO ComplexJunction VALUES(?,?,?,?,?,?,?,?)''', (CJID, MeshID, Owner, CJType, CJNameC, CJNameP, CJNameE, CJGroupID))

		if filepath.find('HLane.shp') > -1:
			print(sr.record)
			HLaneID, SeqNum, MeshID, Owner, SHLNodeID, EHLNodeID, LSpeed, LHRoadID, VLaneFlag, ETCFlag, SDFlag, EGFlag, RampFlag, MELType, NLaneSFlag, tmp = sr.record
			db.c.execute('''INSERT INTO HLane VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',(HLaneID, SeqNum, MeshID, Owner, SHLNodeID, EHLNodeID, LSpeed, LHRoadID, VLaneFlag, ETCFlag, SDFlag, EGFlag, RampFlag, MELType, NLaneSFlag))

		if filepath.find('HLaneNode.shp') > -1:
			HLNodeID, MeshID, Owner, LHNodeID, LHLNodeID, L, B, H, HLWidth = sr.record
			if HLNodeID not in HLNodeIDs:
				HLNodeIDs.append(HLNodeID)
				db.c.execute('''INSERT INTO HLaneNode VALUES (?,?,?,?,?,?,?,?,?)''', (HLNodeID, MeshID, Owner, LHNodeID, LHLNodeID, L, B, H, HLWidth))

		if filepath.find('HLRestriction.shp') > -1:
			LRID, SHLaneID, HLNodeID, EHLaneID, RCID = sr.record
			if LRID not in LRIDs:
				LRIDs.append(LRID)
				db.c.execute('''INSERT INTO HLRestriction VALUES (?,?,?,?,?)''', (LRID, SHLaneID, HLNodeID, EHLaneID, RCID))

		if filepath.find('HLRCondition.shp') > -1:
			RCID, LUserType, FVFlag, RTime = sr.record
			db.c.execute('''INSERT INTO HLRCondition VALUES (?,?,?,?)''', (RCID, LUserType, FVFlag, RTime))

		if filepath.find('HLaneInfo.shp') > -1:
			ID, HLaneID, VertexID, L, B, H, Curvature, Heading, Slope, Width = sr.record
			db.c.execute('''INSERT INTO HLaneInfo VALUES (?,?,?,?,?,?,?,?,?,?)''', (ID, HLaneID, VertexID, L, B, H, Curvature, Heading, Slope, Width))

		if filepath.find('HLaneNodeInfo.shp') > -1:
			ID, HLNodeID, InHLaneID, OutHLaneID, NCurvature, NHeading, NSLope = sr.record
			db.c.execute('''INSERT INTO HLaneNodeInfo VALUES (?,?,?,?,?,?,?)''', (ID, HLNodeID, InHLaneID, OutHLaneID, NCurvature, NHeading, NSLope))

		if filepath.find('LMarking.shp') > -1:
			LMID, MeshID, Owner, LMType, LMColor, LMForm, LMWidth, LMLength, LHRoadID, LHLaneID = sr.record
			if LMID not in LMIDs:
				LMIDs.append(LMID)
				db.c.execute('''INSERT INTO LMarking VALUES (?,?,?,?,?,?,?,?,?,?)''', (LMID, MeshID, Owner, LMType, LMColor, LMForm, LMWidth, LMLength, LHRoadID, LHLaneID))

		if filepath.find('AMarking.shp') > -1:
			AMID, MeshID, Owner, AMType, ArrowType, LHRoadID, LHLaneID = sr.record
			db.c.execute('''INSERT INTO AMarking VALUES (?,?,?,?,?,?,?)''', (AMID, MeshID, Owner, AMType, ArrowType, LHRoadID, LHLaneID))

		if filepath.find('RFacilityP.shp') > -1:
			print(sr.record)
			PObjectID, MeshID, Owner, OType, THeight, BHeight, TSShape, ViaSign, TWidth, Diameter, tmp, LHRoadID = sr.record
			db.c.execute('''INSERT INTO RFacilityP VALUES (?,?,?,?,?,?,?,?,?,?,?)''', (PObjectID, MeshID, Owner, OType, THeight, BHeight, TSShape, ViaSign, TWidth, Diameter, LHRoadID))

		if filepath.find('RFacilityL.shp') > -1:
			LObjectID, MeshID, Owner, OType, LPType, OLHeight, OLLength, LHRoadID = sr.record
			db.c.execute('''INSERT INTO RFacilityL VALUES (?,?,?,?,?,?,?,?)''', (LObjectID, MeshID, Owner, OType, LPType, OLHeight, OLLength, LHRoadID))

		if filepath.find('RFacilityA.shp') > -1:
			AObjectID, MeshID, Owner, OType, OHeight, LHRoadID = sr.record
			db.c.execute('''INSERT INTO RFacilityA VALUES (?,?,?,?,?,?)''', (AObjectID, MeshID, Owner, OType, OHeight, LHRoadID))

def preparse(folderpath):
	"""file I/O and parse all shapes in folder"""

	db = sql.DataBase(sql.DB_NAME)
	db.dropAllTables()
	db.createEMGTables()

	if os.path.isdir(folderpath):
		for pathname, dirnames, filenames in os.walk(sys.argv[1]):
			for filename in filenames:
				if filename.endswith('.shp'):
					filepath = os.path.join(pathname, filename)
					parse_file(db, filepath)
	
	db.conn.commit()

	return db

def main():
	
	if len(sys.argv) == 1:
		print('usage: %s <shapefile or folder>' % __file__)
		sys.exit()

	db = preparse(sys.argv[1])
	db.queryLane()

	db._close()

if __name__ == '__main__':
	main()