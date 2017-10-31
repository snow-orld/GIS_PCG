"""
file: EMG_drawRFacility.py

Generate RFacility(道路设施) specified in the EMG specification,
including RFacilityP(道路设施点), RFacilityL(道路设施线), and RFacilityA(道路设施面).

author: Xueman Mou
date: 2017/10/09
version: 1.0.0
modified: 2017/10/09 15:58:30 GMT+800
Compatible with Python versions 3.6
"""

import bpy
import bmesh
import mathutils
import math

# Sign thickness and pole radius
DEPTH = 0.02
# Callbox side lenghth (assume a square crosssection)
SIDE = 0.5

def verts_in_geom(ret):
	return [ele for ele in ret['geom'] if isinstance(ele, bmesh.types.BMVert)]

def generate_pole(bm, height, radius=DEPTH):
	v_b = bmesh.ops.create_circle(bm, cap_ends=False, diameter=radius, segments=32)
	f_b = bm.faces.new(v_b['verts'])
	polet = bmesh.ops.extrude_face_region(bm, geom=[f_b])
	bmesh.ops.translate(bm, vec=(0,0,height), verts=verts_in_geom(polet))

def generate_facility_p(kargs):
	"""
	Generate facilities which are projected to map as a point.

	Each kind (with a set of identical attributes) of the facility
	should already be categorized after parsing through the shapefile.
	
	Each model is modeled at the center origin (better on different layers).

	All five signs are generated as reference 3D models which
	notice artists a rough idea about what signs to model.

	Parameters
	OType:	点状道路设施类型 
			[1:交通标志牌,2:紧急呼叫点,3:电线杆,4:交通信号灯,5:路标架]
	THeight: 点状道路设施最高处距离路面高度(单位：米)
	BHeight: 点状道路设施下边缘距离路面高度(单位：米)
			OType=1 or 4时有效
	TSShape: 交通标志牌形状 
			[1:正等边三角形,2:圆形,3:倒等边三角形,4:八角形,5:叉形,6:方形]
			OType=1 时有效
	ViaSign: 是否为可变信息标志 
			[1:否,2:是] 
			OType=1 时有效
	TWidth:	点状道路设施宽度(单位：米)
			OType=1 or 4时有效
	Diameter: 点状道路设施直径(单位：米)
			OType=3 or5时有效
	"""

	OTYPE = {
		1: 'Sign',
		2: 'EmergencyCallBox',
		3: 'UtilityPole',
		4: 'TrafficLight',
		5: 'Gantry'
	}

	TSSHAPE = {
		1: 'TriangleP',
		2: 'Circle',
		3: 'TriangleN',
		4: 'Octagon',
		5: 'Crossing',
		6: 'Square'
	}

	OType = kargs['OType']
	THeight = kargs['THeight']
	BHeight = kargs['BHeight']
	TSShape = kargs['TSShape']
	ViaSign = kargs['ViaSign']
	TWidth = kargs['TWidth']
	Diameter = kargs['Diameter']

	bm = bmesh.new()
	dataname = 'object'

	if OType == 1:
		# Signs
		dataname = '{}.{}.({}x{}-{})'.format(
					OTYPE[OType],
					TSSHAPE[TSShape],
					TWidth,
					THeight,
					BHeight,
				)
		
		if TSShape == 1:
			# pole
			generate_pole(bm, BHeight)
			
			# sign top
			v_t = bm.verts.new([0, 0, THeight])
			v_l = bm.verts.new([round(-TWidth/2,3), 0, BHeight])
			v_r = bm.verts.new([round(TWidth/2,3), 0, BHeight])

			signf = bm.faces.new([v_t, v_r, v_l])
			bmesh.ops.translate(bm, vec=(0,-DEPTH,0), verts=[v_t, v_l, v_r])
			signb = bmesh.ops.extrude_face_region(bm, geom=[signf])
			bmesh.ops.translate(bm, vec=(0,2*DEPTH,0), verts=verts_in_geom(signb))

		elif TSShape == 2:
			# pole
			generate_pole(bm, BHeight - TWidth)

			# sign top
			v_t = bmesh.ops.create_circle(bm, cap_ends=False, diameter=TWidth * 0.5, segments=32, matrix=mathutils.Matrix.Rotation(math.radians(90), 3, 'X'))
			signf = bm.faces.new(v_t['verts'])
			bmesh.ops.reverse_faces(bm, faces=[signf])
			bmesh.ops.translate(bm, vec=(0,-DEPTH,BHeight-TWidth*0.5), verts=v_t['verts'])
			signb = bmesh.ops.extrude_face_region(bm, geom=[signf])
			bmesh.ops.translate(bm, vec=(0,2*DEPTH,0), verts=verts_in_geom(signb))
		
		elif TSShape == 3:
			# pole
			generate_pole(bm, THeight)

			# sign top
			v_l = bm.verts.new([round(-TWidth/2,3), 0, THeight])
			v_r = bm.verts.new([round(TWidth/2,3), 0, THeight])
			v_b = bm.verts.new([0, 0, BHeight])

			signf = bm.faces.new([v_l, v_r, v_b])
			bmesh.ops.translate(bm, vec=(0,-DEPTH,0), verts=[v_l, v_r, v_b])
			signb = bmesh.ops.extrude_face_region(bm, geom=[signf])
			bmesh.ops.translate(bm, vec=(0,2*DEPTH,0), verts=verts_in_geom(signb))

		elif TSShape == 4:
			# pole
			generate_pole(bm, BHeight)

			# sign top
			side = (THeight-BHeight)*math.tan(math.radians(22.5))
			v_tl = bm.verts.new([round(-side/2,3),0,THeight])
			v_tr = bm.verts.new([round(side/2,3),0,THeight])
			v_ul = bm.verts.new([round(-TWidth/2,3),0,round(THeight-side*math.sin(math.radians(45)),3)])
			v_ur = bm.verts.new([round(TWidth/2,3),0,round(THeight-side*math.sin(math.radians(45)),3)])
			v_ll = bm.verts.new([round(-TWidth/2,3),0,round(BHeight+side*math.sin(math.radians(45)),3)])
			v_lr = bm.verts.new([round(TWidth/2,3),0,round(BHeight+side*math.sin(math.radians(45)),3)])
			v_bl = bm.verts.new([round(-side/2,3),0,BHeight])
			v_br = bm.verts.new([round(side/2,3),0,BHeight])
			signf = bm.faces.new([v_tl, v_tr, v_ur, v_lr, v_br, v_bl, v_ll, v_ul])
			bmesh.ops.translate(bm, vec=(0,-DEPTH,0), verts=[v_tl, v_tr, v_ur, v_lr, v_br, v_bl, v_ll, v_ul])
			signb = bmesh.ops.extrude_face_region(bm, geom=[signf])
			bmesh.ops.translate(bm, vec=(0,2*DEPTH,0), verts=verts_in_geom(signb))

		elif TSShape == 5:
			# Crossing
			crossing_width = 5 * DEPTH
			# pole
			generate_pole(bm, (THeight+BHeight)/2)

			# sign top
			v_ml = bm.verts.new([-crossing_width,0,(THeight+BHeight)/2])
			v_mt = bm.verts.new([0,0,(THeight+BHeight)/2 + crossing_width])
			v_mr = bm.verts.new([crossing_width,0,(THeight+BHeight)/2])
			v_mb = bm.verts.new([0,0,(THeight+BHeight)/2 - crossing_width])
			v_tl_l = bm.verts.new([-TWidth/2,0,THeight-crossing_width])
			v_tl_r = bm.verts.new([-TWidth/2+crossing_width,0,THeight])
			v_tr_l = bm.verts.new([TWidth/2-crossing_width,0,THeight])
			v_tr_r = bm.verts.new([TWidth/2,0,THeight-crossing_width])
			v_bl_l = bm.verts.new([-TWidth/2,0,BHeight+crossing_width])
			v_bl_r = bm.verts.new([-TWidth/2+crossing_width,0,BHeight])
			v_br_l = bm.verts.new([TWidth/2-crossing_width,0,BHeight])
			v_br_r = bm.verts.new([TWidth/2,0,BHeight+crossing_width])
			
			verts = [v_ml, v_tl_l, v_tl_r, v_mt, v_tr_l, v_tr_r, v_mr, v_br_r, v_br_l, v_mb, v_bl_r, v_bl_l]
			signf = bm.faces.new(verts)
			bmesh.ops.translate(bm, vec=(0,-DEPTH,0), verts=verts)
			signb = bmesh.ops.extrude_face_region(bm, geom=[signf])
			bmesh.ops.translate(bm, vec=(0,2*DEPTH,0), verts=verts_in_geom(signb))
 
		elif TSShape == 6:
			# pole
			generate_pole(bm, BHeight)

			# sign top
			v_tl = bm.verts.new([round(-TWidth/2,3),0,THeight])
			v_tr = bm.verts.new([round(TWidth/2,3), 0,THeight])
			v_bl = bm.verts.new([round(-TWidth/2,3),0,BHeight])
			v_br = bm.verts.new([round(TWidth/2,3), 0,BHeight])
			signf = bm.faces.new([v_tl, v_tr, v_br, v_bl])
			bmesh.ops.translate(bm, vec=(0,-DEPTH,0), verts=[v_tl, v_tr, v_bl, v_br])
			signb = bmesh.ops.extrude_face_region(bm, geom=[signf])
			bmesh.ops.translate(bm, vec=(0,2*DEPTH,0), verts=verts_in_geom(signb))

	elif OType == 2:
		# Emergency Call Boxes
		dataname = '{}.({}^2x{})'.format(
					OTYPE[OType],
					SIDE,
					THeight
				)

		v_nw = bm.verts.new([-SIDE/2, SIDE/2, 0])
		v_ne = bm.verts.new([SIDE/2, SIDE/2, 0])
		v_sw = bm.verts.new([-SIDE/2, -SIDE/2, 0])
		v_se = bm.verts.new([SIDE/2, -SIDE/2, 0])

		bottom = bm.faces.new([v_nw, v_sw, v_se, v_ne])
		top = bmesh.ops.extrude_face_region(bm, geom=[bottom])
		bmesh.ops.translate(bm, vec=(0,0,THeight), verts=verts_in_geom(top))

	elif OType == 3:
		# Utility Pole
		dataname = '{}.(D{}x{})'.format(
					OTYPE[OType],
					Diameter,
					THeight
				)

		generate_pole(bm, THeight, Diameter/2)

	elif OType == 4:
		# Traffic Light
		dataname = dataname = '{}.({}x{}-{})'.format(
					OTYPE[OType],
					TWidth,
					THeight,
					BHeight,
				)

		# pole
		generate_pole(bm, BHeight)

		# light box
		v_nw = bm.verts.new([-TWidth/2, TWidth/2, BHeight])
		v_ne = bm.verts.new([TWidth/2, TWidth/2, BHeight])
		v_sw = bm.verts.new([-TWidth/2, -TWidth/2, BHeight])
		v_se = bm.verts.new([TWidth/2, -TWidth/2, BHeight])

		bottom = bm.faces.new([v_nw, v_sw, v_se, v_ne])
		top = bmesh.ops.extrude_face_region(bm, geom=[bottom])
		bmesh.ops.translate(bm, vec=(0,0,THeight-BHeight), verts=verts_in_geom(top))

	elif OType == 5:
		# Gantry
		dataname = '{}.(D{}x{})'.format(
					OTYPE[OType],
					Diameter,
					THeight
				)
		
		bm.free()
		return

	else:
		# invalid OType
		print('Error: Invalid RFacilityP OType %d' % OType)
		bm.free()
		return

	bm.normal_update()
	me = bpy.data.meshes.new(dataname)
	obj = bpy.data.objects.new(dataname, me)
	bpy.context.scene.objects.link(obj)
	bpy.context.scene.objects.active = obj
	obj.select = True

	bm.to_mesh(me)
	bm.free()

