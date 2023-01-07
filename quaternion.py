import bpy
import os
import mathutils

      
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

    # Check if the .dae file exists
    if not os.path.exists(os.path.join("C:/Users/user/Documents/quaternion tests/", dae_name + ".dae")):
        #print(".dae file not found:", dae_name)
        continue

    # Import the .dae file
    bpy.ops.wm.collada_import(filepath=os.path.join("C:/Users/user/Documents/quaternion tests/", dae_name + ".dae"))
    
    
    # Iterate over all the objects in the scene
    for obj in bpy.context.scene.objects:
    # Set the rotation mode to "QUATERNION"
        obj.rotation_mode = "QUATERNION"
    # Set the rotation to the quaternion value
        obj.rotation_quaternion = quat
        obj.location = (pos_x, pos_y, pos_z)
        
    # Set the export path for the modified .dae file
    export_path = os.path.join("C:/Users/user/Documents/quaternion tests/new", dae_name + ".dae")
        
    # Export the object as a .dae file
    bpy.ops.wm.collada_export(filepath=export_path)
        
    # Remove the object from the scene
    bpy.ops.object.delete()