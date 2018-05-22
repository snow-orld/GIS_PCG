"""
file: curve.py

Generate polyline curve based on central line of given map road data,
the curve is used to deform the unit highway

author: Xueman Mou
date: 2018/5/18
version: 1.0.0
modified: 2018/5/22 10:19:00 GMT +0800

developing env: python 3.5.2
dependencies: bpy, os, sqlite3, pyshp, pyproj, math, Quaternion
"""

import bpy
import os
import sqlite3
import pyproj
import shapefile
from mathutils import Quaternion
import math

DB = '/Users/mxmcecilia/Documents/GIS_PCG/project/python/ESRI/EMG_GZ.db'

wgs84 = pyproj.Proj(init='epsg:4326') # longlat
ecef = pyproj.Proj(init='epsg:4978') # geocentric

center = None
q = q_prime = None

def hanmilton_product(v1, v2):
	return (v1[0] * v2[0] - v1[1] * v2[1] - v1[2] * v2 [2] - v1[3]*v2[3],
			v1[0] * v2[1] + v1[1] * v2[0] + v1[2] * v2[3] - v1[3]*v2[2],
			v1[0] * v2[2] - v1[1] * v2[3] + v1[2] * v2[0] + v1[3]*v2[1],
			v1[0] * v2[3] + v1[1] * v2[2] - v1[2] * v2[1] + v1[3]*v2[0])

def get_quaternion():
	global center
	global q
	global q_prime
	# calculate quaternion
	# https://www.gamedev.net/forums/topic/429507-finding-the-quaternion-betwee-two-vectors/
	# https://stackoverflow.com/questions/1171849/finding-quaternion-representing-the-rotation-from-one-vector-to-another
	crossproduct = (center[1], -center[0], 0)
	q = Quaternion([0, center[1], -center[0], 0])
	q.w = math.sqrt((center[0]*center[0]+center[1]*center[1]+center[2]*center[2])*(1*1)) + center[2]
	length = math.sqrt(q[0]*q[0]+q[1]*q[1]+q[2]*q[2]+q[3]*q[3])
	q = (q[0]/length, q[1]/length, q[2]/length, q[3]/length)
	# q.normalize() -- 4 digits after .
	q_prime = (q[0], -q[1], -q[2], -q[3])
	#new_center = q*center*q_prime
	new_center = hanmilton_product(hanmilton_product(q, (0,)+center), q_prime)[1:]
	center = new_center
	# print(new_center)

def lonlat_to_local_up(lon_lat_alt, center):
	# lon lat first convert to ecef, then rotate ecef's axis towards up to sky
	co = pyproj.transform(wgs84, ecef, lon_lat_alt[0], lon_lat_alt[1], lon_lat_alt[2])
	co = hanmilton_product(hanmilton_product(q, (0,) + co), q_prime)[1:]
	co = [x - x0 for x, x0 in zip(co, center)]
	return co

def getLanePoints(dirpath):

	conn = sqlite3.connect(DB)
	c = conn.cursor()

	sf = shapefile.Reader(os.path.join(dirpath, 'HRoad.shp'))

	global center
	if center == None:
		lon_0 = sum(sf.bbox[0::2]) * 0.5
		lat_0 = sum(sf.bbox[1::2]) * 0.5
		center = pyproj.transform(wgs84, ecef, lon_0, lat_0, 0)

	for index, sr in enumerate(sf.shapeRecords()):
		
		if index != 3:
			continue
		
		shape = sr.shape
		record = sr.record

		nodes = []

		# first lane node, width in HLaneNode
		c.execute('''SELECT * FROM HRoadNode WHERE HNodeID = ?''', (record[3],))
		result = c.fetchone()
		first_node = (shape.points[0][0], shape.points[0][1], shape.z[0])
		nodes.append(first_node)

		# inner shape nodes, width in HLaneInfo
		c.execute('''SELECT * FROM HRoadInfo WHERE HLaneID = ?''', (record[0],))
		result = c.fetchall()
		for zindex, (point, row) in enumerate(zip(shape.points[1:-1], result)):
			node = (point[0], point[1], shape.z[zindex + 1])
			nodes.append(node)
		
		# last lane node, width in HLaneNode
		c.execute('''SELECT * FROM HRoadNode WHERE HNodeID = ?''', (record[4],))
		result = c.fetchone()
		last_node = (shape.points[-1][0], shape.points[-1][1], shape.z[-1])
		nodes.append(last_node)

		# get_quaternion()
		
		# new_nodes = []
		# for node in nodes:
		# 	node = lonlat_to_local_up(node, center)
		# 	new_nodes.append(node)

		# generatePoly(new_nodes)

	return nodes

def convertCoordinate(points):
	new_points = []

	get_quaternion()

	for point in points:
		point = lonlat_to_local_up(point, center)
		new_points.append(point)

	return new_points

def generatePoly(points):
	curve = bpy.data.curves.new('Poly', type='CURVE')
	curve.dimensions = '3D'
	obj = bpy.data.objects.new('Polyline', curve)
	bpy.context.scene.objects.link(obj)

	polyline = obj.data.splines.new('POLY')
	polyline.points.add(len(points) - 1)
	print('points {}'.format(points))
	for i in range(len(points)):
		polyline.points[i].co = (points[i][0], points[i][1], points[i][2], 1)
	
	# change polyline's center to first point (only then can make sure curved offset center-to-center)

	obj.location = (points[0][0], points[0][1], points[0][2])
	for i in range(len(points)):
		polyline.points[i].co[0] -= points[0][0]
		polyline.points[i].co[1] -= points[0][1]
		polyline.points[i].co[2] -= points[0][2]

def main():
	nodes = getLanePoints('/Users/mxmcecilia/Documents/GIS_PCG/data/EMG_sample_data/EMG_GZ')
	nodes = convertCoordinate(nodes)
	generatePoly(nodes)

if __name__ == '__main__':
	main()