def generate_facility_l(verts, record):
	"""
	Parameters
	OType:	线状道路设施类型
			[1:路缘,2:防护栏]
	LPType: 防护栏类型
			[1:水泥墙,2:隧道墙,3:水泥护栏,4:塑料护栏,5:隔音墙,6:金属护栏]
			OType=2时有效
	OLHeight:	线状道路设施高度(单位：米)
				当线状道路设施没有高度时，记录为0
	OLLength:	线状道路设施长度(单位：米)

	Implementation Opts:
	1. 按照传统道路生成方式-用array平铺curb/guardrail
		还是直接生成所有mesh? <-- 采用
	2. 生成的Curb和GuardRail应该以最内侧为line?
	"""

	OTYPE = {
		1: 'Curb',
		2: 'GuardRail',
	}

	LPTYPE = {
		1: 'Wall.Cement',
		2: 'Wall.Tunnel',
		3: 'Rail.Cement',
		4: 'Rail.Plastic',
		5: 'NoiseBarrierWall',
		6: 'Rail.Metal',
	}

	OType = kargs['OType']
	LPType = kargs['LPType']
	OLHeight = kargs['OLHeight']
	OLLength = kargs['OLLength']

	if OType not in OTYPE:
		# invalid OType
		print('Error: Invalid RFacilityL OType %d' % OType)
		return

	bm = bmesh.new()
	dataname = '{}.{}.H{}xL{}'.format(
				OTYPE[OType],
				'' if OType == 1 else LPTYPE[LPType],
				OLHeight,
				OLLength,
			)

	# Find Normal Direction (along the line going forward)
	for vert in verts:
		bm.verts.new(vert.co)

	bm.normal_update()
	me = bpy.data.meshes.new(dataname)
	obj = bpy.data.objects.new(dataname, me)
	bpy.context.scene.objects.link(obj)
	bpy.context.scene.objects.active = obj
	obj.select = True

	bm.to_mesh(me)
	bm.free()

