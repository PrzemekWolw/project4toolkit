import bpy
import os
import mathutils

# Select all objects in the scene
bpy.ops.object.select_all(action='SELECT')

# Delete all selected objects
bpy.ops.object.delete()

# Set the active rendering engine to 'BLANK'

#this will convert the models position and rotation (w, x, y, z) quaternion by using the decrypted .wpl stream files. there is a known error here that in some fringe cases the w rotation is flipped positive when it should be negative, or vice versa. 

#it is possible that RAGE is making a correction on its own here, possibly by using the last two values of the .wpl, but it is unknown. implement a fix for the known flipped w rotations.

#most of these should be combined into one streamer for ease of use.
      
# Open the stream.txt file and read the lines
with open("stream.txt", "r") as stream:
    lines = stream.readlines()

# Iterate through each line in the file
for line in lines:
    # Split the line into a list of values
    values = line.split()

    # Extract the position and rotation values
    pos_x = float(values[0].replace(",", ""))
    pos_y = float(values[1].replace(",", ""))
    pos_z = float(values[2].replace(",", ""))
    rot_x = float(values[3].replace(",", ""))
    rot_y = float(values[4].replace(",", ""))
    rot_z = float(values[5].replace(",", ""))
    rot_w = float(values[6].replace(",", ""))
        
    # Convert the rotational values to a quaternion
    quat = mathutils.Quaternion((rot_w, rot_x, rot_y, rot_z))
    
    # Extract the name of the .dae file
    dae_name = (values[7].replace(",", ""))

    cwd = os.getcwd()
    # Construct the file path to the .dae file
    filepath = os.path.join(cwd, dae_name + ".dae")
    # Check if the .dae file exists
    if not os.path.exists(filepath):
        #print(".dae file not found:", dae_name)
        continue

    # Import the .dae file
    bpy.ops.wm.collada_import(filepath = os.path.join(cwd, dae_name + ".dae"))
    
    
    # Iterate over all the objects in the scene
    for obj in bpy.context.scene.objects:
    # Set the rotation mode to "QUATERNION"
        obj.rotation_mode = "QUATERNION"
    # Set the rotation to the quaternion value
        obj.rotation_quaternion = quat
        obj.location = (pos_x, pos_y, pos_z)
        
    # Set the export path for the modified .dae file
    export_path = os.path.join(cwd, dae_name + ".dae")
        
    # Export the object as a .dae file
    bpy.ops.wm.collada_export(filepath=export_path)
        
    # Remove the object from the scene
    bpy.ops.object.delete()
    
    
exec(open("lodbuilder.py").read())