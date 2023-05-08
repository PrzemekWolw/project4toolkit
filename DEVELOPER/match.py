
def script1_function():
    script1_function()
import bpy
import os

def import_dae(file_path):
    bpy.ops.wm.collada_import(filepath=file_path)

def rename_object(obj, new_name):
    obj.name = new_name

def create_empty(name):
    bpy.ops.object.empty_add(type='ARROWS', radius=1, location=(0, 0, 0))
    obj = bpy.context.object
    obj.name = name
    return obj

def set_parent(child, parent):
    child.parent = parent

def export_dae(file_path):
    bpy.ops.wm.collada_export(filepath=file_path, selected=True)

# Get all .dae files in the current working directory
cwd = os.getcwd()
dae_files = [f for f in os.listdir(cwd) if f.endswith('.dae')]

# Store the names of the .dae files in a set
dae_set = set(dae_files)

# Read the .pt4kIDX file and search for matches
matches = []
with open('mh01.pt4kIDX', 'r') as f:
    for line in f:
        name1, name2, _ = line.strip().split(',')
        name1 = name1.strip() + '.dae'
        name2 = name2.strip() + '.dae'
        if name1 in dae_set and name2 in dae_set:
            matches.append((name1, name2))

# Create a set to store the names of the .dae files that are used in matches
used_dae_files = set()
for match in matches:
    used_dae_files.update(match)

# Import and rename the .dae files for each match
for name1, name2 in matches:
    file_path1 = os.path.join(cwd, name1)
    file_path2 = os.path.join(cwd, name2)

    import_dae(file_path1)
    obj1 = bpy.context.selected_objects[0]
    rename_object(obj1, obj1.name + "_a430")

    import_dae(file_path2)
    obj2 = bpy.context.selected_objects[0]
    rename_object(obj2, obj2.name + "_a250")

    # Create the empty objects and set their hierarchy
    base00 = create_empty("base00")
    start01 = create_empty("start01")
    set_parent(start01, base00)
    set_parent(obj1, start01)
    set_parent(obj2, start01)

    # Select all objects and export to a single .dae file
    bpy.ops.object.select_all(action='SELECT')
    export_path = os.path.join(cwd, name1.split('.')[0] + "_" + name2.split('.')[0] + "_merged.dae")
    export_dae(export_path)

    # Remove all objects from the scene
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

# Rename .dae files that have no matching pairs and are not used in any valid imports/exports
for dae_file in dae_files:
    if dae_file not in used_dae_files:
        file_path = os.path.join(cwd, dae_file)
        os.rename(file_path, os.path.join(cwd, dae_file.split('.')[0] + "_unmatched.dae"))


def script2_function():
    script2_function()

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



##### this isnt parent of this script MOVE IT, this is for creating the index of inside outside img
# These are a complete mess and still need to be manually written to because R* messed up the outside/inside .IMG .WPL index. For most models the way this works is that the insideIMG .wpls will refer a .wdr to a index line in the outsideIMG, and that is how LODs are matched to real models. However for a fair number of .wdrs they are all pushed into the outsideIMG and self refers to a line within itself. NIGHTMARE!
with open('mh01.p4tkLITTLE') as little_file:
    with open('mh01.p4tkBIG') as big_file:
          with open('output.txt', 'w') as output_file:
            for little_line in little_file:
                little_parts = little_line.strip().split(',')
                little_name = little_parts[7].strip()
                big_line_number = int(little_parts[9].strip())
                if big_line_number != -1:
                    for i, big_line in enumerate(big_file):
                        if i == big_line_number -1:
                            big_parts = big_line.strip().split(',')
                            big_name = big_parts[7].strip()
                            output_file.write(f"{little_name}, {big_name}, {big_line_number}\n")
                            big_file.seek(0)
                            break
                        elif i >= big_line_number:
                            big_file.seek(0)
                            break
