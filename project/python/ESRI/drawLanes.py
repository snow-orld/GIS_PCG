"""
file: drawLanes.py

draw closed lanes with surfaces. Lanes can be in a junction.

author: Xueman Mou
date: 2018/3/19
version: 1.0.1
modified: 2018/3/27 09:09:00 GMT +800

developing env: python 3.5.2
dependencies: sqlite3, pyshp, pyproj, bpy, bmesh, mathutils
"""

import bpy
import bmesh
import os
import sys
import shapefile
import pyproj
import sqlite3
from mathutils import Vector

# proj parameters
wgs84 = pyproj.Proj(init='epsg:4326') # longlat
ecef = pyproj.Proj(init='epsg:4978') # geocentric

# center of drawing as first shapefile's center
center = None

# EMG.db
DB = '/Users/mxmcecilia/Documents/GIS_PCG/project/python/ESRI/EMG_GZ.db'

def ls(folder):
	shapefiles = []
	for dirpath, dirnames, filenames in os.walk(folder):
		for filename in filenames:
			if filename.endswith('.shp'):
				shapefiles.append(filename)

	return shapefiles

def filterRoadsNotInJunction(folderpath):
	"""find roads' IDs that are not in any junctions"""
	roadIDs = set()

	sf = shapefile.Reader(os.path.join(folderpath, 'HRoad.shp'))
	print('Type %s' % sf.shapeType)
	
	for sr in sf.shapeRecords():
		record = sr.record
		if record[-3] == 1 and record[-3] not in roadIDs:
			roadIDs.add(str(record[0]))

	return roadIDs

def draw_shp(shpname, roadIDs):
	sf = shapefile.Reader(shpname)

	# print('Type %s' % sf.shapeType)
	# print('ShapeRecords num #%d' % len(sf.shapeRecords()))

	# invalid type
	if not sf.shapeType in [1, 3, 5, 8, 11, 13, 15, 18, 21, 23, 25, 28, 31]:
		return

	# recenter bbox 
	global center
	if center == None:
		lon_0 = sum(sf.bbox[0::2]) * 0.5
		lat_0 = sum(sf.bbox[1::2]) * 0.5
		center = pyproj.transform(wgs84, ecef, lon_0, lat_0, 0)
		print('\ncenter longlatalt(%f, %f, %f)' % (lon_0, lat_0, 0))
		print('ecef {}'.format(center))

	bm = bmesh.new()

	for srindex, shapeRec in enumerate(sf.shapeRecords()):
		shape = shapeRec.shape
		record = shapeRec.record

		# print('\nShape#%d %d parts, %d points, record: %s' % (srindex, len(shape.parts), len(shape.points), record))

		# only draw roads not in junctions for now
		if os.path.basename(shpname) == 'HLane.shp':
			if record[7] not in roadIDs:
				continue

		if len(shape.parts) == 0:

			if os.path.basename(shpname).find('RFacilityP') == 0:
				if srindex in [1, 15, 16, 37, 56]:
					vert.select = True

			for pindex, point in enumerate(shape.points):
				# point is of type shapefile._Array
				co = (point[0], point[1], shape.z[pindex])
				co = pyproj.transform(wgs84, ecef, co[0], co[1], co[2])
				co = [x - x0 for x, x0 in zip(co, center)]
				if shape.shapeType == 11:
					vert = bm.verts.new(co)
		else:

			for pindex, part in enumerate(shape.parts):
				start_index = part
				end_index = shape.parts[pindex + 1] - 1 if pindex < len(shape.parts) - 1 else len(shape.points) - 1

				verts_in_edge_loop = []
				verts_in_face = []

				for sub_index, point in enumerate(shape.points[start_index:end_index+1]):
					sub_index_next = (sub_index + 1) % (end_index + 1 - start_index)
					point_next = shape.points[start_index + sub_index_next]
					
					co = point + (shape.z[start_index + sub_index],)
					co_next = point_next + (shape.z[start_index + sub_index_next],)
					
					# print('\nlonglatalt {}'.format(co))
					co = pyproj.transform(wgs84, ecef, co[0], co[1], co[2])
					co_next = pyproj.transform(wgs84, ecef, co_next[0], co_next[1], co_next[2])
					# print('ecef {}'.format(co))

					co = [x - x0 for x, x0 in zip(co, center)]
					co_next = [x - x0 for x, x0 in zip(co_next, center)]
					# print('centered {}'.format(co))

					if shape.shapeType == 13:
						vert = bm.verts.new(co)
						verts_in_edge_loop.append(vert)
					if shape.shapeType == 15:
						vert = bm.verts.new(co)
						verts_in_face.append(vert)
				
				if verts_in_edge_loop:
					for vindex, vert in enumerate(verts_in_edge_loop):
						if vindex == len(verts_in_edge_loop) - 1:
							break
						bm.edges.new([vert, verts_in_edge_loop[vindex + 1]])

				if verts_in_face:
					face = bm.faces.new(verts_in_face)
					bmesh.ops.reverse_faces(bm, faces=[face])

	dataname = os.path.splitext(os.path.basename(shpname))[0]
	me = bpy.data.meshes.new(dataname)
	file_obj = bpy.data.objects.new(dataname, me)
	bpy.context.scene.objects.link(file_obj)

	bm.to_mesh(me)
	bm.free()

