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
    pos_x = float(values[0].replace(",", ""))
    pos_y = float(values[1].replace(",", ""))
    pos_z = float(values[2].replace(",", ""))
    rot_x = float(values[3].replace(",", ""))
    rot_y = float(values[4].replace(",", ""))
    rot_z = float(values[5].replace(",", ""))

    # Extract the name of the .dae file
    dae_name = (values[7].replace(",", ""))

    # Check if the .dae file exists
    if not os.path.exists(os.path.join("C:/Users/user/Downloads/P4Toolkit/", dae_name + ".dae")):
        print(".dae file not found:", dae_name)
        continue

    # Import the .dae file
    bpy.ops.wm.collada_import(filepath=os.path.join("C:/Users/user/Downloads/P4Toolkit/", dae_name + ".dae"))

    # Select the imported object
    obj = bpy.context.selected_objects[0]
    def replace_material(bad_mat, good_mat):
        bad_mat.user_remap(good_mat)
        bpy.data.materials.remove(bad_mat)
        
        
    def get_duplicate_materials(og_material):
        
        common_name = og_material.name
        
        if common_name[-3:].isnumeric():
            common_name = common_name[:-4]
        
        duplicate_materials = []
        
        for material in bpy.data.materials:
            if material is not og_material:
                name = material.name
                if name[-3:].isnumeric() and name[-4] == ".":
                    name = name[:-4]
                
                if name == common_name:
                    duplicate_materials.append(material)
        
        text = "{} duplicate materials found"
        print(text.format(len(duplicate_materials)))
        
        return duplicate_materials


    def remove_all_duplicate_materials():
        i = 0
        while i < len(bpy.data.materials):
            
            og_material = bpy.data.materials[i]
            
            print("og material: " + og_material.name)
            
            # get duplicate materials
            duplicate_materials = get_duplicate_materials(og_material)
            
            # replace all duplicates
            for duplicate_material in duplicate_materials:
                replace_material(duplicate_material, og_material)
            
            # adjust name to no trailing numbers
            if og_material.name[-3:].isnumeric() and og_material.name[-4] == ".":
                og_material.name = og_material.name[:-4]
                
            i = i+1
        
        
    # Set the position and rotation of the object
    obj.location = (pos_x, pos_y, pos_z)
    obj.rotation_euler = (rot_x, rot_y, rot_z)
    
    
    
    # Set the export path for the modified .dae file
    export_path = os.path.join("C:/Users/user/Downloads/P4Toolkit/", dae_name + ".dae")
        
    # Export the object as a .dae file
    bpy.ops.wm.collada_export(filepath=export_path)
        
    # Remove the object from the scene
    bpy.ops.object.delete()