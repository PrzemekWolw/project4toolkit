import bpy
import os

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

cwd = os.getcwd()
for filename in os.listdir(cwd):
    if filename.endswith(".dae"):
        file_path = os.path.join(cwd, filename)
        bpy.ops.wm.collada_import(filepath=file_path)
        for obj in bpy.context.selected_objects:
            if obj.type == 'MESH':
                if obj.name.endswith("_a130") or obj.name.endswith("_a250"):
                    obj.data.materials.clear()
                    gray = bpy.data.materials.new("gray")
                    obj.data.materials.append(gray)
        bpy.ops.wm.collada_export(filepath=file_path)
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()
