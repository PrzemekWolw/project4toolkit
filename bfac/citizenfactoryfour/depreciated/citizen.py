def script3_function():
    print("Converting Quaternions")


import bpy
import os
import mathutils

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

#This will convert the models position and rotation (w, x, y, z) quaternion by using the decrypted .wpl stream files. 
#There is a known error here that in some fringe cases the w rotation is flipped positive when it should be negative, or vice versa. I do not have a fix for this other than manually editing. I know OpenFormats and GIMS experienced the same issue, but do not know how they fixed it.

with open("stream.p4tkpl", "r") as stream:
    lines = stream.readlines()

for line in lines:
    values = line.split()

    # Extract the position and rotation values from .wpl. RAGE uses Euler for position and quaternion for its rotations, it is also possible to convert to a rotation matrix that T3D would understand since it does not currently support .json quaternion to my knowledge. If the mechanism for doing so can be found, error correction for W need not be implemented.
    # WDD dictionaries when exploded still use this format in the WPL, it is just contained in the non '_stream' WPLs. You cannot remove the '_stream' WPLs for the script using just the LODs as R* sometimes includes LOD positions in the stream.
    pos_x = float(values[0].replace(",", ""))
    pos_y = float(values[1].replace(",", ""))
    pos_z = float(values[2].replace(",", ""))
    rot_x = float(values[3].replace(",", ""))
    rot_y = float(values[4].replace(",", ""))
    rot_z = float(values[5].replace(",", ""))
    rot_w_str = values[6].replace(",", "")
    rot_w = -float(rot_w_str[1:]) if rot_w_str[0] == "-" else float(rot_w_str)
    quat = mathutils.Quaternion((rot_w, rot_x, rot_y, rot_z))
    dae_name = (values[7].replace(",", ""))

    cwd = os.getcwd()
    filepath = os.path.join(cwd, f"{dae_name}.dae")
    if not os.path.exists(filepath):
        continue

    bpy.ops.wm.collada_import(filepath=os.path.join(cwd, f"{dae_name}.dae"))

    for obj in bpy.context.scene.objects:
        obj.rotation_mode = "QUATERNION"
        obj.rotation_quaternion = quat
        # fix for the above quat bug is forcing all non w=1 quats to a negative, even if the engine does not consider them as such. this works for all models and fixes the rotation bug.
        obj.rotation_quaternion.w *= -1
        obj.location = (pos_x, pos_y, pos_z)

    export_path = os.path.join(cwd, f"{dae_name}.dae")

    bpy.ops.wm.collada_export(filepath=export_path)
    bpy.ops.object.delete()

    print(dae_name)
    print(pos_x, pos_y, pos_z)
    print(quat)

def script4_function():
    print("Assigning Materials")

script4_function()

import bpy
import os

def find_base_color_node(mat):
    try:
        for node in mat.node_tree.nodes:
            if node.type == 'BSDF_PRINCIPLED':
                break

        return node.inputs["Base Color"].links[0].from_node
        
    except Exception:
        return None

def get_node_name(node):
    try:
        return node.label or node.image.name
    except Exception:
        return None

def convert_dae_file(filepath):
    print(f"Converting {filepath}...")
    bpy.ops.wm.collada_import(filepath=filepath)
    mat_names = [
        mat.name for mat in bpy.data.materials
        if mat.name.startswith("MAT")
    ]

    for mat_name in mat_names:
        mat = bpy.data.materials[mat_name]
        node = find_base_color_node(mat)
        if new_name := get_node_name(node):
            mat.name = new_name

    filepath_dst = os.path.splitext(filepath)[0] + ".dae"
    bpy.ops.wm.collada_export(filepath=filepath_dst)
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

def convert_recursive(base_path):
    for entry in os.scandir(base_path):
        if entry.is_file() and entry.name.endswith('.dae'):
            convert_dae_file(entry.path)
        elif entry.is_dir():
            convert_recursive(entry.path)

convert_recursive(os.getcwd())


def script5_function():
    print("Cleaning Materials")

# This just works better than attempting material cleaning in Blender, and saves an import. The re.sub for .XXXX is really only used when I test collision dictionaries for now, but when native collision support is added this will come in handy.
import os
import re

cwd = os.getcwd()
for file in os.listdir(cwd):
    if file.endswith(".dae"):
        with open(os.path.join(cwd, file), "r") as f:
            lines = f.readlines()
        with open(os.path.join(cwd, file), "w") as f:
            for line in lines:
                line = re.sub(r'_\d+-material', '-material', line)
                line = re.sub(r'\.\d+">', '">', line)
                line = re.sub(r'\.png', '', line)  # Remove ".png" from the lines
                f.write(line)

def script4_function():
    print("Merging LODs")

import bpy
import os