def draw_lane_not_in_junction(dirpath):
	
	conn = sqlite3.connect(DB)
	c = conn.cursor()

	# all lane IDs that are not in junctions
	c.execute('''SELECT HLaneID FROM HLane INNER JOIN HRoad
		ON HLane.LHRoadID = HRoad.HRoadID
		WHERE HRoad.InnerCJ == 1
		''')
	
	count = 0
	laneIDs = [t[0] for t in c.fetchall()]
	for laneID in laneIDs:
		print('\n%d' % laneID)
		draw_single_lane(dirpath, laneID)
		
		# count += 1
		# if count > 3:
		# 	break

	conn.close()

class laneNode(object):
	"""laneNode including info about B, L, H etc."""
	def __init__(self, L, B, H, width=None):
		self.lon = L
		self.lat = B
		self.alt = H
		self.width = width
		
def draw_lanes(dirpath):

	conn = sqlite3.connect(DB)
	c = conn.cursor()

	sf = shapefile.Reader(os.path.join(dirpath, 'HLane.shp'))
	for index, sr in enumerate(sf.shapeRecords()):
		shape = sr.shape
		record = sr.record

		if record[-1] == 1 or record[-1]==2:

			# the lane is with in a fixed lane
			print('lane #%d, is within unspecified area %s' % (record[0], 'no' if record[-1]==1 else 'yes') )
			nodes = []
			nodes_zero_width = []

			# first lane node, width in HLaneNode
			c.execute('''SELECT * FROM HLaneNode WHERE HLNodeID = ?''', (record[4],))
			result = c.fetchone()
			first_node = laneNode(shape.points[0][0], shape.points[0][1], shape.z[0], result[8])
			nodes.append(first_node)
			
			# last lane node, width in HLaneNode
			c.execute('''SELECT * FROM HLaneNode WHERE HLNodeID = ?''', (record[5],))
			result = c.fetchone()
			last_node = laneNode(shape.points[-1][0], shape.points[-1][1], shape.z[-1], result[8])
	
			# inner shape nodes, width in HLaneInfo
			laneID = record[0]
			c.execute('''SELECT * FROM HLaneInfo WHERE HLaneID = ?''', (laneID,))
			for zindex, (point, row) in enumerate(zip(shape.points[1:-1], c.fetchall())):
				if record[-1] == 1:
					width = row[9]
				elif record[-1] == 2:
					# linear interpolation for lanes that are not in specified within boundaries
					width = first_node.width + (last_node.width - first_node.width) * (zindex + 1) / (len(shape.points))
				node = laneNode(point[0], point[1], shape.z[zindex + 1], width)
				if laneID in (50100000070, 50100000101, 50100000136, 50100000137):
					print(row[9])
				nodes.append(node)
				
			nodes.append(last_node)

			# deal with leading/ending width
			if nodes[1].width == 0:
				nodes[0].width = 0
			if nodes[-2].width == 0:
				nodes[-1].width = 0
			count = 0
			while nodes[count].width == 0:
				count += 1
				if count == len(nodes):
					break
			if count > 1:
				nodes_zero_width = nodes[:count]
				nodes = nodes[count:]
			last_count = 0
			if len(nodes)>0:
				while nodes[-1-last_count].width == 0:
					last_count += 1
					if last_count == len(nodes):
						break
			if last_count > 1:
				nodes_zero_width = nodes[-last_count:]
				nodes = nodes[:-last_count]

			verts_left = []
			verts_central = []
			verts_right = []
			verts_in_face = []

			bm = bmesh.new()
			
			for index, node in enumerate(nodes):
				co = (node.lon, node.lat, node.alt)
				width = node.width

				co = pyproj.transform(wgs84, ecef, co[0], co[1], co[2])
				up = Vector(co)
				up.normalize()

				co = [x - x0 for x, x0 in zip(co, center)]
				
				forward = None
				if index < len(nodes) - 1:
					co_next = (nodes[index + 1].lon, nodes[index + 1].lat, nodes[index + 1].alt)
					co_next = pyproj.transform(wgs84, ecef, co_next[0], co_next[1], co_next[2])
					co_next = [x - x0 for x, x0 in zip(co_next, center)]
					forward = [x - y for x, y in zip(co_next, co)]
					forward = Vector(forward)
					forward.normalize()
				else:
					co_prev = (nodes[index - 1].lon, nodes[index - 1].lat, nodes[index - 1].alt)
					co_prev = pyproj.transform(wgs84, ecef, co_prev[0], co_prev[1], co_prev[2])
					co_prev = [x - x0 for x, x0 in zip(co_prev, center)]
					forward = [x - y for x, y in zip(co, co_prev)]
					forward = Vector(forward)
					forward.normalize()

				left = up.cross(forward)
				left.normalize()

				co = Vector(co)
				vert1 = bm.verts.new(left * width / 2 + co)
				vert2 = bm.verts.new(-left * width / 2 + co)

				verts_left.append(vert1)
				verts_right.append(vert2)

			# drawing central points for nodes with 0 width
			for index, node_zero_width in enumerate(nodes_zero_width):
				co = (node.lon, node.lat, node.alt)
				co = pyproj.transform(wgs84, ecef, co[0], co[1], co[2])
				co = [x - x0 for x, x0 in zip(co, center)]
				vert3 = bm.verts.new(co)
				verts_central.append(vert3)
					
			# for vindex, vert in enumerate(verts_left):
			# 	if vindex == len(verts_left) - 1 :
			# 		break
			# 	else:
			# 		bm.edges.new([vert, verts_left[vindex + 1]])

			# for vindex, vert in enumerate(verts_right):
			# 	if vindex == len(verts_right) - 1 :
			# 		break
			# 	else:
			# 		bm.edges.new([vert, verts_right[vindex + 1]])

			for vindex, vert in enumerate(verts_central):
				if vindex == len(verts_central) - 1 :
					break
				else:
					bm.edges.new([vert, verts_central[vindex + 1]])

			verts_left.reverse()
			verts_in_face = verts_left + verts_right
			if len(verts_in_face) > 1:
				bm.faces.new(verts_in_face)
			
			dataname = str(laneID)
			me = bpy.data.meshes.new(dataname)
			file_obj = bpy.data.objects.new(dataname, me)
			bpy.context.scene.objects.link(file_obj)

			bm.to_mesh(me)
			bm.free()

			# test_helper(dirpath, laneID)
	conn.close()

