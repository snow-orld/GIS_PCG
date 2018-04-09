"""
file: junction_test.py

only for testing closed surface as junction. Data is artifically made up instead of
extracting from a formal ESRI database.

author: Xueman Mou
date: 2018/4/3
version: 1.0.1
modified: 2018/4/3 016:111:00 +0800

developing env: python 3.5.2
dependencies: bpy, bmesh, mathutils
"""

import bpy
import bmesh
from mathutils import Vector

class HLane():
	def __init__(self, HLaneID, SeqNum, SHLNodeID, EHLNodeID, LHRoadID):
		self.HLaneID = HLaneID
		self.SeqNum = SeqNum
		self.SHLNodeID = SHLNodeID
		self.EHLNodeID = EHLNodeID
		self.LHRoadID = LHRoadID

class HLaneInfo():
	def __init__(self, HLaneID, x, y, z, Width):
		self.HLaneID = HLaneID
		self.x = x
		self.y = y
		self.z = z
		self.width = Width

class HLaneNode():
	def __init__(self, HLNodeID, x, y, z, HLWidth):
		self.HLNodeID = HLNodeID
		self.x = x
		self.y = y
		self.z = z
		self.width = HLWidth

class HRoad():
	def __init__(self, HRoadID, SHNodeID, EHNodeID, InnerCJ, LCJID):
		self.HRoadID = HRoadID
		self.SHNodeID = SHNodeID
		self.EHNodeID = EHNodeID
		self.InnerCJ = InnerCJ
		self.LCJID = LCJID

class ComplexJunction():
	def __init__(self, CJID, CJType):
		self.CJID = CJID
		self.CJType = CJType

class junction():
	def __init__(self, CJID, roads):
		self.CJID = CJID
		self.roads = roads
class road():
	def __init__(self, roadID, lanes, CJID):
		self.roadID = roadID
		self.lanes = lanes
		self.CJID = CJID
class lane():
	def __init__(self, laneID, start, end, shape, roadID):
		self.laneID = laneID
		self.start = start
		self.end = end
		self.shape = shape
		self.roadID  = roadID
	def contains(self, x, y):
		points = [start,] + self.shape + [end,]

		verts_left = []
		verts_right = []
		for index, point in enumerate(points):
			forward = None
			if index < len(points) - 1:
				co_next = points[index + 1]
				forward = [x - y for x, y in zip(co_next, point)]
				forward = Vector(forward)
				forward.normalize()
			else:
				co_prev = points[index - 1]
				forward = [x - y for x, y in zip(point, co_prev)]
				forward = Vector(forward)
				forward.normalize()
			up = Vector(point)
			up.normalize()
			left = up.cross(forward)
			left.normalize()
			width = 4.0
			vert1 = left * width / 2 + point
			vert2 = -left * width / 2 + point

			verts_left.append(vert1)
			verts_right.append(vert2)

			# Point in Polygon algorithm
			point_in_polygon(testPoint, polyPoints)

		return False

class Point():
	def __init__(self, x, y, z):
		self.x = x
		self.y = y
		self.z = z

class LineSegment():
	def __init__(self, p1, p2):
		self.p1 = p1
		self.p2 = p2

def point_in_polygon():
	pass

