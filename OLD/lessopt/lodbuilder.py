import bpy
import os

# Delete the default objects
bpy.ops.object.delete()

# Get a list of all .dae files in the current directory
dae_files = [f for f in os.listdir('.') if f.endswith('.dae')]

# Iterate over the .dae files
for dae_file in dae_files:
    # Check if the file has a prefix of "lod", "_lod", or "l_"
    if dae_file.startswith(('lod', '_lod', 'l_')):
        # Get the file name without the prefix
        base_name = dae_file[4:]
        
        # Check if the file has a suffix of "_lod_0X"
        if base_name.endswith('_lod_0'):
            # Get the number after the "_lod_0" part of the suffix
            suffix_number = base_name[-1]
            
            # Check if the number is between 1 and 99
            if suffix_number.isnumeric() and 1 <= int(suffix_number) <= 99:
                # Get the file name without the suffix
                base_name = base_name[:-7]
        
        # Check if there is a matching file with the same name but no prefix or suffix
        if base_name in dae_files:
            # Import the two files
            bpy.ops.wm.collada_import(filepath=dae_file)
            bpy.ops.wm.collada_import(filepath=base_name)
            
            # Get a list of the imported objects
            imported_objects = [obj for obj in bpy.data.objects if obj.type != 'EMPTY']


            # Create an empty called "base00"
            bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0))
            base00 = bpy.context.active_object
            base00.name = "base00"

            # Create an empty called "start01" inside "base00"
            bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0))
            start01 = bpy.context.active_object
            start01.name = "start01"
            start01.parent = base00

                        # Iterate over the imported objects
            for obj in imported_objects:
                # Check if the object's name contains the string "lod"
                if "lod" in obj.name:
                    # Add the suffix "_a130" to the object's name
                    obj.name += "_a130"
                else:
                    # Check if the object's name is the same as the "lod" object's name without the "lod" string
                    for lod_obj in imported_objects:
                        if "lod" in lod_obj.name and obj.name == lod_obj.name.replace("lod", ""):
                            # Add the suffix "_a430" to the object's name
                            obj.name += "_a430"
            
            # Parent the imported objects to "start01"
            for obj in imported_objects:
                obj.parent = start01
                
            # Export the two files together
            bpy.ops.wm.collada_export(filepath=dae_file)

            # Remove the imported objects from the scene
            for obj in imported_objects:
                bpy.data.objects.remove(obj)
                
                
                
                
                