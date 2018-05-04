"""
file: drawLanes.py

draw closed lanes with surfaces. Lanes can be in a junction.

author: Xueman Mou
date: 2018/3/19
version: 1.0.4
modified: 2018/5/4 09:05:00 GMT +0800

developing env: python 3.5.2
dependencies: sqlite3, pyshp, pyproj, bpy, bmesh, mathutils, math
"""

import bpy
import bmesh
import os
import sys
import shapefile
import pyproj
import sqlite3
from mathutils import Vector, Quaternion
import math

# proj parameters
wgs84 = pyproj.Proj(init='epsg:4326') # longlat
ecef = pyproj.Proj(init='epsg:4978') # geocentric

# center of drawing as first shapefile's center
center = None
q = None
q_prime = None

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

def draw_shp(shpname):

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
					# bmesh.ops.triangulate(bm, faces=bm.faces)

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

		road_obj_name = 'Road_' + record[7]
		road_obj = None
		if bpy.data.objects.find(road_obj_name) == -1:
			road_obj = bpy.data.objects.new(road_obj_name, None)
			bpy.context.scene.objects.link(road_obj)
		else:
			road_obj = bpy.data.objects[road_obj_name]

		nodes = []

		if record[14] == 1:

			# the lane is with in a fixed lane
			# print('lane #%d, is within unspecified area %s' % (record[0], 'no' if record[14]==1 else 'yes') )
			# print('VLaneFlag %d, ETCFlag %d, SDFlag %d, EGFlag %d, RampFlag %d, MELType %d, NLaneSFlag %d' % (record[8], record[9], record[10], record[11], record[12], record[13], record[14]))

			# first lane node, width in HLaneNode
			c.execute('''SELECT * FROM HLaneNode WHERE HLNodeID = ?''', (record[4],))
			result = c.fetchone()
			first_node = laneNode(shape.points[0][0], shape.points[0][1], shape.z[0], result[8])
			nodes.append(first_node)
			
			# inner shape nodes, width in HLaneInfo
			c.execute('''SELECT * FROM HLaneInfo WHERE HLaneID = ?''', (record[0],))
			result = c.fetchall()
			for zindex, (point, row) in enumerate(zip(shape.points[1:-1], result)):
				width = row[9]
				node = laneNode(point[0], point[1], shape.z[zindex + 1], width)
				nodes.append(node)

			# last lane node, width in HLaneNode
			c.execute('''SELECT * FROM HLaneNode WHERE HLNodeID = ?''', (record[5],))
			result = c.fetchone()
			last_node = laneNode(shape.points[-1][0], shape.points[-1][1], shape.z[-1], result[8])
			nodes.append(last_node)
			
		elif record[14] == 2:

			# if lane is in unspecified area, HLaneInfo 's width is all 0.0
			# width is determined at each node by cases
			c.execute('''SELECT * FROM HLaneNode WHERE HLNodeID = ?''', (record[4],))
			result = c.fetchone()
			first_node = laneNode(shape.points[0][0], shape.points[0][1], shape.z[0], result[8])
			nodes.append(first_node)

			# last lane node, width in HLaneNode
			c.execute('''SELECT * FROM HLaneNode WHERE HLNodeID = ?''', (record[5],))
			result = c.fetchone()
			last_node = laneNode(shape.points[-1][0], shape.points[-1][1], shape.z[-1], result[8])
			
			c.execute('''SELECT * FROM HLaneInfo WHERE HLaneID = ?''', (record[0],))
			result = c.fetchall()

			# to deal with shoulder-like lanes merge out and merge in
			
			if first_node.width != 0 and last_node.width != 0:
				is_zero_width_inbetween = True
				for row in result:
					if row[9] != 0:
						is_zero_width_inbetween = False
						break
				if is_zero_width_inbetween:
					for zindex, (point, row) in enumerate(zip(shape.points[1:-1], result)):
						width = first_node.width + (last_node.width - first_node.width) * (zindex + 1)/len(shape.points)
						node = laneNode(point[0], point[1], shape.z[zindex + 1], width)
						nodes.append(node)

			nodes.append(last_node)
			
		# draw lane by lane
		draw_single_lane(nodes, record[0], road_obj)

	# test_helper(dirpath)
	conn.close()

