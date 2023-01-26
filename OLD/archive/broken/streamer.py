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

        
    # Create a quaternion from the rotation values
    rot_quat = mathutils.Quaternion((rot_w, rot_x, rot_y, rot_z,))
    
    # Extract the name of the .dae file
    dae_name = (values[7].replace(",", ""))

    print("pos_x:", pos_x)
    print("pos_y:", pos_y)
    print("pos_z:", pos_z)
    print("rot_x:", rot_x)
    print("rot_y:", rot_y)
    print("rot_z:", rot_z)
    print("rot_w:", rot_w)
    print("rot_quat:", rot_quat)
    print("dae_name:", dae_name)
    # Check if the .dae file exists
    if not os.path.exists(os.path.join("C:/Users/user/Downloads/P4Toolkit/", dae_name + ".dae")):
        #print(".dae file not found:", dae_name)
        continue

    # Import the .dae file
    bpy.ops.wm.collada_import(filepath=os.path.join("C:/Users/user/Downloads/P4Toolkit/", dae_name + ".dae"))
    
    
    # Get a list of all the imported objects
    obj = bpy.context.selected_objects[0]
    
    obj.rotation_mode = "QUATERNION"
    obj.location = (pos_x, pos_y, pos_z)
    obj.rotation_quaternion = (rot_quat)
       
    print("pos_x:", pos_x)
    print("pos_y:", pos_y)
    print("pos_z:", pos_z)
    print("rot_x:", rot_x)
    print("rot_y:", rot_y)
    print("rot_z:", rot_z)
    print("rot_w:", rot_w)
    print("rot_quat:", rot_quat)
    print("dae_name:", dae_name)  
    # Set the export path for the modified .dae file
    export_path = os.path.join("C:/Users/user/Downloads/P4Toolkit/", dae_name + ".dae")
        
    # Export the object as a .dae file
    bpy.ops.wm.collada_export(filepath=export_path)
        
    # Remove the object from the scene
    bpy.ops.object.delete()