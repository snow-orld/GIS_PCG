#!/usr/bin/python
# -*- coding: utf8 -*-

"""
headreader.py
Provides quick header read support for ESRI Shapefiles.
author: Cecilia M.
date: 2017/09/20
version: 1.0.0
modified: 2017/09/21 10:51:30 GMT+800
Compatible with Python versions 3.6

Modified from original shapefile.py of the pyshp module.
"""

from struct import pack, unpack, calcsize, error, Struct
import array
import os
import sys
import re

from shapetype import SHAPETYPE

class _Array(array.array):
    """Converts python tuples to lits of the appropritate type.
    Used to unpack different shapefile header parts."""
    def __repr__(self):
        return str(self.tolist())

class ShapefileException(Exception):
    """An exception to handle shapefile specific problems."""
    pass

class Reader():
	def __init__(self, *args, **kwargs):
		self.shp = None
		self.shpLength = None
		self.numRecords = None
		self.bbox = None
		self.prj = None
		# See if a shapefile name was passed as an argument
		if len(args) > 0:
			if isinstance(args[0], str):
				self.load(args[0])

	def load(self, shapefile=None):
		"""Opens a shapefile from a filename or file-like
		object. Normally this method would be called by the
		constructor with the file name as an argument."""
		if shapefile:
			(shapename, ext) = os.path.splitext(shapefile)
			try:
				self.shp = open('%s.shp' % shapename, 'rb')
			except IOError:
				pass
			try:
				self.prj = open('%s.prj' % shapename, 'rU')
			except IOError:
				pass
		if self.shp:
			self.__shpHeader()
		if self.prj:
			self.__prjReader()

	def __shpHeader(self):
		"""Reads the header information from a .shp or .shx file."""
		if not self.shp:
			raise ShapefileException("Shapefile Reader requires a shapefile or file-like object. (no shp file found")
		shp = self.shp
		# File length (16-bit word * 2 = bytes)
		shp.seek(24)
		self.shpLength = unpack('>i', self.shp.read(4))[0] * 2
		# Shape type
		shp.seek(32)
		self.shapeType= unpack("<i", shp.read(4))[0]
		# The shapefile's bounding box (lower left, upper right)
		self.bbox = _Array('d', unpack("<4d", shp.read(32)))
		# Elevation
		self.elevation = _Array('d', unpack("<2d", shp.read(16)))
		# Measure
		self.measure = _Array('d', unpack("<2d", shp.read(16)))

	def __prjReader(self):
		"""Reads the projection information from a .prj file."""
		if not self.prj:
			return
		projection_info = self.prj.read()
		# print('%s.prj reads:\n%s\n' % (self.prj, projection_info))
		datum = re.search(r'GEOGCS\[\"(.+)\",DATUM', projection_info).group(1)
		if ''.join(datum.split('_')[1:]) == 'WGS1984':
			self.datum = 'WGS84'

if __name__ == '__main__':
	if len(sys.argv) == 1:
		print('usage: %s shapefile' % __file__)
		sys.exit()

	if os.path.isfile(sys.argv[1]):
		print('%s shape type %s' % (sys.argv[1], Reader(sys.argv[1]).shapeType))

	else:
		types = {}
		for dirpath, dirnames, filenames in os.walk(sys.argv[1]):
			for filename in filenames:
				if filename.endswith('.shp'):
					sf = Reader(os.path.join(dirpath, filename))
					if sf.shapeType not in types:
						types[sf.shapeType] = [(filename, sf.shpLength)]
					else:
						types[sf.shapeType].append((filename, sf.shpLength))

		for shapetype in types:
			print(shapetype, types[shapetype])
			for filename, shpLength in sorted(types[shapetype], key=lambda shp: shp[1], reverse=True):
				print('\t%s\t%s' % (filename.ljust(32), str(shpLength).rjust(12)))
