import bpy
import os
import json
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete

cwd = os.getcwd()
results = []

# Iterate over all .dae files in the current working directory
for filename in os.listdir(cwd):
    if filename.endswith(".dae"):
        filepath = os.path.join(cwd, filename)
        bpy.ops.wm.collada_import(filepath=filepath)

        # Select only the object with the suffix "_a430"
        for obj in bpy.context.selected_objects:
            if obj.name.endswith("_a430"):
                selected_obj = obj
                break

        # Calculate the bounding box of the selected object
        bbox = selected_obj.bound_box
        x_size = bbox[4][0] - bbox[0][0] + 0.5
        y_size = bbox[2][1] - bbox[0][1] + 0.5
        z_size = bbox[1][2] - bbox[0][2] + 0.5
        scale = [x_size, y_size, z_size]
        position = selected_obj.location

        # Add the results to a list
        results.append({"name": filename, "class": "OcclusionVolume", "persistentId": "", "__parent": "occluIPL", "position": list(position), "scale": scale})

        # Clear the scene after each import
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete

# Write the results to a JSON file
with open("results.json", "w") as f:
    for result in results:
        f.write(json.dumps(result, separators=(',', ':')) + ",\n")