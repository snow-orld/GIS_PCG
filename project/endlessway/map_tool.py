"""
file: map_tool.py

Basic operations used when mapping unit track to road reference line as a blender plugin

author: Xueman Mou
date: 2018/5/22
version: 1.0.0
modified: 2018/5/22 17:00:00 GMT +0800

developing env: python 3.5.2
dependencies: bpy, os, sqlite3, pyshp, pyproj, math, Quaternion
"""

bl_info = {
	"name": "Map Tools",
	"version": (1, 0),
	"blender": (2, 7, 8),
	"location": "VIEW 3D > Tools > Map Tool",
	"description": "Tools for mapping unit track to road reference line",
	"warning": "For Internal Development Only",
	"wiki_url": "",
	"tracker_url": "",
	"category": "Mesh"}

# Imports
import bpy
from bpy.types import Operator, Menu, Panel, UIList
from bpy.props import BoolProperty, FloatProperty, IntProperty, StringProperty

# *************** Operators used in Map Tool *******************
class MapTool_Operator_FocusOnSelectedObject(Operator):
	"""Focus on to the selected Object"""
	bl_idname = "map.focus_on_selected_object"
	bl_label = "Focus on selected object"
	bl_options = {"REGISTER", "UNDO"}
	
	def execute(self, context):
		print('HELLO WORLD')
		
		return {'FINISHED'}


# *************** Tools Panel for Map Tool **********************
class MapToolPanel:
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'TOOLS'
	bl_category = 'Map Tools'

class MapTool_Panel_Focus(MapToolPanel, Panel):
	bl_label = 'Focus on Selected Object'

	def draw(self, context):
		layout = self.layout

		col = layout.column(align=True)
		layout.operator("map.focus_on_selected_object")

def register():
	bpy.utils.register_class(MapTool_Operator_FocusOnSelectedObject)

	bpy.utils.register_class(MapTool_Panel_Focus)

def unregister():
	bpy.utils.unregister_class(MapTool_Operator_FocusOnSelectedObject)

	bpy.utils.unregister_class(MapTool_Panel_Focus)

if __name__ == '__main__':
	register()