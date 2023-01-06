#there is probably an error with running brook merge at the end in overwriting proper rotations with unfixed meshes
#there is also likely an error with rotations from the .wpl using E for exponents in defining the float value, should probably be converted to use another representation or removed altogether past thousandths place.

import bpy
import os


def replace_material(bad_mat, good_mat):
    bad_mat.user_remap(good_mat)
    bpy.data.materials.remove(bad_mat)
    
    
def get_duplicate_materials(og_material):
    
    common_name = og_material.name
    
    if common_name[-3:].isnumeric():
        common_name = common_name[:-4]
    
    duplicate_materials = []
    
    for material in bpy.data.materials:
        if material is not og_material:
            name = material.name
            if name[-3:].isnumeric() and name[-4] == ".":
                name = name[:-4]
            
            if name == common_name:
                duplicate_materials.append(material)
    
    text = "{} duplicate materials found"
    print(text.format(len(duplicate_materials)))
    
    return duplicate_materials


def remove_all_duplicate_materials():
    i = 0
    while i < len(bpy.data.materials):
        
        og_material = bpy.data.materials[i]
        
        print("og material: " + og_material.name)
        
        # get duplicate materials
        duplicate_materials = get_duplicate_materials(og_material)
        
        # replace all duplicates
        for duplicate_material in duplicate_materials:
            replace_material(duplicate_material, og_material)
        
        # adjust name to no trailing numbers
        if og_material.name[-3:].isnumeric() and og_material.name[-4] == ".":
            og_material.name = og_material.name[:-4]
            
        i = i+1
    
# Specify the path to the folder containing the .dae files
folder_path = "C:/Users/user/Downloads/P4Toolkit/"

# Iterate through all .dae files in the folder
for file in os.listdir(folder_path):
    if file.endswith(".dae"):
        file_path = os.path.join(folder_path, file)
        
        # Import the .dae file
        bpy.ops.wm.collada_import(filepath=file_path)
        
        # Remove duplicate materials
        remove_all_duplicate_materials()
                
        # Export the .dae file, overwriting the original
        bpy.ops.wm.collada_export(filepath=file_path)
        
        # Remove the object from the scene
        bpy.ops.object.delete()

import os
import shutil
import zipfile

# Find all .dds and .dae files in the current directory and its subdirectories
dds_files = []
for root, dirs, files in os.walk("."):
    for file in files:
        if file.endswith(".dds") or file.endswith(".dae"):
            dds_files.append(os.path.join(root, file))

# Create a new directory called "brook"
os.makedirs("brook", exist_ok=True)

# Move all .dds and .dae files into the new directory
for file in dds_files:
    shutil.move(file, "brook")