import bpy
import os

# Get a list of .dae files in the working directory
dae_files = [f for f in os.listdir('.') if f.endswith('.dae')]

# Loop through the .dae files
for dae_file in dae_files:
    # Import the .dae file
    bpy.ops.wm.collada_import(filepath=dae_file)

    # Deselect all objects in the scene
    bpy.ops.object.select_all(action='DESELECT')

    # Select the non-decimated mesh
    bpy.ops.object.select_pattern(pattern="mesh_name")

    # Get the selected mesh object
    mesh = bpy.context.selected_objects[0]

    # Create a copy of the mesh with 25% decimation
    mesh_copy = bpy.data.objects.new(name="Low Detail", object_data=mesh.data)
    bpy.context.collection.objects.link(mesh_copy)
    bpy.ops.object.select_all(action='DESELECT')
    mesh_copy.select_set(True)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.decimate(ratio=0.75)
    bpy.ops.object.mode_set(mode='OBJECT')

    # Add a material slot to the duplicated mesh
    bpy.ops.object.material_slot_add()

    # Create a new material and assign it to the slot
    material = bpy.data.materials.new(name="LOD")
    mesh_copy.material_slots[0].material = material

    # Rename the duplicated mesh
    mesh_copy.name = "Imported Mesh_a250"

    # Create another copy of the mesh with 50% decimation
    mesh_copy2 = bpy.data.objects.new(name="Very Low Detail", object_data=mesh.data)
    bpy.context.collection.objects.link(mesh_copy2)
    bpy.ops.object.select_all(action='DESELECT')
    mesh_copy2.select_set(True)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.decimate(ratio=0.50)
    bpy.ops.object.mode_set(mode='OBJECT')
    # Add a material slot to the duplicated mesh
    bpy.ops.object.material_slot_add()

    # Create a new material and assign it to the slot
    material = bpy.data.materials.new(name="LOD")
    mesh_copy2.material_slots[0].material = material

    # Rename the duplicated mesh
    mesh_copy2.name = "Imported Mesh_a130"

    # Create the base00 empty
    base00 = bpy.data.objects.new(name="base00", object_data=None)
    bpy.context.collection.objects.link(base00)

    # Create the start01 empty
    start01 = bpy.data.objects.new(name="start01", object_data=None)
    bpy.context.collection.objects.link(start01)

    # Parent start01 to base00
    start01.parent = base00

    # Parent the meshes to start01
    mesh.parent = start01
    mesh_copy.parent = start01
    mesh_copy2.parent = start01

    # Export the scene as a .dae file, overwriting the original
    bpy.ops.wm.collada_export(filepath=dae_file)

    # Delete all objects in the scene
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()