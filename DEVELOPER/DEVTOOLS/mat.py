import bpy
import os
import re

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()


cwd = os.getcwd()
for file in os.listdir(cwd):
    if file.endswith(".dae"):
        bpy.ops.wm.collada_import(filepath=file)


        for ob in bpy.context.selected_editable_objects:    
            for m_slot in ob.material_slots:
                if not m_slot.material:
                    continue
                s1 = m_slot.material.name
                sArr = s1.split(".")
                m_slot.material.name = sArr[0]

        for ob in bpy.context.selected_editable_objects:    
            for m_slot in ob.material_slots:
                if not m_slot.material:
                    continue
                s1 = m_slot.material.name
                s1 = re.sub(r"\.\d{3}", "", s1)
                m_slot.material.name = s1

        for mat in bpy.data.materials:
            if mat.name[-4:].isdigit():
                mat.name = mat.name[:-4]
        print(s1)
        bpy.ops.wm.collada_export(filepath=file)
 
        bpy.ops.object.delete()