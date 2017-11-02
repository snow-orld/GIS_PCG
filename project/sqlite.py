"""
file: sqlite.py

Synthesize .shp related files in a folder to one single OpenDRIVE formatted .XML file

author: Xueman Mou
date: 2017/10/30
version: 1.0.0
modified: 2017/11/1 14:07:00 GMT+800

developing env: python 3.6.2
dependencies  :	sqlite3

Class DataBase Definition
"""

import sqlite3

DB_NAME = 'EMG.db'

# Class DataBase
class DataBase(object):
	
	def __init__(self, name):
		self.db_name = name
		self.c = sqlite3.connect(self.db_name).cursor()
		self.tables = {}	# key - table name, value - schema ?

	def __repr__(self):
		return '{} has {} tables'.format(self.db_name, len(self.tables))

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

	def createEMGTables(self):
		"""Create all tables specified in EMG Spec"""

		## Road Level
		# HRoad 	- Road Reference Line
		
		# HRoadNode	- Connecting Points of Road Reference Line

		# ComplexJunction	- Juncions

		## Lane Level
		# HLane 		- 车道级道路

		# HLaneNode 	- 车道级道路连接点

		# HLRestriction	- 车道级道路交通限制信息

		# HLRCondition	- 车道级道路交通限制条件

		# HLaneInfo 	- 车道级道路形状点高端属性

		# HLaneNodeInfo - 车道级道路连接点高端属性

		## Traffic Markings
		# LMarking		- 线状交通标线

		# AMarking		- 面状交通标线

		## Road Facilities
		# RFacilityP	- 道路设施点

		# RFacilityL 	- 道路设施线

		# RFacilityA 	- 道路设施面
		pass

def main():
	db = DataBase(DB_NAME)
	# db._createTable()
	# db._insert()
	# db._delete()
	# db._search()
	# db._update()

if __name__ == '__main__':
	main()