"""
file: function.py

common functions used in oo drawing

author: Xueman Mou
date: 2018/5/28
version: 1.0.1
modified: 2018/6/8 16:59:00 GMT +0800

developing env: python 3.5.2
dependencies: pyproj, mathutils.Vector, bpy

"""

from mathutils import Vector

import pyproj, shapefile
import os, sqlite3, math
import bpy, bmesh

# proj parameters
WGS84 = pyproj.Proj(init='epsg:4326') # longlat
ECEF = pyproj.Proj(init='epsg:4978') # geocentric

center = None
DB = '/Users/mxmcecilia/Documents/GIS_PCG/project/python/ESRI/EMG_GZ.db'

def distance(co1, co2):
	return math.sqrt(math.pow(co2[0] - co1[0], 2) + math.pow(co2[1] - co1[1], 2) + math.pow(co2[2] - co1[2], 2))

def move2Center(co, center):
	# re-center co by center
	return [x - x0 for x, x0 in zip(co, center)]

def transform(co):
	# get ecef coordinates of wgs84 co
	return pyproj.transform(WGS84, ECEF, co[0], co[1], co[2])

def cross(co1, co2):
	# cross product of tuple/array co1 x co2
	return (co1[1]*co2[2] - co2[1]*co1[2],
			co2[0]*co1[2] - co1[0]*co2[2],
			co1[0]*co2[1] - co2[0]*co1[1])

def dot(co1, co2):
	# dot product of tuple/array co1 . co2
	return co1[0]*co2[0] + co1[1]*co2[1] + co1[2]*co2[2]

def add(co1, co2):
	# sum tuple/array vector co1, co2
	return (co1[0] + co2[0], co1[1] + co2[1], co1[2] + co2[2])

def minus(co1, co2):
	# co1 - co2 of tuple/array vector
	return (co1[0] - co2[0], co1[1] - co2[1], co1[2] - co2[2])

def expand(array_co, array_width):
	# return the border points in ccw order
	# input array_co: array of [lon, lat, alt] in wgs84
	# input width: width at each centered point
	cos_left = []
	cos_right = []

	for index, (co, width) in enumerate(zip(array_co, array_width)):
		co = transform(co)
		up = Vector(co)
		up.normalize()
		co = move2Center(co, center)

		forward = None
		if index < len(array_co) - 1:
			co_next = array_co[index + 1]
			co_next = transform(co_next)
			co_next = move2Center(co_next, center)
			forward = [x - y for x, y in zip(co_next, co)]
			forward = Vector(forward)
			forward.normalize()
		else:
			co_prev = array_co[index - 1]
			co_prev = transform(co_prev)
			co_prev = move2Center(co_prev, center)
			forward = [x - y for x, y in zip(co, co_prev)]
			forward = Vector(forward)
			forward.normalize()

		left = up.cross(forward)
		left.normalize()

		co = Vector(co)

		co1 = co + width * left / 2
		co2 = co + (-width) * left / 2

		cos_left.append(co1)
		cos_right.append(co2)

	cos_left.reverse()
	cos_in_face = cos_left + cos_right
	
	return cos_in_face

def expandDouble(array_co, array_width, in_between_width=0.15):

	left_part_cos_left = []
	left_part_cos_right = []
	right_part_cos_left = []
	right_part_cos_right = []

	for index, (co, width) in enumerate(zip(array_co, array_width)):
		co = transform(co)
		up = Vector(co)
		up.normalize()
		co = move2Center(co, center)

		forward = None
		if index < len(array_co) - 1:
			co_next = array_co[index + 1]
			co_next = transform(co_next)
			co_next = move2Center(co_next, center)
			forward = [x - y for x, y in zip(co_next, co)]
			forward = Vector(forward)
			forward.normalize()
		else:
			co_prev = array_co[index - 1]
			co_prev = transform(co_prev)
			co_prev = move2Center(co_prev, center)
			forward = [x - y for x, y in zip(co, co_prev)]
			forward = Vector(forward)
			forward.normalize()

		left = up.cross(forward)
		left.normalize()

		co = Vector(co)
		co_ll = co + (in_between_width / 2 + width) * left
		co_lr = co + (in_between_width / 2) * left
		co_rl = co + (-in_between_width / 2) * left
		co_rr = co + (-in_between_width / 2 - width) * left
	
		left_part_cos_left.append(co_ll)
		left_part_cos_right.append(co_lr)
		right_part_cos_left.append(co_rl)
		right_part_cos_right.append(co_rr)
	
	left_part_cos_left.reverse()
	right_part_cos_left.reverse()

	return left_part_cos_left + left_part_cos_right, right_part_cos_left + right_part_cos_right

