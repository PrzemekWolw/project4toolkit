import bpy
import os
import re

# Select all objects in the scene
bpy.ops.object.select_all(action='SELECT')

# Delete all selected objects
bpy.ops.object.delete()

# Get a list of all .dae files in the current directory
dae_files = [f for f in os.listdir('.') if f.endswith('.dae')]

# Iterate over the .dae files
for dae_file in dae_files:
    # Define base_name as an empty string
    base_name = ""
    # Check if the file has a prefix of "lod", "LOD", "lod_", or "LOD_"
    if dae_file.startswith(('lod_', 'LOD_')):
        # Get the file name without the prefix
        base_name = dae_file[4:]
    elif dae_file.startswith(('lod', 'LOD')):
        base_name = dae_file[3:]
        
        # Check if there is a matching file with the same name but no prefix or suffix
        if base_name in dae_files:
            # Import the two files
            bpy.ops.wm.collada_import(filepath=dae_file)
            bpy.ops.wm.collada_import(filepath=base_name)
            
            # Get a list of the imported objects
            imported_objects = [obj for obj in bpy.data.objects if obj.type != 'EMPTY']


            

            # Iterate over the imported objects
            for obj in imported_objects:
                # Check if the object's name contains any of the strings in the tuple ('lod', 'LOD', '_lod', 'l_')
                if any(prefix in obj.name for prefix in ('lod', 'LOD', '_lod', 'l_')):
                    # Add the suffix "_a130" to the object's name
                    obj.name += "_a130"
                else:
                    # Add the suffix "_a430" to the object's name
                    obj.name += "_a430"

            # Export the two files together
            bpy.ops.wm.collada_export(filepath=dae_file[:-4] + "_fixed.dae")

            # Remove the imported objects from the scene
            for obj in imported_objects:
                bpy.data.objects.remove(obj)
                
   
exec(open("empty.py").read())                   
                
                