# Delete all objects in the scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Set the path to the directory containing the .dae files
path = os.getcwd()

filename = input("Enter the name of the zone you are exporting (without the .idx extension): ")
filename += ".idx"
with open(filename, 'r') as f:
    lines = f.readlines()

# Loop through each line in the .idx file
for line in lines:
    # Get the names of the models in the current line
    models = [model.lower() for model in line.strip().split(', ')]
    model1, model2, model3 = models[0], models[1], models[2]
    
    # Check if the .dae file for model1 exists in the cwd
    if not os.path.exists(os.path.join(path, model1 + '.dae')):
        # If it doesn't exist, skip to the next line
        continue
    
    # Import model1 into Blender and name it with the suffix '_a430'
    bpy.ops.wm.collada_import(filepath=os.path.join(path, model1 + '.dae'))
    obj1 = bpy.context.selected_objects[0]
    obj1.name = obj1.name + '_a11500'
    
    # Create an empty and name it 'nulldetail50'
    null_obj = bpy.data.objects.new('nulldetail50', None)
    
    # Link the empty to the scene and move it to the origin
    bpy.context.scene.collection.objects.link(null_obj)
    null_obj.location = (0, 0, 0)
    
    if os.path.exists(os.path.join(path, model2 + '.dae')):
        # If the .dae file for model2 exists in the cwd, import it into Blender
        bpy.ops.wm.collada_import(filepath=os.path.join(path, model2 + '.dae'))
        obj2 = bpy.context.selected_objects[0]
        obj2.name = obj2.name + '_a1000'
    else:
        # If it doesn't exist, create an empty and name it with the suffix '_a250'
        null_obj2 = bpy.data.objects.new('nulldetail1000', None)
        bpy.context.scene.collection.objects.link(null_obj2)
        null_obj2.location = (0, 0, 0)
        obj2 = null_obj2
    
    # Create two empties and name them 'base00' and 'start01'
    base = bpy.data.objects.new('base00', None)
    start = bpy.data.objects.new('start01', None)
    
    # Link the objects to the scene and move them to the origin
    bpy.context.scene.collection.objects.link(base)
    bpy.context.scene.collection.objects.link(start)
    base.location = (0, 0, 0)
    start.location = (0, 0, 0)
    
    # Make 'start01' the parent of 'base00', 'nulldetail50', and the two objects
    for obj in [obj1, obj2]:
        obj.parent = start
    null_obj.parent = start
    start.parent = base
    
    merged_filename = model1.capitalize() + '_' + model2.capitalize() + '_merged.dae'
    bpy.ops.wm.collada_export(filepath=os.path.join(path, merged_filename))
    
    # Delete all objects in the scene
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

# Delete the original .dae files
    if os.path.exists(os.path.join(path, model1 + '.dae')):
        os.remove(os.path.join(path, model1 + '.dae'))
    else:
        continue
    if os.path.exists(os.path.join(path, model2 + '.dae')):
        os.remove(os.path.join(path, model2 + '.dae'))
    else:
        continue

################################################################

def script5_function():
    print("Cleaning Materials")

# This just works better than attempting material cleaning in Blender, and saves an import. The re.sub for .XXXX is really only used when I test collision dictionaries for now, but when native collision support is added this will come in handy.
import os
import re

cwd = os.getcwd()
for file in os.listdir(cwd):
    if file.endswith(".dae"):
        with open(os.path.join(cwd, file), "r") as f:
            lines = f.readlines()
        with open(os.path.join(cwd, file), "w") as f:
            for line in lines:
                line = re.sub(r'_\d+-material', '-material', line)
                line = re.sub(r'\.\d+">', '">', line)
                f.write(line)

################################################################

def script6_function():
    print("Moving Files")


import os
import shutil

cwd = os.getcwd()

delete_types = ['.obj', '.mtl', '.odr', '.mesh', '.odd', '.otd']

for item in os.listdir(cwd):
    item_path = os.path.join(cwd, item)
    if os.path.isfile(item_path):
        if any(item.endswith(x) for x in delete_types):
            os.remove(item_path)
        elif item.lower().endswith(".dae") and "merged" not in item.lower() and ("slod" in item.lower() or "lod" in item.lower()):
            os.remove(item_path)
    elif os.path.isdir(item_path):
        shutil.rmtree(item_path)

# Create the target directory outside the current working directory
parent_dir = os.path.abspath(os.path.join(cwd, os.pardir))
target_dir = os.path.join(parent_dir, "map")
if not os.path.exists(target_dir):
    os.mkdir(target_dir)

# Move all remaining .dae files to the target directory
for item in os.listdir(cwd):
    item_path = os.path.join(cwd, item)
    if os.path.isfile(item_path) and item.lower().endswith(".dae"):
        target_path = os.path.join(target_dir, item)
        shutil.move(item_path, target_path)