def expandECEF(array_co, array_width):
	# return the border points in ccw order
	# input array_co: array of [x, y, z] in ECEF
	# input width: width at each centered point
	cos_left = []
	cos_right = []

	for index, (co, width) in enumerate(zip(array_co, array_width)):
		up = Vector(co)
		up.normalize
		co = move2Center(co, center)

		forward = None
		if index < len(array_co) - 1:
			co_next = array_co[index + 1]
			co_next = move2Center(co_next, center)
			forward = [x - y for x, y in zip(co_next, co)]
			forward = Vector(forward)
			forward.normalize()
		else:
			co_prev = array_co[index - 1]
			co_prev = move2Center(co_prev, center)
			forward = [x - y for x, y in zip(co, co_prev)]
			forward = Vector(forward)
			forward.normalize()

		left = up.cross(forward)
		left.normalize()

		co = Vector(co)

		co1 = co + width * left / 2
		co2 = co + (-width) * left / 2

		cos_left.append(co1)
		cos_right.append(co2)

	cos_left.reverse()
	cos_in_face = cos_left + cos_right
	
	return cos_in_face

def showLanes(pathname):
	sf = shapefile.Reader(os.path.join(pathname, 'HLane.shp'))

	# recenter bbox 
	global center
	if center == None:
		lon_0 = sum(sf.bbox[0::2]) * 0.5
		lat_0 = sum(sf.bbox[1::2]) * 0.5
		center = transform((lon_0, lat_0) + (0,))

	conn = sqlite3.connect(DB)
	c = conn.cursor()
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

		coordinates = []
		widths = []

		c.execute('''SELECT * FROM HLaneNode WHERE HLNodeID = ?''', (record[4],))
		result = c.fetchone()
		coordinates.append((shape.points[0][0], shape.points[0][1], shape.z[0]))
		widths.append(result[8])

		# inner shape nodes, width in HLaneInfo
		c.execute('''SELECT * FROM HLaneInfo WHERE HLaneID = ?''', (record[0],))
		result = c.fetchall()
		for zindex, (point, row) in enumerate(zip(shape.points[1:-1], result)):
			width = row[9]
			coordinates.append((point[0], point[1], shape.z[zindex + 1]))
			widths.append(width)

		# last lane node, width in HLaneNode
		c.execute('''SELECT * FROM HLaneNode WHERE HLNodeID = ?''', (record[5],))
		result = c.fetchone()
		coordinates.append((shape.points[-1][0], shape.points[-1][1], shape.z[-1]))
		widths.append(result[8])

		coordinates_in_face = expand(coordinates, widths)

		bm = bmesh.new()
		verts_in_face = []
		for co in coordinates_in_face:
			vert = bm.verts.new(co)
			verts_in_face.append(vert)
		face = bm.faces.new(verts_in_face)

		dataname = str(record[0])
		me = bpy.data.meshes.new(dataname)
		file_obj = bpy.data.objects.new(dataname, me)
		bpy.context.scene.objects.link(file_obj)
		file_obj.parent = road_obj

		bm.to_mesh(me)
		bm.free()