def create_roads(num_roads):
	# generate a four-road two-way crossing or five-road two-way crossing
	if num_roads == 4:

		bm = bmesh.new()

		# Lanes before entering junction
		verts_in_face = []
		verts_in_face.append(bm.verts.new((-20, -4, 0)))
		verts_in_face.append(bm.verts.new((-10, -4, 0)))
		verts_in_face.append(bm.verts.new((-10,  0, 0)))
		verts_in_face.append(bm.verts.new((-20,  0, 0)))
		bm.faces.new(verts_in_face)

		verts_in_face = []
		verts_in_face.append(bm.verts.new((-20,  0, 0)))
		verts_in_face.append(bm.verts.new((-10,  0, 0)))
		verts_in_face.append(bm.verts.new((-10,  4, 0)))
		verts_in_face.append(bm.verts.new((-20,  4, 0)))
		bm.faces.new(verts_in_face)

		verts_in_face = []
		verts_in_face.append(bm.verts.new(( -4,  10, 0)))
		verts_in_face.append(bm.verts.new((  0,  10, 0)))
		verts_in_face.append(bm.verts.new((  0,  20, 0)))
		verts_in_face.append(bm.verts.new(( -4,  20, 0)))
		bm.faces.new(verts_in_face)

		verts_in_face = []
		verts_in_face.append(bm.verts.new((  0,  10, 0)))
		verts_in_face.append(bm.verts.new((  4,  10, 0)))
		verts_in_face.append(bm.verts.new((  4,  20, 0)))
		verts_in_face.append(bm.verts.new((  0,  20, 0)))
		bm.faces.new(verts_in_face)

		verts_in_face = []
		verts_in_face.append(bm.verts.new((  10,  0, 0)))
		verts_in_face.append(bm.verts.new((  20,  0, 0)))
		verts_in_face.append(bm.verts.new((  20,  4, 0)))
		verts_in_face.append(bm.verts.new((  10,  4, 0)))
		bm.faces.new(verts_in_face)

		verts_in_face = []
		verts_in_face.append(bm.verts.new((  10, -4, 0)))
		verts_in_face.append(bm.verts.new((  20, -4, 0)))
		verts_in_face.append(bm.verts.new((  20,  0, 0)))
		verts_in_face.append(bm.verts.new((  10,  0, 0)))
		bm.faces.new(verts_in_face)

		verts_in_face = []
		verts_in_face.append(bm.verts.new((  -4, -10, 0)))
		verts_in_face.append(bm.verts.new((  -4, -20, 0)))
		verts_in_face.append(bm.verts.new((   0, -20, 0)))
		verts_in_face.append(bm.verts.new((   0, -10, 0)))
		bm.faces.new(verts_in_face)

		verts_in_face = []
		verts_in_face.append(bm.verts.new((   0, -10, 0)))
		verts_in_face.append(bm.verts.new((   0, -20, 0)))
		verts_in_face.append(bm.verts.new((   4, -20, 0)))
		verts_in_face.append(bm.verts.new((   4, -10, 0)))
		bm.faces.new(verts_in_face)
		# end lanes entering junctions

		# junction outside boundary
		verts_in_face = []
		verts_in_face.append(bm.verts.new(( -4, -10, 0)))
		verts_in_face.append(bm.verts.new((  4, -10, 0)))
		verts_in_face.append(bm.verts.new(( 10,  -4, 0)))
		verts_in_face.append(bm.verts.new(( 10,   4, 0)))
		verts_in_face.append(bm.verts.new((  4,  10, 0)))
		verts_in_face.append(bm.verts.new(( -4,  10, 0)))
		verts_in_face.append(bm.verts.new((-10,   4, 0)))
		verts_in_face.append(bm.verts.new((-10,  -4, 0)))
		bm.faces.new(verts_in_face)
		# end of junction outside boundary

		me = bpy.data.meshes.new('Lanes')
		obj = bpy.data.objects.new('Lanes', me)
		bpy.context.scene.objects.link(obj)

		bm.to_mesh(me)
		bm.free()

	elif num_roads == 5:
		pass

def generate_junction_surface():
	pass

def get_bbox(positions):
	x_min = min(pos[0] for pos in positions)
	x_max = max(pos[0] for pos in positions)
	y_min = min(pos[1] for pos in positions)
	y_max = max(pos[1] for pos in positions)
	return x_min, y_min, x_max, y_max

def sample():
	resolution = 0.1 # 10 cm
	xmin, ymin, xmax, ymax = get_bbox([(-10,-4,0), (-10, 4,0), (-4, 10,0), (4,10,0), (10,4,0), (10,-4,0), (4, -10,0), (-4,-10,0)])
	epsi = 0.0001
	xindex = 0

	bm = bmesh.new()
	while (xindex * 0.1 + xmin < xmax + epsi):
		yindex = 0
		while (yindex * 0.1 + ymin < ymax + epsi):
			x = xindex * 0.1 + xmin
			y = yindex * 0.1 + ymin
			yindex += 1
			testPoint = Point(x, y, 0)
			polygon = []
			polygon.append(Point(-10,0,0))
			polygon.append(Point( 0,10,0))
			polygon.append(Point(10,0,0))
			polygon.append(Point(0,-10,0))
			if isInPolygon(testPoint, polygon, 4):
				# pixel (x,y) = 0
				bm.verts.new((x,y,0))
			else:
				# pixel (x,y) = 255
				print('is outside polygon')
		xindex += 1


def is_in_junction(x, y):
	# go through each cross section, see if it is within all normals of cross section of roads in junction
	
	return False