def draw_single_lane(dirpath, laneID):

	conn = sqlite3.connect(DB)
	c = conn.cursor()

	nodes = []

	# get laneNodes first, with HLane and width info from HLaneNode and HLaneInfo
	sf = shapefile.Reader(os.path.join(dirpath, 'HLane.shp'))
	for index, sr in enumerate(sf.shapeRecords()):
		shape = sr.shape
		record = sr.record

		if record[0] != laneID:
			continue

		# first lane node, width in HLaneNode
		c.execute('''SELECT * FROM HLaneNode WHERE HLNodeID = ?''', (record[4],))
		result = c.fetchone()
		node = laneNode(shape.points[0][0], shape.points[0][1], shape.z[0], result[8])
		nodes.append(node)

		c.execute('''SELECT * FROM HLaneInfo WHERE HLaneID = ?''', (laneID,))
		for zindex, (point, row) in enumerate(zip(shape.points[1:-1], c.fetchall())):
			node = laneNode(point[0], point[1], shape.z[zindex + 1], row[9])
			nodes.append(node)

		# last lane node, width in HLaneNode
		c.execute('''SELECT * FROM HLaneNode WHERE HLNodeID = ?''', (record[5],))
		result = c.fetchone()
		node = laneNode(shape.points[-1][0], shape.points[-1][1], shape.z[-1], result[8])
		nodes.append(node)

	conn.close()

	bm = bmesh.new()

	verts_left = []
	verts_right = []
	verts_central = []
	verts_in_face = []

	# deal with width 0 neibours
	nodes_zero_width = None
	if nodes[1].width == 0:
		nodes[0].width = 0
	if nodes[-2].width == 0:
		nodes[-1].width = 0
	count = 0
	while nodes[count].width == 0 and count <= len(nodes) - 1:
		count += 1
	if count > 1:
		nodes_zero_width = nodes[:count]
		nodes = nodes[count:]
	last_count = 0
	while nodes[-1-last_count].width == 0 and last_count <= len(nodes) - 1:
		last_count += 1
	if last_count > 1:
		nodes_zero_width = nodes[-last_count:]
		nodes = nodes[:-last_count]
	
	# end of dealing with 0 width problem

	for index, node in enumerate(nodes):
		co = (node.lon, node.lat, node.alt)
		width = node.width

		co = pyproj.transform(wgs84, ecef, co[0], co[1], co[2])
		up = Vector(co)
		up.normalize()

		co = [x - x0 for x, x0 in zip(co, center)]
		
		forward = None
		if index < len(nodes) - 1:
			co_next = (nodes[index + 1].lon, nodes[index + 1].lat, nodes[index + 1].alt)
			co_next = pyproj.transform(wgs84, ecef, co_next[0], co_next[1], co_next[2])
			co_next = [x - x0 for x, x0 in zip(co_next, center)]
			forward = [x - y for x, y in zip(co_next, co)]
			forward = Vector(forward)
			forward.normalize()
		else:
			co_prev = (nodes[index - 1].lon, nodes[index - 1].lat, nodes[index - 1].alt)
			co_prev = pyproj.transform(wgs84, ecef, co_prev[0], co_prev[1], co_prev[2])
			co_prev = [x - x0 for x, x0 in zip(co_prev, center)]
			forward = [x - y for x, y in zip(co, co_prev)]
			forward = Vector(forward)
			forward.normalize()

		left = up.cross(forward)
		left.normalize()

		co = Vector(co)
		vert1 = bm.verts.new(left * width / 2 + co)
		vert2 = bm.verts.new(-left * width / 2 + co)
		# vert2 = bm.verts.new(co)
		
		vert1.select = True
		vert2.select = True
		
		verts_left.append(vert1)
		verts_right.append(vert2)

	# drawing central points for nodes with 0 width
	if nodes_zero_width is not None:
		for index, node_zero_width in enumerate(nodes_zero_width):
			co = (node.lon, node.lat, node.alt)
			co = pyproj.transform(wgs84, ecef, co[0], co[1], co[2])
			co = [x - x0 for x, x0 in zip(co, center)]
			vert3 = bm.verts.new(co)
			verts_central.append(vert3)
			
	for vindex, vert in enumerate(verts_left):
		if vindex == len(verts_left) - 1 :
			break
		else:
			bm.edges.new([vert, verts_left[vindex + 1]])

	for vindex, vert in enumerate(verts_right):
		if vindex == len(verts_right) - 1 :
			break
		else:
			bm.edges.new([vert, verts_right[vindex + 1]])

	for vindex, vert in enumerate(verts_central):
		if vindex == len(verts_central) - 1 :
			break
		else:
			bm.edges.new([vert, verts_central[vindex + 1]])

	verts_left.reverse()
	verts_in_face = verts_left + verts_right
	bm.faces.new(verts_in_face)
	
	dataname = str(laneID)
	me = bpy.data.meshes.new(dataname)
	file_obj = bpy.data.objects.new(dataname, me)
	bpy.context.scene.objects.link(file_obj)

	bm.to_mesh(me)
	bm.free()

	# test_helper(dirpath, laneID)

