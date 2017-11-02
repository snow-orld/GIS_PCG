"""
file: preparse.py

Parse original ESRI files to data sets acceptable for sqlite insertion.

author: Xueman Mou
date: 2017/11/1
version: 1.0.0
modified: 2017/11/1 16:28:00 GMT+800

developing env: python 3.6.2
dependencies  :	shapefile, pyproj

input :	path to EMG sample data folder
output: RDBMS insertion and hierachical mesh with shpName|-recID|-partID(only one part in each shape for now)
"""

import os
import sys
import shapefile

def parse(filepath):
	"""
	shape-record pair (shape is like a basic geometry or road, more
	suitably, in OpenDRIVE standard)

	input : filepath
	output: tables (schema and tuples)
	"""

	print(filepath)

	sf = shapefile.Reader(filepath)
	fields = sf.fields[1:]	# ('DeletionFlag' is not specified in EMG's spec)

	# Attributes
	# ['AttributeName', 'Type', 'LengthIntegral', 'LengthFractal']
	# NOTE: EMG spec has an additional contraint 'Obl' for value that must be present
	for field in fields:
		attribute, datatype, lenA, lenB = field
		print('\t%s%s\t%s\t%s\t%s' % (attribute, ' '*(8 - len(attribute)), datatype, lenA, lenB))

	# Tuples
	for srindex, sr in enumerate(sf.shapeRecords()):
		print('#%03d %s' % (srindex, sr.record))

def main():
	"""file I/O and parse all shapes in folder"""

	if len(sys.argv) == 1:
		print('usage: %s <shapefile or folder>' % __file__)
		sys.exit()

	if os.path.isdir(sys.argv[1]):
		for pathname, dirnames, filenames in os.walk(sys.argv[1]):
			for filename in filenames:
				if filename.endswith('.shp'):
					filepath = os.path.join(pathname, filename)
					# filter: road and lane only
					if filepath.find('Road') > -1:
						parse(filepath)
					# if filepath.find('Lane') > -1:
					# 	parse(filepath)

if __name__ == '__main__':
	main()