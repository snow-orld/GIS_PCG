"""
file: polygon_test.py

play with polygon module.

author: Xueman Mou
date: 2018/4/9
version: 1.0.1
modified: 2018/4/9 14:45:00 +0800

developing env: python 3.5.2
dependencies: bpy, bmesh, polygon

Polygon Ref: https://www.j-raedler.de/projects/polygon/
"""

#import bpy
#import bmesh
import Polygon, Polygon.IO

q = Polygon.Polygon(((0.0,0.0), (10.0, 0.0), (10.0, 5.0), (0.0, 5.0)))
t = Polygon.Polygon(((1.0, 1.0), (3.0, 1.0), (2.0, 3.0)))
a = q - t
#Polygon.IO.writeSVG('test.svg', (a, ))

c = Polygon.Shapes.Circle()
s = Polygon.Shapes.Star()
Polygon.IO.writeSVG('test.svg', (a, c, s))