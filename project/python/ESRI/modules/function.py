"""
file: function.py

common functions used in oo drawing

author: Xueman Mou
date: 2018/5/28
version: 1.0.1
modified: 2018/6/1 08:53:00 GMT +0800

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

def expandDoubleECEF(array_co, array_width):
	# return the border points in ccw order
	# input array_co: array of [x, y, z] in ECEF
	# input width: width at each centered point
	left_part_cos_left = []
	left_part_cos_right = []
	right_part_cos_left = []
	right_part_cos_right = []

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
			start_co = Vector(transform((shape.points[0][0], shape.points[0][1], shape.z[0])))
			end_co = Vector(transform((shape.points[1][0], shape.points[1][1], shape.z[1])))
			coordinates = [start_co]
			widths = [record[6]]
			pindex = 1
			while pindex < len(shape.points):
				if distance(start_co, end_co) > length_to_go:
					print('Interpolated between two points isLine=%s length_to_go=%f' % (isLine, length_to_go))
					# find an intermediate point to cover 'length_to_go'
					direction_vector = end_co - start_co
					direction_vector.normalize()
					inter_co = direction_vector * length_to_go + start_co
					start_co = inter_co
					length_to_go = 0
					if isLine:
						coordinates.append(inter_co)
						widths.append(record[6])
				else:
					length_to_go -= distance(end_co, start_co)
					print('isLine=%s length_to_go=%f' % (isLine, length_to_go))
					if isLine:
						coordinates.append(end_co)
						widths.append(record[6])
					pindex += 1
					if pindex < len(shape.points) - 1:
						start_co = end_co	
						end_co = Vector(transform((shape.points[pindex][0], shape.points[pindex][1], shape.z[pindex])))
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

		coordinates = []
		widths = []

		for pindex, point in enumerate(shape.points):
			coordinates.append((point[0], point[1], shape.z[pindex]))
			# curbs cannot use expand here
			widths.append(0.2)

		coordinates_in_face = expand(coordinates, widths)

		bm = bmesh.new()
		verts_in_face = []
		for co in coordinates_in_face:
			vert = bm.verts.new(co)
			verts_in_face.append(vert)
		face = bm.faces.new(verts_in_face)

		dataname = 'LObject_' + str(record[0])
		me = bpy.data.meshes.new(dataname)
		file_obj = bpy.data.objects.new(dataname, me)
		bpy.context.scene.objects.link(file_obj)
		file_obj.parent = RFacilityL_obj

		bm.to_mesh(me)
		bm.free()

def main():
	pathname = '/Users/mxmcecilia/Documents/GIS_PCG/data/EMG_sample_data/EMG_GZ'
	# showLanes(pathname)
	showLMarkings(pathname)
	# showRFacilityL(pathname)
	

if __name__ == '__main__':
	main()