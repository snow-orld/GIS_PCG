import bpy
import bmesh
import os
import sys
import shapefile
import pyproj

# proj parameters
wgs84 = pyproj.Proj(init='epsg:4326') # longlat
ecef = pyproj.Proj(init='epsg:4978') # geocentric

# center of drawing as first shapefile's center
center = None

def ls(folder):
	shapefiles = []
	for dirpath, dirnames, filenames in os.walk(folder):
		for filename in filenames:
			if filename.endswith('.shp'):
				shapefiles.append(filename)

	return shapefiles

def draw_shp(shpname):
	sf = shapefile.Reader(shpname)

	print('Type %s' % sf.shapeType)
	print('ShapeRecords num #%d' % len(sf.shapeRecords()))

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

		print('\nShape#%d %d parts, %d points, record: %s' % (srindex, len(shape.parts), len(shape.points), record))

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

if __name__ == '__main__':
	
	pathname = 'D:\Documents\GIS\data\EMG_sample_data\EMG_GZ'
	# pathname = os.path.join(pathname, 'LMarking.shp')

	if os.path.isfile(pathname):
		if os.path.exists(pathname):
			print('Drawing %s ...' % pathname)
			draw_shp(pathname)
	else:
		shapefiles = ls(pathname)

		# print('%d shapefiles' % len(shapefiles))
		
		for index, filename in enumerate(shapefiles):
			print('Drawing %s ...' % filename)
			draw_shp(os.path.join(pathname, filename))