def ccw(p0, p1, p2):
	dx1 = p1.x - p0.x
	dy1 = p1.y - p0.y
	dx2 = p2.x - p0.x
	dy2 = p2.y - p0.y

	# second slope is greater than the first one --> counter-clockwise
	if dx1 * dy2 > dx2 * dy1:
		return 1
	# first slope is greater than the second one --> clockwise
	elif dx1 * dy2 < dx2 * dy1:
		return -1
	# both slopes are equal --> colinear line segments
	else:
		# p0 is between p1 and p2
		if (dx1 * dx2 < 0 or dy1 * dy2 < 0):
			return -1
		# p2 is between p0 and p1, as the length is compared
		# square roots are avoided to increase performance
		elif dx1*dx1 + dy1*dy1 >= dx2*dx2 + dy2*dy2:
			return 0
		# p1 is between p0 and p2
		else:
			return 1

def intersect(line1, line2):
	# ccw returns 0 if two points are identical, except from the situation
	# when p0 and p1 are identical and different from p2
	ccw11 = ccw(line1.p1, line1.p2, line2.p1)
	ccw12 = ccw(line1.p1, line1.p2, line2.p2)
	ccw21 = ccw(line2.p1, line2.p2, line1.p1)
	ccw22 = ccw(line2.p1, line2.p2, line2.p2)

	return 1 if (((ccw11 * ccw12 < 0) and (ccw21 * ccw22 < 0))
		# once ccw is zero to detect an intersection
		or (ccw11 * ccw12 * ccw21 * ccw22 == 0)) else 0

def getNextIndex(n, current):
	return 0 if current == n - 1 else current + 1;

def isInPolygon(testPoint, polygon, n):
	startPoint = Point(0, 0, 0)

	xAxis = LineSegment(Point(0,0,0), Point(0,0,0))
	xAxisPositive = LineSegment(Point(0,0,0), Point(0,0,0))

	startNodePosition = -1

	# Is testPoint on a node?
	# Move polygon to 0|0
	# Enlarge axes
	for i in range(n):
		if(testPoint.x == polygon[i].x and testPoint.y == polygon[i].y):
			return 1

		# move polygon to 0|0
		polygon[i].x -= testPoint.x
		polygon[i].y -= testPoint.y

		# Find start point which is not on the x axis
		if polygon[i].y !=0:
			startPoint.x = polygon[i].x
			startPoint.y = polygon[i].y
			startNodePosition = i

		# enlarge axes
		if (polygon[i].x > xAxis.p2.x):
			xAxis.p2.x = polygon[i].x
			xAxisPositive.p2.x = polygon[i].x
		if polygon[i].x < xAxis.p1.x:
			xAxis.p1.x = polygon[i].x

	# Move testPoint to 0|0
	testPoint.x = 0
	testPoint.y = 0
	testPoint.z = 0
	testPointLine = LineSegment(testPoint, testPoint)

	# Is testPoint on an edge?
	edge = LineSegment(Point(0,0,0), Point(0,0,0))
	for i in range(n):
		edge.p1 = polygon[i]
		# Get correct index of successor
		edge.p2 = polygon[getNextIndex(n, i)]
		if intersect(testPointLine, edge) == 1:
			return 1

	# No start point found and point is not on an edge or node
	# --> point is outside
	if startNodePosition == -1:
		return 0

	count = 0
	seenPoints = 0
	i = startNodePosition

	# Consider all edges
	while(seenPoints < n):
		savedX = polygon[getNextIndex(n, i)].x
		savedIndex = getNextIndex(n, i)

		# move to next point which is not on the x-axis
		while 1:
			i = getNextIndex(n, i)
			seenPoints += 1
			if polygon[i].y != 0:
				break

		# Found end point
		endPoint.x = polygon[i].x
		endPoint.y = polygon[i].y

		# Only intersect lines that cross the x-axis
		if startPoint.y * endPoint.y < 0:
			edge.p1 = startPoint
			edge.p2 = endPoint
			
			# No nodes have been skipped and the successor node
			# has been chosen as the end point
			if savedIndex == i:
				count += intersect(edge, xAxisPositive)

			# If at least one node on the right side has been skipped,
			# the original edge would have been intersected
			# --> intersect with full x-axis
			elif savedIndex > 1:
				count += intersect(edge, xAxis)

		# End point is the next start point
		startPoint = endPoint 

	# Odd count --> in the polygon (1)
	# Even count --> outside (0)
	return count % 2

def write_to_png():
	pass

def main():
	create_roads(4)
	generate_junction_surface()
	sample()

if __name__ == '__main__':
	main()