def draw_single_lane(nodes, laneID, parent=None):
	"""return the center of the lane face, and the radius bound"""
	bm = bmesh.new()

	my_nodes = nodes
	nodes_zero_width = []

	verts_left = []
	verts_right = []
	verts_central = []
	verts_in_face = []

	# deal with width 0 neibours
	if my_nodes[1].width == 0:
		my_nodes[0].width = 0
	if my_nodes[-2].width == 0:
		my_nodes[-1].width = 0
	count = 0
	while my_nodes[count].width == 0:
		count += 1
		if count == len(my_nodes):
			break
	if count > 1:
		nodes_zero_width += my_nodes[:count]
		my_nodes = my_nodes[count:]
	last_count = 0
	if len(my_nodes) > 0:
		while my_nodes[-1-last_count].width == 0:
			last_count += 1
			if last_count == len(my_nodes):
				break
	if last_count > 0:
		nodes_zero_width += my_nodes[-last_count:]
		my_nodes = my_nodes[:-last_count]
	
	# end of dealing with 0 width problem

	for index, node in enumerate(my_nodes):
		co = (node.lon, node.lat, node.alt)
		width = node.width

		co = pyproj.transform(wgs84, ecef, co[0], co[1], co[2])
		# co = hanmilton_product(hanmilton_product(q, (0,) + co), q_prime)[1:]
		up = Vector(co)
		up.normalize()

		co = [x - x0 for x, x0 in zip(co, center)]
		
		forward = None
		if index < len(my_nodes) - 1:
			co_next = (my_nodes[index + 1].lon, my_nodes[index + 1].lat, my_nodes[index + 1].alt)
			co_next = pyproj.transform(wgs84, ecef, co_next[0], co_next[1], co_next[2])
			# co_next = hanmilton_product(hanmilton_product(q, (0,) + co_next), q_prime)[1:]
			
			co_next = [x - x0 for x, x0 in zip(co_next, center)]
			forward = [x - y for x, y in zip(co_next, co)]
			forward = Vector(forward)
			forward.normalize()
		else:
			co_prev = (my_nodes[index - 1].lon, my_nodes[index - 1].lat, my_nodes[index - 1].alt)
			co_prev = pyproj.transform(wgs84, ecef, co_prev[0], co_prev[1], co_prev[2])
			# co_prev = hanmilton_product(hanmilton_product(q, (0,) + co_prev), q_prime)[1:]
			
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
		
		verts_left.append(vert1)
		verts_right.append(vert2)

	# drawing central points for nodes with 0 width	
	for index, node in enumerate(nodes_zero_width):
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
	if len(verts_in_face) > 1:
		face = bm.faces.new(verts_in_face)

	dataname = str(laneID)
	me = bpy.data.meshes.new(dataname)
	file_obj = bpy.data.objects.new(dataname, me)
	bpy.context.scene.objects.link(file_obj)
	if parent is not None:
		file_obj.parent = parent

	bm.to_mesh(me)
	bm.free()

def test_helper(dirpath):
	# draw reference line of single lane
	sf = shapefile.Reader(os.path.join(dirpath,'HLane.shp'))
	for index, sr in enumerate(sf.shapeRecords()):
		shape = sr.shape
		record = sr.record
	
		verts_in_edge_loop = []
		
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

		dataname = 'laneC_' + str(record[0])
		me = bpy.data.meshes.new(dataname)
		obj = bpy.data.objects.new(dataname, me)
		bpy.context.scene.objects.link(obj)

		bm.to_mesh(me)
		bm.free()

def calculate_all_center(dirpath):
	conn = sqlite3.connect(DB)
	c = conn.cursor()
	c.execute('select HRoadID from HRoad')

	file_path = os.path.join(dirpath, 'ecef_roads.txt')
	with open(file_path, 'w') as f:
		f.write('center_x, center_y, center_z, radius\n')
		for row in c.fetchall():
			roadID = str(row[0])
			center, radius = calculate_road_ecef_center(roadID)
			f.write('{},{},{},{},{}\n'.format(roadID, center[0], center[1], center[2], radius))
			
			join_lanes_to_road(roadID)
			replace_parent_with_child(roadID)
			export_road_gltf(roadID, export_path=dirpath)

