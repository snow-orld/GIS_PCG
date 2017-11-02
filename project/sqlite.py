"""
file: sqlite.py

Synthesize .shp related files in a folder to one single OpenDRIVE formatted .XML file

author: Xueman Mou
date: 2017/10/30
version: 1.0.0
modified: 2017/11/1 14:07:00 GMT+800

developing env: python 3.6.2
dependencies  :	sqlite3

input :	path to EMG sample data folder (by calling preparse.py)
output: single OpenDRIVE-like .XML file
"""

import sqlite3

# DB_NAME = 'EMG.db'
DB_NAME = 'tutorial.db'

# Class DataBase
class DataBase(object):
	
	def __init__(self, name):
		self.db_name = name
		self.c = sqlite3.connect(self.db_name).cursor()
		self.tables = {}	# key - table name, value - schema ?

	def __repr__(self):
		return '{} has {} tables'.format(self.db_name, len(self.tables))

	def insert(self, table, tuples):
		print('inserting ...')

	def delete(self):
		print('deleting ...')

	def search(self):
		print('searching ...')

	def update(self):
		print('updating ...')

def main():
	db = DataBase(DB_NAME)
	test(db)

# Test
def test(db):
	# Create table
	db.c.execute('''CREATE TABLE stocks
					(date text, trans text, symbol text, qty real, price real)''')

if __name__ == '__main__':
	main()