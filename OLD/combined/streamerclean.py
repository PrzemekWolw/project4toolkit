import bpy
import os

def replace_material(bad_mat, good_mat):
    if bad_mat.name[-3:].isnumeric() and bad_mat.name[-4] == ".":
        bad_mat.name = bad_mat.name[:-4]
    for obj in bpy.data.objects:
        for slot in obj.material_slots:
            if slot.material == bad_mat:
                slot.material = good_mat
    bpy.data.materials.remove(bad_mat)

def get_duplicate_materials(og_material):
    duplicate_materials = []
    for material in bpy.data.materials:
        if material is not og_material and material.name == og_material.name:
            duplicate_materials.append(material)
    return duplicate_materials

def remove_all_duplicate_materials():
    for material in bpy.data.materials:
        duplicate_materials = get_duplicate_materials(material)
        for duplicate_material in duplicate_materials:
            replace_material(duplicate_material, material)

folder_path = "."
for file in os.listdir(folder_path):
    if file.endswith(".dae"):
        file_path = os.path.join(folder_path, file)
        bpy.ops.wm.collada_import(filepath=file_path)
        remove_all_duplicate_materials()
        bpy.ops.wm.collada_export(filepath=file_path)
        bpy.ops.object.delete()