import bpy
import os
import re

# Select all objects in the scene
bpy.ops.object.select_all(action='SELECT')

# Delete all selected objects
bpy.ops.object.delete()



# Get a list of all .dae files in the current directory
dae_files = [f for f in os.listdir('.') if f.endswith('.dae')]

# Create a dictionary to store the matching .dae files
matches = {}

# Initialize a counter for the number of .dae files that meet the criteria
counter2 = 0

for dae_file in dae_files:
    base_name = ""
    if dae_file.endswith(('_lod', '_LOD')):
        if dae_file[-7:] in ['_lod_01', '_lod_02', '_lod_03', '_lod_04', '_lod_05', '_lod_06', '_lod_07', '_lod_08', '_lod_09', '_lod_10', '_lod_11', '_lod_12', '_lod_13', '_lod_14', '_lod_15', '_lod_16', '_lod_17', '_lod_18', '_lod_19', '_lod_20']:
            base_name = dae_file[:-7]
        elif dae_file[-6:] in ['_LOD01', '_LOD02', '_LOD03', '_LOD04', '_LOD05', '_LOD06', '_LOD07', '_LOD08', '_LOD09', '_LOD10', '_LOD11', '_LOD12', '_LOD13', '_LOD14', '_LOD15', '_LOD16', '_LOD17', '_LOD18', '_LOD19', '_LOD20']:
            base_name = dae_file[:-6]
        elif dae_file[-4:-1].isnumeric():
            base_name = dae_file[:-4]
        elif dae_file.endswith('_LOD'):
            base_name = dae_file[:-4]
        else:
            base_name = dae_file[:-5]
    elif dae_file.startswith(('lod_', 'LOD_')):
        base_name = dae_file[4:]
    elif dae_file.startswith(('lod', 'LOD')):
        base_name = dae_file[3:]

        
    # Increment the counter
    counter2 += 1
    
    # Check if the base_name is in the dictionary
    if base_name in matches:
        # Add the dae_file to the list of matching files
        matches[base_name].append(dae_file)
    else:
        # Add the base_name and dae_file to the dictionary
        matches[base_name] = [dae_file]

# Print the matching .dae files
for base_name, dae_files in matches.items():
    print(f"Matching .dae files for {base_name}: {dae_files}")
    
    print(f"LOD to Main Mesh Matches {counter2}")
    