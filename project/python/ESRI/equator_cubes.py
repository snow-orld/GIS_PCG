"""
file: equator_cubes.py

ecef positions at equator to test against dynamic loading at client.

author: Xueman Mou
date: 2018/4/19
version: 1.0.1
modified: 2018/4/19 10:42:00 GMT +0800

developing env: python 3.5.2
dependencies: pyshp, pyproj, bpy, bmesh, mathutils, math, random
"""
import math
import random

R = 64000 # raidus of earth 6400km at equator

def get_posionts_on_equator(segments):
	with open('ecef_equator.txt', 'w') as f:
		for i in range(segments):
			delta_theta = 360 / 180 * math.pi / segments
			f.write('{}, {}, {}\n'.format(R * math.cos(delta_theta * i), R * math.sin(delta_theta * i), 10 * random.random()))

def main():
	segments = int(R / 100 * 2 * math.pi)
	get_posionts_on_equator(segments)	

if __name__ == '__main__':
	main()