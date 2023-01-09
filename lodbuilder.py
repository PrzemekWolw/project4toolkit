import glob
import os
import re
import bpy

# Find all .dae files in the working directory
dae_files = glob.glob("*.dae")

# Iterate over the .dae files
for dae_file in dae_files:
    # Get the base name of the file (without the .dae extension)
    base_name = os.path.splitext(dae_file)[0]

    # Check if there's a matching .dae file with a name that
    # has the same base name if you remove "lod", "lod_",
    # "_lod01", or "_lod_01"
    match_found = False
    for possible_match in ["lod", "lod_", "_lod[0-9][0-9]", "_lod_[0-9][0-9]"]:
        if re.search(possible_match, base_name):
            # Remove the possible match from the base name
            # to get the name of the second .dae file
            second_dae_file = re.sub(possible_match, "", base_name) + ".dae"
            if os.path.exists(second_dae_file):
                match_found = True
                break
    
    # If a matching file was found, import both files and export them together
    if match_found:
        print(f"Matching .dae files found: {dae_file}, {second_dae_file}")