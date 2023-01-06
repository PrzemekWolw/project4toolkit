import bpy
import os

# Open the stream.txt file and read the lines
with open("stream.txt", "r") as stream:
    lines = stream.readlines()

# Iterate through each line in the file
for line in lines:
    # Split the line into a list of values
    values = line.split()

    # Extract the position and rotation values
    pos_x = float(values[0])
    pos_y = float(values[1])
    pos_z = float(values[2])
    rot_x = float(values[3])
    rot_y = float(values[4])
    rot_z = float(values[5])

    # Extract the name of the .dae file
    dae_name = (values[7])

    # Check if the .dae file exists
    if not os.path.exists(os.path.join("/path/to/folder/", dae_name)):
        print(".dae file not found:", dae_name)
        continue

    # Import the .dae file
    bpy.ops.wm.collada_import(filepath=os.path.join("/path/to/folder/", dae_name))

    # Select the imported object
    obj = bpy.context.selected_objects[0]

    # Set the position and rotation of the object
    obj.location = (pos_x, pos_y, pos_z)
    obj.rotation_euler = (rot_x, rot_y, rot_z)