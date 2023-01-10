import bpy
import os

# Select all objects in the scene
bpy.ops.object.select_all(action='SELECT')

# Delete all selected objects
bpy.ops.object.delete()

# Get the current working directory
path = os.getcwd()

# Get a list of all .dae files with the suffix "_fixed" in the folder
files = [f for f in os.listdir(path) if f.endswith('_fixed.dae')]

# Iterate through the .dae files
for file in files:
    # Import the .dae file
    bpy.ops.wm.collada_import(filepath=os.path.join(path, file))

    # Create an empty called 'base00'
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0))
    base00 = bpy.context.active_object
    base00.name = 'base00'

    # Create an empty called 'start01' and parent it to 'base00'
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0))
    start01 = bpy.context.active_object
    start01.name = 'start01'
    start01.parent = base00

     # Parent all objects in the scene to 'start01'
    for obj in bpy.data.objects:
        # Skip the object if it is already a child of 'start01' or if it is 'start01' itself
        if obj.parent != start01 and obj != start01:
            obj.parent = start01
    
    # Get the original file name without the "_fixed" suffix
    original_name = file[:-9]
    # Export 'start01' to a .dae file with the same name as the original file but with the "_final" suffix
    bpy.ops.wm.collada_export(filepath=os.path.join(path, original_name + "_final.dae"))
    
    # Remove all objects from the scene
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()