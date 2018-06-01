"""
file: parameters.py

global parameters used in building up roads

author: Xueman Mou
date: 2018/5/28
version: 1.0.1
modified: 2018/5/28 14:01:00 GMT +0800

developing env: python 3.5.2
dependencies: pyproj

"""

import pyproj

# proj parameters
WGS84 = pyproj.Proj(init='epsg:4326') # longlat
ECEF = pyproj.Proj(init='epsg:4978') # geocentric

center = None
DB = '/Users/mxmcecilia/Documents/GIS_PCG/project/python/ESRI/EMG_CX.db'