def generate_facility_a(me, record):
	"""
	Parameters
	me: mesh data representing a set of polygons of a shape
	record:
		OType:	面状道路设施类型
				[1:绿化隔离带,2:特殊结构,3:收费站,4:过街天桥]
		OHeight: 面状道路设施高度
				 当面状道路设施没有高度时，记录为0

	Challenge:
	After extruded face to the desired height, keep or delete the original face?
	"""

	OTYPE = {
		1: 'MedianStrip',
		2: 'SpecialStructure',
		3: 'Toll',
		4: 'Skyway'
	}

	OType = record[3]
	OHeight = record[4]

	if OType not in OTYPE:
		# invalid OType
		print('Error: Invalid RFacilityA OType %d' % OType)
		return

	if OHeight > 0:
		bm = bmesh.new()
		dataname = '{}.H{}'.format(OTYPE[OType], OHeight)

		bm.from_mesh(me)
		top = bmesh.ops.extrude_face_region(bm, geom=bm.faces)
		bmesh.ops.translate(bm, vec=(0,0,1), verts=verts_in_geom(top))

		bm.normal_update()
		me = bpy.data.meshes.new(dataname)
		obj = bpy.data.objects.new(dataname, me)
		bpy.context.scene.objects.link(obj)
		bpy.context.scene.objects.active = obj
		obj.select = True

		bm.to_mesh(me)
		bm.free()

if __name__ == '__main__':
	kargs = {}
	kargs['OType'] = 5
	kargs['THeight'] = 7.4
	kargs['BHeight'] = 2.3
	kargs['TSShape'] = 5
	kargs['ViaSign'] = 1
	kargs['TWidth'] = 0.8
	kargs['Diameter'] = 0.35
	# generate_facility_p(kargs)

	me = bpy.data.meshes['Circle']
	record = [5010000013, 0, 440100, 1, 1.5, '5010000023-5010000007-5010001333']
	# record = [5010000065, 0, 440100, 2, 4.5, '5010001302']
	# record = [5010000003, 0, 440100, 3, 4.5, '5010000021-5010000020-5010001303']
	generate_facility_a(me, record)