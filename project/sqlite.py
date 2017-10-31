"""
file: sqlite.py

Synthesize .shp related files in a folder to one single OpenDRIVE formatted .XML file

author: Xueman Mou
date: 2017/10/30
version: 1.0.0
modified: 2017/10/30 15:50:00 GMT+800

developing env: python 3.6.2
dependencies  :	sqlite3

input :	path to EMG sample data folder
output: single OpenDRIVE-like .XML file
"""

import sqlite3

conn = sqlite3.connect('example.db')
c = conn.cursor()

# Create table
c.execute('''CREATE TABLE stocks
             (date text, trans text, symbol text, qty real, price real)''')

# Insert a row of data
c.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")

# Save (commit) the changes
conn.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()

def main():
	pass

if __name__ == '__main__':
	main()