import os
import bpy

# Delete all objects in the scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

working_dir = os.getcwd()

# Iterate over all .dae files in the working directory
for file in os.listdir(working_dir):
    if file.endswith(".dae"):
        file_path = os.path.join(working_dir, file)
        
        # Import COLLADA file
        bpy.ops.wm.collada_import(filepath=file_path)
        
        # Get reference to the imported object
        imported_obj = bpy.context.selected_objects[0]
        
        # Duplicate imported object
        bpy.context.view_layer.objects.active = imported_obj
        bpy.ops.object.duplicate()
        obj1 = bpy.context.selected_objects[0]
        obj1.name = imported_obj.name + "_a250"
        bpy.context.view_layer.objects.active = imported_obj
        bpy.ops.object.duplicate()
        obj2 = bpy.context.selected_objects[0]
        obj2.name = imported_obj.name + "_a130"
        
        # Add empty objects
        bpy.ops.object.empty_add(type='ARROWS', radius=1, location=(0, 0, 0))
        base00 = bpy.context.object
        base00.name = "base00"
        bpy.ops.object.empty_add(type='ARROWS', radius=1, location=(0, 0, 0))
        start01 = bpy.context.object
        start01.name = "start01"
        
        # Parent objects
        start01.parent = base00
        imported_obj.parent = start01
        obj1.parent = start01
        obj2.parent = start01
        
        # Decimate objects
for obj in bpy.data.objects:
    if "_a250" in obj.name:
        # Add Decimate modifier
        obj.modifiers.new("Decimate", type='DECIMATE')
        obj.modifiers["Decimate"].ratio = 0.75
        # Set the active object
        bpy.context.view_layer.objects.active = obj
        # Apply the Decimate modifier
        bpy.ops.object.modifier_apply(modifier="Decimate")
    elif "_a130" in obj.name:
        # Add Decimate modifier
        obj.modifiers.new("Decimate", type='DECIMATE')
        obj.modifiers["Decimate"].ratio = 0.5
        # Set the active object
        bpy.context.view_layer.objects.active = obj
        # Apply the Decimate modifier
        bpy.ops.object.modifier_apply(modifier="Decimate")
        
        # Export COLLADA file
        bpy.ops.wm.collada_export(filepath=file_path)
        
        # Delete all objects
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()