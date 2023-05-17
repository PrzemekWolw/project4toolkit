import bpy
import os
import numpy as np

texture_folder = os.path.expanduser('~/Documents/ac-test/texture/')
placeholder_path = os.path.join(texture_folder, 'placeholder.png')

# Create a black placeholder image and save it to a file
placeholder_image = bpy.data.images.new("placeholder", width=1, height=1)
pixels = np.zeros((1, 1, 4), dtype=np.float32)
placeholder_image.pixels.foreach_set(pixels.ravel())
placeholder_image.filepath_raw = placeholder_path
placeholder_image.file_format = 'PNG'
placeholder_image.save()
placeholder_image.pack()

# Iterate through all materials in the scene
for material in bpy.data.materials:
    if not material.use_nodes:
        material.use_nodes = True

    tree = material.node_tree

    texture_nodes = [node for node in tree.nodes if node.type == 'TEX_IMAGE']
    for node in texture_nodes:
        tree.nodes.remove(node)

    texture_node = tree.nodes.new(type='ShaderNodeTexImage')

        # Create the path of the new texture
    if not material.name.endswith(".dds"):
        texture_path = os.path.join(texture_folder, material.name + ".dds")
    else:
        texture_path = os.path.join(texture_folder, material.name)


    # Load the image if it exists
    if os.path.exists(texture_path):
        try:
            texture_image = bpy.data.images.load(filepath=texture_path)
            texture_image.pack()  # Pack the image
        except RuntimeError:
            print(f'Failed to load texture for {material.name} from {texture_path}')
            texture_image = placeholder_image  # Use placeholder image if loading fails
    else:
        print(f'No texture found for {material.name} at {texture_path}')
        texture_image = placeholder_image  # Use placeholder image if none found

    texture_node.image = texture_image

    bsdf_node = tree.nodes.new('ShaderNodeBsdfPrincipled')

    tree.links.new(texture_node.outputs['Color'], bsdf_node.inputs['Base Color'])

    output_node = [node for node in tree.nodes if node.type == 'OUTPUT_MATERIAL'][0]

    tree.links.new(bsdf_node.outputs['BSDF'], output_node.inputs['Surface'])