def showLMarkings(pathname):
	"""
	Problem:
		1.虚线涉及到对中心线的重采样，保证虚线是等间隔分布
		2.双线时确定两条线间隔 (10-30) http://www.360doc.com/content/14/1221/10/116554_434544846.shtml
		3.虚实线时确定哪侧为虚哪侧为实
	"""
	sf = shapefile.Reader(os.path.join(pathname, 'LMarking.shp'))

	# recenter bbox 
	global center
	if center == None:
		lon_0 = sum(sf.bbox[0::2]) * 0.5
		lat_0 = sum(sf.bbox[1::2]) * 0.5
		center = transform((lon_0, lat_0) + (0,))

	LMarking_obj_name = 'LMarking'
	LMarking_obj = None
	if bpy.data.objects.find(LMarking_obj_name) == -1:
		LMarking_obj = bpy.data.objects.new(LMarking_obj_name, None)
		bpy.context.scene.objects.link(LMarking_obj)
	else:
		LMarking_obj = bpy.data.objects[LMarking_obj_name]

	for index, sr in enumerate(sf.shapeRecords()):
		shape = sr.shape
		record = sr.record

		coordinates = []
		widths = []

		# see what type of lane form the L Marking is
		bm = bmesh.new()
		form = record[5]
		if form == 1 or form == 3:
			# 单实线
			coordinates = []
			widths = []
			for pindex, point in enumerate(shape.points):
				coordinates.append((point[0], point[1], shape.z[pindex]))
				widths.append(record[6])
			coordinates_in_face = expand(coordinates, widths)
			verts_in_face = []
			for co in coordinates_in_face:
				vert = bm.verts.new(co)
				verts_in_face.append(vert)
			face = bm.faces.new(verts_in_face)
		elif form == 2 or form == 4 or form == 5:
			# 双实线
			coordinates = []
			widths = []
			for pindex, point in enumerate(shape.points):
				coordinates.append((point[0], point[1], shape.z[pindex]))
				widths.append(record[6])
			cos_left, cos_right = expandDouble(coordinates, widths)
			verts_in_face_left = []
			verts_in_face_right = []
			
			for co in cos_left:
				vert = bm.verts.new(co)
				verts_in_face_left.append(vert)
			face = bm.faces.new(verts_in_face_left)
			for co in cos_right:
				vert = bm.verts.new(co)
				verts_in_face_right.append(vert)
			face = bm.faces.new(verts_in_face_right)
		elif form == 3:
			# 单虚线 - 需要计算相对长度，所以在expand前就需要坐标转换，所以不能使用expand
			# if record[0] != 5010001545:
			# 	continue
			isLine = True
			length_to_go = 6
			start_co = transform((shape.points[0][0], shape.points[0][1], shape.z[0]))
			end_co = transform((shape.points[1][0], shape.points[1][1], shape.z[1]))
			coordinates = [start_co]
			widths = [record[6]]
			pindex = 1
			while pindex < len(shape.points):
				if distance(start_co, end_co) > length_to_go:
					print(start_co, end_co)
					print('Interpolated between two points length_to_go=%f' % length_to_go)
					# find an intermediate point to cover 'length_to_go'
					direction_vector = minus(end_co, start_co)
					direction_vector_norm = distance((0,0,0), direction_vector)
					direction_vector = [x / direction_vector_norm for x in direction_vector]
					inter_co = [x * length_to_go + x0 for x, x0 in zip(direction_vector, start_co)]
					start_co = inter_co
					length_to_go = 0
					if isLine:
						coordinates.append(inter_co)
						widths.append(record[6])
				else:
					length_to_go -= distance(end_co, start_co)
					print('length_to_go=%f' % length_to_go)
					if isLine:
						coordinates.append(end_co)
						widths.append(record[6])
					pindex += 1
					if pindex < len(shape.points) - 1:
						start_co = end_co	
						end_co = transform((shape.points[pindex][0], shape.points[pindex][1], shape.z[pindex]))
					else:
						length_to_go = 0

				if math.fabs(length_to_go - 0) < 1E-05:
					if isLine:
						verts_in_face = []
						cos = expandECEF(coordinates, widths)
						for co in cos:
							vert = bm.verts.new(co)
							verts_in_face.append(vert)
						face = bm.faces.new(verts_in_face)

					isLine = False if isLine is True else True
					length_to_go = 6 if isLine is True else 9
					coordinates = [start_co]
					widths = [record[6]]

		elif form == 4:
			# 双虚线
			pass
		elif form == 5:
			# 虚实线
			pass

		dataname = 'LMID_' + str(record[0])
		me = bpy.data.meshes.new(dataname)
		file_obj = bpy.data.objects.new(dataname, me)
		bpy.context.scene.objects.link(file_obj)
		file_obj.parent = LMarking_obj

		# color with material
		mat = bpy.data.materials.new('line_color')
		if record[4] == 1:
			mat.diffuse_color = (1.0, 1.0, 1.0)
		elif record[4] == 2:
			mat.diffuse_color = (1.0, 1.0, 0.0)
		file_obj.active_material = mat

		bm.to_mesh(me)
		bm.free()

