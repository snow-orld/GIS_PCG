"""
file: sqlite.py

Synthesize .shp related files in a folder to one single OpenDRIVE formatted .XML file

author: Xueman Mou
date: 2017/10/30
version: 1.0.1
modified: 2018/3/13 09:17:00 GMT+800

developing env: python 3.6.3
dependencies  :	sqlite3

Class DataBase Definition
"""

import sqlite3

DB_NAME = 'EMG.db'

# Class DataBase
class DataBase(object):
	
	def __init__(self, name):
		self.db_name = name
		self.conn = sqlite3.connect(self.db_name)
		self.c = self.conn.cursor()

	def _createTable(self):
		print('creating table ...')

	def _insert(self):
		print('inserting ...')

	def _delete(self):
		print('deleting ...')

	def _search(self):
		print('searching ...')

	def _update(self):
		print('updating ...')

	def _close(self):
		print('closing connection ...')
		self.conn.close()

	def createHRoadTable(self):
		self.c.execute('''CREATE TABLE IF NOT EXISTS HRoad(
				HRoadID int(10) PRIMARY KEY,
				MeshID int(10),
				Owner int(6),
				SHNodeID int(10) NOT NULL,
				EHNodeID int(10) NOT NULL,
				HRLength real(16,2) NOT NULL,
				HRType int(2) NOT NULL,
				Direction int(2) NOT NULL,
				LaneNumSE int(2) NOT NULL,
				LaneNumES int(2),
				InnerCJ int(1) NOT NULL,
				LCJID int(10),
				LEDGEID int(10) NOT NULL
			)''')

	def createHRoadNodeTable(self):
		self.c.execute('''CREATE TABLE IF NOT EXISTS HRoadNode(
				HNodeID int(10) PRIMARY KEY,
				MeshID int(10),
				Owner int(6),
				LHNodeID int(10),
				LMeshID int(10),
				LHRoadID char(254) NOT NULL,
				LJCID int(10),
				CJHNFlag int(1) NOT NULL,
				LCJID int(10),
				SSFlag int(1) NOT NULL,
				SSType int(2),
				MergeFlag int(1) NOT NULL,
				SplitFlag int(1) NOT NULL
			)''')

	def createComplexJunctionTable(self):
		self.c.execute('''CREATE TABLE IF NOT EXISTS ComplexJunction(
				CJID int(10) PRIMARY KEY,
				MeshID int(10),
				Owner int(6),
				CJType int(2) NOT NULL,
				CJNameC char(100),
				CJNameP char(254),
				CJNameE char(254),
				CJGroupID int(10)
			)''')

	def createHLaneTable(self):
		self.c.execute('''CREATE TABLE IF NOT EXISTS HLane(
				HLaneID int(11) PRIMARY KEY,
				SeqNum int(2),
				MeshID int(10),
				Owner int(6),
				SHLNdoeID int(10) NOT NULL,
				EHLNodeID int(10) NOT NULL,
				LSpeed int(3),
				LHRoadID char(254),
				VLaneFlag int(1) NOT NULL,
				ETCFlag int(1) NOT NULL,
				SDFlag int(1) NOT NULL,
				EGFlag int(1) NOT NULL,
				RampFlag int(1) NOT NULL,
				MELType int(1),
				NLaneSFlag int(1) NOT NULL
			)''')

	def createHLaneNodeTable(self):
		self.c.execute('''CREATE TABLE IF NOT EXISTS HLaneNode(
				HLNodeID int(10) PRIMARY KEY,
				MeshID int(10),
				Owner int(6),
				LHNodeID int(10) NOT NULL,
				LHLaneID char(254) NOT NULL,
				L real(12,8) NOT NULL,
				B real(12,8) NOT NULL,
				H real(9,3) NOT NULL,
				HLWidth real(8,2)
			)''')

	def createHLRestrictionTable(self):
		self.c.execute('''CREATE TABLE IF NOT EXISTS HLRestriction(
				LRID int(10) PRIMARY KEY,
				SHLaneID int(11) NOT NULL,
				HLNodeID int(10) NOT NULL,
				EHLaneID char(254) NOT NULL,
				RCID char(254)
			)''')

	def createHLRConditionTable(self):
		self.c.execute('''CREATE TABLE IF NOT EXISTS HLRCondition(
				RCID int(10) PRIMARY KEY,
				LUserType char(11) NOT NULL,
				FVFlag int(1) NOT NULL,
				RTime char(200) NOT NULL
			)''')

	def createHLaneInfoTable(self):
		self.c.execute('''CREATE TABLE IF NOT EXISTS HLaneInfo(
				ID int(11) PRIMARY KEY,
				HLaneID int(11) NOT NULL,
				VertexID int(6) NOT NULL,
				L real(12,8) NOT NULL,
				B real(12,8) NOT NULL,
				H real(9,3) NOT NULL,
				Curvature real(8,2),
				Heading real(6,2) NOT NULL,
				Slope real(6,2),
				Width real(8,2)
			)''')

	def createHLaneNodeInfoTable(self):
		self.c.execute('''CREATE TABLE IF NOT EXISTS HLaneNodeInfo(
				ID int(10) PRIMARY KEY,
				HLNodeID int(10) NOT NULL,
				InHLaneID int(11) NOT NULL,
				OutHLaneID int(11) NOT NULL,
				NCurvature real(8,6),
				NHeading real(6,2) NOT NULL,
				NSlope real(6,2)
			)''')

	def createLMarkingTable(self):
		self.c.execute('''CREATE TABLE IF NOT EXISTS LMarking(
				LMID int(10) PRIMARY KEY,
				MeshID int(10),
				Owner int(6),
				LMType int(2) NOT NULL,
				LMColor int(1) NOT NULL,
				LMForm int(2) NOT NULL,
				LMWidth real(16,2) NOT NULL,
				LMLength real(16,2) NOT NULL,
				LHRoadID char(254) NOT NULL,
				LHLaneID char(254) NOT NULL
			)''')

	def createAMarkingTable(self):
		self.c.execute('''CREATE TABLE IF NOT EXISTS AMarking(
				AMID int(10) PRIMARY KEY,
				MeshID int(10),
				Owner int(6),
				AMType int(2) NOT NULL,
				ArrowType int(2),
				LHRoadID char(254) NOT NULL,
				LHLaneID char(254) NOT NULL
			)''')


	def createRFacilityPTable(self):
		self.c.execute('''CREATE TABLE IF NOT EXISTS RFacilityP(
				PObjectID int(10) PRIMARY KEY,
				MeshID int(10),
				Owner int(6),
				OType int(2) NOT NULL,
				THeight real(16,2) NOT NULL,
				BHeight real(16,2),
				TSShape int(2),
				ViaSign int(1),
				TWidth real(16,2),
				Diameter real(16,2),
				LHRoadID char(50) NOT NULL
			)''')

	def createRFacilityLTable(self):
		self.c.execute('''CREATE TABLE IF NOT EXISTS RFacilityL(
				LObject int(10) PRIMARY KEY,
				MeshID int(10),
				Owner int(6),
				OType int(2) NOT NULL,
				LPType int(2),
				OLHeight real(16,2),
				OLLength real(16,2),
				LHRoadID char(50)
			)''')

	def createRFacilityATable(self):
		self.c.execute('''CREATE TABLE IF NOT EXISTS RFacilityA(
				AObjectID int(10) PRIMARY KEY,
				MeshID int(10),
				Owner int(6),
				OType int(2) NOT NULL,
				OHeight real(16,2),
				LHRoadID char(50) NOT NULL
			)''')

	def dropAllTables(self):
		self.c.execute('''DROP TABLE IF EXISTS HRoad''')
		self.c.execute('''DROP TABLE IF EXISTS HRoadNode''')
		self.c.execute('''DROP TABLE IF EXISTS ComplexJunction''')
		self.c.execute('''DROP TABLE IF EXISTS HLane''')
		self.c.execute('''DROP TABLE IF EXISTS HLaneNode''')
		self.c.execute('''DROP TABLE IF EXISTS HLRestriction''')
		self.c.execute('''DROP TABLE IF EXISTS HLRCondition''')
		self.c.execute('''DROP TABLE IF EXISTS HLaneInfo''')
		self.c.execute('''DROP TABLE IF EXISTS HLaneNodeInfo''')
		self.c.execute('''DROP TABLE IF EXISTS LMarking''')
		self.c.execute('''DROP TABLE IF EXISTS AMarking''')
		self.c.execute('''DROP TABLE IF EXISTS RFacilityP''')
		self.c.execute('''DROP TABLE IF EXISTS RFacilityL''')
		self.c.execute('''DROP TABLE IF EXISTS RFacilityA''')

	def createEMGTables(self):
		"""Create all tables specified in EMG Spec"""

		## Road Level
		# HRoad 	- Road Reference Line
		self.createHRoadTable()

		# HRoadNode	- Connecting Points of Road Reference Line
		self.createHRoadNodeTable()

		# ComplexJunction	- Juncions
		self.createComplexJunctionTable()

		## Lane Level
		# HLane 		- 车道级道路
		self.createHLaneTable()

		# HLaneNode 	- 车道级道路连接点
		self.createHLaneNodeTable()

		# HLRestriction	- 车道级道路交通限制信息
		self.createHLRestrictionTable()

		# HLRCondition	- 车道级道路交通限制条件
		self.createHLRConditionTable()

		# HLaneInfo 	- 车道级道路形状点高端属性
		self.createHLaneInfoTable()

		# HLaneNodeInfo - 车道级道路连接点高端属性
		self.createHLaneNodeInfoTable()

		## Traffic Markings
		# LMarking		- 线状交通标线
		self.createLMarkingTable()

		# AMarking		- 面状交通标线
		self.createAMarkingTable()

		## Road Facilities
		# RFacilityP	- 道路设施点
		self.createRFacilityPTable()

		# RFacilityL 	- 道路设施线
		self.createRFacilityLTable()

		# RFacilityA 	- 道路设施面
		self.createRFacilityATable()

	def queryLane(self):
		queryLaneNode = '''SELECT * FROM HLaneNode''';
		# for row in self.c.execute(queryLaneNode):
		# 	print(row)

def main():
	db = DataBase(DB_NAME)
	db.createEMGTables()
	# db._insert()
	# db._delete()
	# db._search()
	# db._update()

if __name__ == '__main__':
	main()