def test_helper(dirpath, laneID):
	# draw reference line of single lane
	sf = shapefile.Reader(os.path.join(dirpath,'HLane.shp'))
	for index, sr in enumerate(sf.shapeRecords()):
		shape = sr.shape
		record = sr.record
		
		if record[0] != laneID:
			continue

		verts_in_edge_loop = []

		if record[0] == laneID:
			bm = bmesh.new()
			# print('shape.parts #%d, shape.points #%d, shape.z #%d' % (len(shape.parts), len(shape.points), len(shape.z)))
			for pindex, point in enumerate(shape.points):
				co = point + (shape.z[pindex],)
				co = pyproj.transform(wgs84, ecef, co[0], co[1], co[2])
				co = [x - x0 for x, x0 in zip(co, center)]
				
				vert = bm.verts.new(co)
				verts_in_edge_loop.append(vert)

			if verts_in_edge_loop:
				for vindex, vert in enumerate(verts_in_edge_loop):
					if vindex == len(verts_in_edge_loop) - 1:
						break
					bm.edges.new([vert, verts_in_edge_loop[vindex + 1]])

			dataname = 'laneC_' + str(laneID)
			me = bpy.data.meshes.new(dataname)
			file_obj = bpy.data.objects.new(dataname, me)
			bpy.context.scene.objects.link(file_obj)

			bm.to_mesh(me)
			bm.free()

def main():

	pathname = '/Users/mxmcecilia/Documents/GIS_PCG/data/EMG_sample_data/EMG_GZ'

	shapefiles = ls(pathname)
	
	if os.path.isfile(pathname):
		if os.path.exists(pathname):
			print('Drawing %s ...' % pathname)
			draw_shp(pathname)
	else:
		shapefiles = ls(pathname)

		# print('%d shapefiles' % len(shapefiles))
		roadIDs = filterRoadsNotInJunction(pathname)

		for index, filename in enumerate(shapefiles):
			print('Drawing %s ...' % filename)	
			draw_shp(os.path.join(pathname, filename), roadIDs)

	# draw_lane_not_in_junction(pathname)
	draw_lanes(pathname)

if __name__ == '__main__':
	main()