def calculate_road_ecef_center(roadID):
	# http://www.kurzemnieks.com/goodies_files/hierarchy_helper.py
	road_obj_name = 'Road_' + roadID
	road_obj = bpy.data.objects[road_obj_name]

	sum_x = 0
	sum_y = 0
	sum_z = 0
	cnt = 0
	radius = 0

	# ASSUME all lanes are of equal length in one road - NOT OK. May vary on lane width
	for child in road_obj.children:
		verts = [vert.co for vert in child.data.vertices]
		plain_verts = [vert.to_tuple() for vert in verts]
		for vert in plain_verts:
			sum_x += vert[0]
			sum_y += vert[1]
			sum_z += vert[2]
			cnt += 1

	avg_x = sum_x/cnt
	avg_y = sum_y/cnt
	avg_z = sum_z/cnt

	# calculate bounding sphere radius
	for child in road_obj.children:
		verts = [vert.co for vert in child.data.vertices]
		plain_verts = [vert.to_tuple() for vert in verts]
		for vert in plain_verts:
			d = distance(vert, (avg_x, avg_y, avg_z))
			if d > radius:
				radius = d

	# translate coordinate system, ecef as local origin
	translate_coordinate_ecef_as_origin(avg_x, avg_y, avg_z, roadID)

	return (avg_x, avg_y, avg_z), radius

def distance(vert1, vert2):
	square = (vert1[0] - vert2[0])**2 + (vert1[1] - vert2[1])**2 + (vert1[2] - vert2[2])**2
	return math.sqrt(square)

def deselect_all():
	for selected in bpy.context.selected_objects:
		selected.select = False
	# bpy.ops.object.select_all(action='DESELECT')

def translate_coordinate_ecef_as_origin(avg_x, avg_y, avg_z, roadID):
	"""
	IMPORTANT: originaly the origin is at (0,0,0), but with ecef, parent origin should be at ecef, with ecef's offset deducted from mesh's vertices
	"""
	road_name = 'Road_' + roadID
	parent = bpy.data.objects[road_name]

	for child in parent.children:
		bm = bmesh.new()
		bm.from_mesh(child.data)

		for vert in bm.verts:
			vert.co[0] -= avg_x
			vert.co[1] -= avg_y
			vert.co[2] -= avg_z

		bm.to_mesh(child.data)
		bm.free()

	parent.location = (avg_x, avg_y, avg_z)

def join_lanes_to_road(roadID):
	road_name = 'Road_' + roadID
	road_obj = bpy.data.objects[road_name]

	deselect_all()
	for child in road_obj.children:
		child.select = True
		bpy.context.scene.objects.active = child
	bpy.ops.object.join()

	for child in road_obj.children:
		child.select = False

def replace_parent_with_child(roadID):
	#https://blender.stackexchange.com/questions/27234/python-how-to-completely-remove-an-object
	# cost an appearant period of time
	road_name = 'Road_' + roadID
	road_obj = bpy.data.objects[road_name]

	deselect_all()

	child_obj = None # actuall only one child
	for child in road_obj.children:
		child.select = True
		bpy.context.scene.objects.active = child
		child_obj = child
		bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
		child.select = False

	road_obj.select = True
	bpy.ops.object.delete()

	child_obj.name = road_name

def export_road_gltf(roadID, export_path):
	"""
	Automatically batch export : https://github.com/Takanu/Capsule
	OR move this part into a standalone add-on like Capsule
	"""
	# road_obj now is joined lanes mesh without hierarchy
	deselect_all()
	road_name = 'Road_' + roadID
	road_obj = bpy.data.objects[road_name]

	road_obj.select = True

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
			draw_shp(os.path.join(pathname, filename))

	# draw_lane_not_in_junction(pathname)
	draw_lanes(pathname)

	# calculate_road_ecef_center('5010000001')
	calculate_all_center('/Users/mxmcecilia/Documents/GIS_PCG/project/server/data')

if __name__ == '__main__':
	main()