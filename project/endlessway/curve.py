"""
file: curve.py

Generate polyline curve based on central line of given map road data,
the curve is used to deform the unit highway

author: Xueman Mou
date: 2018/5/18
version: 1.0.0
modified: 2018/5/18 08:27:00 GMT +0800

developing env: python 3.5.2
dependencies: bpy, os, sqlite3, pyshp, pyproj
"""

import bpy
import os
import sqlite3
import pyproj
import shapefile

DB = '/Users/mxmcecilia/Documents/GIS_PCG/project/python/ESRI/EMG_GZ.db'

wgs84 = pyproj.Proj(init='epsg:4326') # longlat
ecef = pyproj.Proj(init='epsg:4978') # geocentric

center = None

def getLanePoints(dirpath):

	conn = sqlite3.connect(DB)
	c = conn.cursor()

	sf = shapefile.Reader(os.path.join(dirpath, 'HLane.shp'))

	global center
	if center == None:
		lon_0 = sum(sf.bbox[0::2]) * 0.5
		lat_0 = sum(sf.bbox[1::2]) * 0.5
		center = pyproj.transform(wgs84, ecef, lon_0, lat_0, 0)

	for index, sr in enumerate(sf.shapeRecords()):
		
		if index > 0:
			break
		
		shape = sr.shape
		record = sr.record

		nodes = []

		# first lane node, width in HLaneNode
		c.execute('''SELECT * FROM HLaneNode WHERE HLNodeID = ?''', (record[4],))
		result = c.fetchone()
		first_node = (shape.points[0][0], shape.points[0][1], shape.z[0])
		nodes.append(first_node)

		# inner shape nodes, width in HLaneInfo
		c.execute('''SELECT * FROM HLaneInfo WHERE HLaneID = ?''', (record[0],))
		result = c.fetchall()
		for zindex, (point, row) in enumerate(zip(shape.points[1:-1], result)):
			node = (point[0], point[1], shape.z[zindex + 1])
			nodes.append(node)
		
		# last lane node, width in HLaneNode
		c.execute('''SELECT * FROM HLaneNode WHERE HLNodeID = ?''', (record[5],))
		result = c.fetchone()
		last_node = (shape.points[-1][0], shape.points[-1][1], shape.z[-1])
		nodes.append(last_node)

	return nodes

def convertCoordinate(points):
	new_points = []

	for point in points:
		point = pyproj.transform(wgs84, ecef, point[0], point[1], point[2])
		point = [x - x0 for x, x0 in zip(point, center)]
		new_points.append(point)

	return new_points

def generatePoly(points):
	pass

def main():
	nodes = getLanePoints('/Users/mxmcecilia/Documents/GIS_PCG/data/EMG_sample_data/EMG_GZ')
	nodes = convertCoordinate(nodes)
	generatePoly(nodes)

if __name__ == '__main__':
	main()