def showRFacilityL(pathname):
	sf = shapefile.Reader(os.path.join(pathname, 'RFacilityL.shp'))

	# recenter bbox 
	global center
	if center == None:
		lon_0 = sum(sf.bbox[0::2]) * 0.5
		lat_0 = sum(sf.bbox[1::2]) * 0.5
		center = transform((lon_0, lat_0) + (0,))

	RFacilityL_obj_name = 'RFacilityL'
	RFacilityL_obj = None
	if bpy.data.objects.find(RFacilityL_obj_name) == -1:
		RFacilityL_obj = bpy.data.objects.new(RFacilityL_obj_name, None)
		bpy.context.scene.objects.link(RFacilityL_obj)
	else:
		RFacilityL_obj = bpy.data.objects[RFacilityL_obj_name]

	for index, sr in enumerate(sf.shapeRecords()):
		shape = sr.shape
		record = sr.record

		OType = record[3]
		LPType = record[4]
		height = record[5]
		roadID = record[7]

		# if len(roadID.split('-')) == 1:
		# 	continue
		# else:
		# 	print(roadID.split('-'))

		# needs to find out which side this barrier on the road is

		cos_upper = []
		cos_lower = []

		cos_lower_l = []
		cos_upper_l = []
		
		for pindex, point in enumerate(shape.points):
			plower = transform((point[0], point[1], shape.z[pindex]))
			up = plower
			up_norm = distance((0,0,0), up)
			up = [x / up_norm for x in up]

			pupper = [x * height + x0 for x, x0 in zip(up, plower)]
			pupper = move2Center(pupper, center)
			plower = move2Center(plower, center)

			forward = None
			if pindex == len(shape.points) - 1:
				p_prev = transform((shape.points[pindex - 1][0], shape.points[pindex - 1][1], shape.z[pindex - 1]))
				forward = minus(plower, p_prev)
				pass
			else:
				p_next = transform((shape.points[pindex + 1][0], shape.points[pindex + 1][1], shape.z[pindex + 1]))
				forward = minus(p_next, plower)
				pass

			forward_norm = distance((0,0,0), forward)
			forward = [x / forward_norm for x in forward]

			left = cross(up, forward)
			left_norm = distance((0,0,0), left)
			left = [x / left_norm for x in left]

			plower_left = [x * 0.5 + x0 for x, x0 in zip(left, plower)]
			pupper_left = [x * 0.5 + x0 for x, x0 in zip(left, pupper)]

			cos_lower.append(plower)
			cos_upper.append(pupper)

			cos_lower_l.append(plower_left)
			cos_upper_l.append(pupper_left)

		# cos_upper.reverse()
		# coordinates_in_face = cos_upper + cos_lower

		bm = bmesh.new()
		# verts_in_face = []
		# for co in coordinates_in_face:
		# 	vert = bm.verts.new(co)
		# 	verts_in_face.append(vert)
		# # face = bm.faces.new(verts_in_face)

		# vertical curbs or walls may not perfectly sit in one plane, thus using n-polygon generation may cause unexpected shape
		for index, (co_up, co_low) in enumerate(zip(cos_upper, cos_lower)):
			if index == len(cos_upper) - 1:
				break
			verts_in_face = []
			cos_in_face = []
			cos_in_face.append(cos_upper[index + 1])
			cos_in_face.append(co_up)
			cos_in_face.append(co_low)
			cos_in_face.append(cos_lower[index + 1])
			for co in cos_in_face:
				vert = bm.verts.new(co)
				if index < 2:
					vert.select = True
				verts_in_face.append(vert)
			face = bm.faces.new(verts_in_face)

			verts_in_face = []
			cos_in_face = []
			cos_in_face.append(co_up)
			cos_in_face.append(cos_upper[index + 1])
			cos_in_face.append(cos_upper_l[index + 1])
			cos_in_face.append(cos_upper_l[index])
			for co in cos_in_face:
				vert = bm.verts.new(co)
				if index < 2:
					vert.select = True
				verts_in_face.append(vert)
			# face = bm.faces.new(verts_in_face)

			verts_in_face = []
			cos_in_face = []
			cos_in_face.append(cos_upper_l[index])
			cos_in_face.append(cos_upper_l[index + 1])
			cos_in_face.append(cos_lower_l[index + 1])
			cos_in_face.append(cos_lower_l[index])
			for co in cos_in_face:
				vert = bm.verts.new(co)
				if index < 2:
					vert.select = True
				verts_in_face.append(vert)
			# face = bm.faces.new(verts_in_face)

		# for index, co in enumerate(cos_lower_l):
		# 	if index < len(cos_lower_l) - 1:
		# 		vert = bm.verts.new(co)
		# 		vert2 = bm.verts.new(cos_lower_l[index + 1])
		# 		bm.edges.new([vert, vert2])

		# for index, co in enumerate(cos_upper_l):
		# 	if index < len(cos_upper_l) - 1:
		# 		vert = bm.verts.new(co)
		# 		vert2 = bm.verts.new(cos_upper_l[index + 1])
		# 		bm.edges.new([vert, vert2])

		# for index, co in enumerate(cos_lower):
		# 	if index < len(cos_lower) - 1:
		# 		vert1 = bm.verts.new(co)
		# 		vert2 = bm.verts.new(cos_lower[index + 1])
		# 		edge = bm.edges.new([vert1, vert2])
		# for index, co in enumerate(cos_upper):
		# 	if index < len(cos_upper) - 1:
		# 		vert1 = bm.verts.new(co)
		# 		vert2 = bm.verts.new(cos_upper[index + 1])
		# 		edge = bm.edges.new([vert1, vert2])

		dataname = 'LObject_' + str(record[0])
		me = bpy.data.meshes.new(dataname)
		file_obj = bpy.data.objects.new(dataname, me)
		bpy.context.scene.objects.link(file_obj)
		file_obj.parent = RFacilityL_obj

		bm.to_mesh(me)
		bm.free()

def fill_between_two_lines(lineobj1, lineobj2):
	verts1 = []
	verts2 = []

	bm = bmesh.new()
	bm.from_mesh(lineobj1)

	for v in bm.verts:
		verts1.append(v)

	bm.free()
	bm.from_mesh(lineobj2)
	for v in bm.verts:
		verts2.append(v)
	bm.free()

	bm = bmesh.new()
	face = bm.faces.new(verts1 + verts2)
	
	me = bpy.data.meshes.new('surface')
	obj= bpy.data.objects.new('surface', me)
	bpy.context.scene.objects.link(obj)
	bm.to_mesh(me)
	bm.free()

def main():
	pathname = '/Users/mxmcecilia/Documents/GIS_PCG/data/EMG_sample_data/EMG_GZ'
	# showLanes(pathname)
	showLMarkings(pathname)
	showRFacilityL(pathname)
	
if __name__ == '__main__':
	main()