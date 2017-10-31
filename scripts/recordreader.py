#!/usr/bin/python
# -*- coding: utf8 -*-

"""
recordreader.py
Provides quick header read support for ESRI Shapefiles.
author: Cecilia M.
date: 2017/10/09
version: 1.0.0
modified: 2017/10/10 12:06:30 GMT+800
Compatible with Python versions 3.6

Future Reference:

Find a record by field name
https://gis.stackexchange.com/questions/74808/extract-a-record-by-name-in-pyshp

"""

import os
import sys
import shapefile

def write_facility_file(type, field_names, fdict):
	dirname = '..\data\EMG_sample_data'
	if type == 'P':
		outfile = os.path.join(dirname, 'RFacilityPAttrs.csv')
	elif type == 'L':
		outfile = os.path.join(dirname, 'RFacilityLAttrs.csv')
	elif type == 'A':
		outfile = os.path.join(dirname, 'RFacilityAAttrs.csv')
	else:
		print('Error: Invalid RFacility Type')
		return

	if not os.path.exists(outfile):
		with open(outfile, 'w') as f:
			f.write('%s,%s\n' % ('RecordIndex', ','.join(field_names)))
			for attrs, srindex in fdict.items():
				# print('#%03d %s' % (srindex, attrs))
				f.write('#%03d,%s\n' % (srindex, ','.join([str(num) for num in attrs])))

def show_records(filepath, maxlimit=10):
	sf = shapefile.Reader(filepath)
	field_names = [field[0] for field in sf.fields[1:]]
	print('\n%s type %s\n' % (filepath, sf.shapeType))
	print('Filed%s' % field_names)

	RFacilityP = {}
	RFacilityL = {}
	RFacilityA = {}

	for srindex, sr in enumerate(sf.shapeRecords()):
		if srindex >= maxlimit:
			break
		if os.path.basename(filepath).find('ComplexJunction') > -1:
			attrs = sr.record[:4]
			attrs.append(sr.record[4].decode('gb2312'))
			attrs += sr.record[5:]
			print('#%03d %s' % (srindex, attrs))
		elif os.path.basename(filepath).find('RFacilityP') > -1:
			# print('#%03d %s' % (srindex, sr.record))
			attrs = tuple(sr.record[3:10])
			if attrs not in RFacilityP:
				RFacilityP[attrs] = srindex
			if sr.record[3] == 5:
				print('#%03d %s' % (srindex, sr.record))
		elif os.path.basename(filepath).find('RFacilityL') > -1:
			print('#%03d %s' % (srindex, sr.record))
			attrs = tuple(sr.record[3:8])
			if attrs not in RFacilityL:
				RFacilityL[attrs] = srindex
		elif os.path.basename(filepath).find('RFacilityA') > -1:
			print('#%03d %s' % (srindex, sr.record))
			attrs = tuple(sr.record[3:6])
			if attrs not in RFacilityL:
				RFacilityA[attrs] = srindex
		else:
			print('#%03d %s' % (srindex, sr.record))

	if RFacilityP:
		write_facility_file('P', field_names[3:10], RFacilityP)
	if RFacilityL:
		write_facility_file('L', field_names[3:8], RFacilityL)
	if RFacilityA:
		write_facility_file('A', field_names[3:6], RFacilityA)

if __name__ == '__main__':
	if len(sys.argv) == 1:
		print('usage: %s shapefile' % __file__)
		sys.exit()

	if os.path.isdir(sys.argv[1]):
		for pathname, dirnames, filenames in os.walk(sys.argv[1]):
			for filename in filenames:
				if filename.endswith('.shp'):
					show_records(os.path.join(pathname, filename))
	else:
		show_records(sys.argv[1])