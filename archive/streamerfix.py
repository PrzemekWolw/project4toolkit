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
def remove_all_nonsense():

    # Remove objects
    for obj in bpy.data.objects:
        if obj.name.startswith("cube"):
            bpy.ops.object.select_all(action='DESELECT')
            obj.select_set(True)
            bpy.ops.object.delete()

    # Remove lights
    for obj in bpy.data.objects:
        if obj.name.startswith("light"):
            bpy.ops.object.select_all(action='DESELECT')
            obj.select_set(True)
            bpy.ops.object.delete())

    # Remove cameras
    for obj in bpy.data.objects:
        if obj.name.startswith("camera"):
            bpy.ops.object.select_all(action='DESELECT')
            obj.select_set(True)
            bpy.ops.object.delete()
            
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
        
        # Remove nonsense
        remove_all_nonsense()
                
        # Export the .dae file, overwriting the original
        bpy.ops.wm.collada_export(filepath=file_path)
        
        # Remove the object from the scene
        bpy.ops.object.delete()
        
