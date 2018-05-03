"""
file: leatStorage.py

include lots of utility functions

author: Xueman Mou
date: 2018/4/25
version: 1.0.1
modified: 2018/4/25 09:27:00 GMT +0800

developing env: python 3.5.2
dependencies: leancloud
"""

import leancloud
import random
import math
import json

def init():
	leancloud.init('lLuXQkIRtEx5v4SV1NMduoAs-gzGzoHsz', 'P7U5cm6AOC8J2TvC3Wjnl5Ww')

def uploadFile(number = 2):
	fileURLs = []
	for i in range(number):
		with open('./data/test.gltf', 'rb') as f:
			lfile = leancloud.File('test' + str(i) + '.gltf', f)
			lfile.save()
			lfileID = lfile.id
			fileURLs.append(lfile.url)
	return fileURLs

def insertData(fileURLs, number = 2):
	TestObject = leancloud.Object.extend('TestObject')

	for i in range(number):
		test_object = TestObject()
		test_object.set('type', 0)
		test_object.set('center', (number * random.random(), number * random.random(), number * random.random()))
		test_object.set('boundRadius', number * random.random())
		test_object.set('url', fileURLs[i])
		test_object.save()

def query(center, radius):
	TestObject = leancloud.Object.extend('TestObject')
	query = leancloud.Query(TestObject)

	query.exists('objectId')
	IDsInRange = []
	for result in query.find():
		pcenter = result.get('center')
		pradius = result.get('boundRadius')
		
		centerDistance = math.sqrt((center[0] - pcenter[0])**2 + (center[1] - pcenter[1])**2 + (center[2] - pcenter[2])**2)
		if centerDistance < radius + pradius:
			IDsInRange.append(result.id)

	query2 = leancloud.Query(TestObject)
	json_obj = []
	for id in IDsInRange:
		result = query2.get(id)
		obj = {'id': id, 'type': result.get('type'), 'center': result.get('center'), 'bounds': result.get('boundRadius'), 'asseturi': result.get('url')}
		json_obj.append(obj)

	print (json_obj)
	return json.dumps(json_obj)

def main():
	init()
	fileURLs = uploadFile()
	insertData(fileURLs)
	# query((0,0,0), 10)

if __name__ == '__main__':
	main()