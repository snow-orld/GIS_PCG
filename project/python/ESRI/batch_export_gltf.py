# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 3
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
# ##### END GPL LICENSE BLOCK #####

"""
file: batch_export_gltf.py

draw closed lanes with surfaces. Lanes can be in a junction.

author: Xueman Mou
date: 2018/5/4
version: 1.0.1
modified: 2018/5/4 14:11:00 GMT +0800

developing env: python 3.5.2
dependencies: sqlite3, pyshp, pyproj, bpy, bmesh, mathutils, math
"""

bl_info = {
	"name": "Batch Export gltf files",
	"author": "Xueman Mou",
	"version": (1, 0, 1),
	"blender": (2, 78, 3),
	"location": "3D View > Object Mode > Tools > Capsule",
	"wiki_url": "",
	"description": "Batch export assets into multiple gltf files.",
	"tracker_url": "",
	"category": "Import-Export"
}

import bpy

class BatchExportGLTF(bpy.types.Operator):
	"""Batch Export multiple gltf files"""
	bl_idname = "object.batch_export_gltf"
	bl_label = "Batch Export GLTF Files"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		print('Executed ADD-ON')

		return {'FINISHED'}

def register():
	bpy.utils.register_class(BatchExportGLTF)

def unregister():
	bpy.utils.unresiter_class(BatchExportGLTF)

if __name__ == '__main__':
	register()
