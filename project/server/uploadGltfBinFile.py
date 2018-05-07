"""
file: uploadGltfBinFile.py

upload GLTF and bin file to lean storage

author: Xueman Mou
date: 2018/5/4
version: 1.0.0
modified: 2018/5/7 08:37:00 GMT +0800

developing env: python 3.5.2
dependencies: leancloud
write output file: ../server/data/ecef_roads.txt
"""

import os
import leancloud

def init():
	leancloud.init('lLuXQkIRtEx5v4SV1NMduoAs-gzGzoHsz', 'P7U5cm6AOC8J2TvC3Wjnl5Ww')

def upload_bin(roadID):
	# pass
	# return uploaded file name (or link is composed of name)
	binurl = None
	road_name = 'Road_' + roadID
	path = os.path.join(os.path.dirname(__file__), 'data')
	if os.path.isfile(os.path.join(path, road_name + '.bin')):
		with open(os.path.join(path, road_name + '.bin'), 'rb') as f:
			leanfile = leancloud.File(road_name + '.bin', f)
			leanfile.save()
			binurl = leanfile.url.split('/')[-1]
	return binurl

def modify_gltf(roadID, binuri):
	pass
	# open roadID file 
	# then modify the bin files url
	# save the file
	road_name = 'Road_' + roadID
	path = os.path.join(os.path.dirname(__file__), 'data')
	with open(os.path.join(path, road_name + '.gltf'), 'r') as fr:
		with open(os.path.join(path, road_name + '.tmp.gltf'), 'w') as fw:
			for line in fr:
				if "uri" in line:
					fw.write(line.replace(road_name + '.bin', binuri))
				else:
					fw.write(line)
	os.rename(os.path.join(path, road_name + '.tmp.gltf'), os.path.join(path, road_name + '.gltf'))

def upload_gltf(roadID):
	pass
	# return uploaded file link
	gltfufl = None
	road_name = 'Road_' + roadID
	path = os.path.join(os.path.dirname(__file__), 'data')
	with open(os.path.join(path, road_name + '.gltf'), 'rb') as f:
		leanfile = leancloud.File(road_name + '.gltf', f)
		leanfile.save()
		gltfurl = leanfile.url
	return gltfurl

def insert_road_info(roadID, center, radius):
	pass
	# upload road_id bin file
	# modify gltf 
	# upload road_id gltf file
	# insert into a class table with ecef center, bounding sphere radius
	# done

	print('writing %s into table...' % roadID)

	binurl = upload_bin(roadID)
	if binurl is not None:
		modify_gltf(roadID, binurl)
	gltfurl = upload_gltf(roadID)

	road_name = 'Road_' + roadID
	TestObject = leancloud.Object.extend('TestObject')
	test_object = TestObject()
	test_object.set('roadID', roadID)
	test_object.set('type', 0)
	test_object.set('center', center)
	test_object.set('boundRadius', radius)
	test_object.set('url', gltfurl)
	test_object.save()

def main():
 	# according to ecef_roads.txt, get each lines roadID
 	# insert_road_info(roadID, center, radius)

 	init()
 	# upload_bin('5010000001')
 	# modify_gltf('5010000001', '069c13e1f47a41348dfb2dc65f99a1b5.bin')
 	# insert_road_info('5010000001', (0,0,100), 10)

 	path = os.path.join(os.path.dirname(__file__), 'data')
 	with open(os.path.join(path, 'ecef_roads.txt')) as f:
 		for line in f:
 			roadID, center_x, center_y, center_z, radius = line.split(',')
 			center = (float(center_x), float(center_y), float(center_z))
 			radius = float(radius)
 			insert_road_info(roadID, center, radius)

if __name__ == '__main__':
	main()