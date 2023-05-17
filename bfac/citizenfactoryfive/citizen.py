import bpy
import os
import xml.etree.ElementTree as ET

cwd = os.getcwd() 
xml_file = 'stream.xml'  

# parse the XML file and apply positions and quaternion rotations
tree = ET.parse(os.path.join(cwd, xml_file))
root = tree.getroot()

for item in root.iter('Item'):
    if item.get('type') == 'CEntityDef':
        archetype_name = item.find('archetypeName').text
        dae_file = os.path.join(cwd, archetype_name + '.dae')
        if os.path.exists(dae_file):
            position = item.find('position').attrib
            rotation = item.find('rotation').attrib
         
            bpy.ops.wm.collada_import(filepath=dae_file)
            obj = bpy.context.selected_objects[0]
            obj.location = (float(position['x']), float(position['y']), float(position['z']))
            obj.rotation_mode = "QUATERNION"
            obj.rotation_quaternion = (float(rotation['w']), float(rotation['x']), float(rotation['y']), float(rotation['z']))
            bpy.ops.wm.collada_export(filepath=dae_file, check_existing=False, apply_modifiers=True)
            bpy.ops.object.select_all(action='SELECT')
            bpy.ops.object.delete()

def script4_function():
    print("Assigning Materials")

script4_function()

import bpy
import os

def find_base_color_node(mat):
    try:
        for node in mat.node_tree.nodes:
            if node.type == 'BSDF_PRINCIPLED':
                break

        return node.inputs["Base Color"].links[0].from_node
        
    except Exception:
        return None

def get_node_name(node):
    try:
        return node.label or node.image.name
    except Exception:
        return None

def convert_dae_file(filepath):
    print(f"Converting {filepath}...")
    bpy.ops.wm.collada_import(filepath=filepath)
    mat_names = [
        mat.name for mat in bpy.data.materials
        if mat.name.startswith("MAT")
    ]

    for mat_name in mat_names:
        mat = bpy.data.materials[mat_name]
        node = find_base_color_node(mat)
        if new_name := get_node_name(node):
            mat.name = new_name

    filepath_dst = os.path.splitext(filepath)[0] + ".dae"
    bpy.ops.wm.collada_export(filepath=filepath_dst)
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

def convert_recursive(base_path):
    for entry in os.scandir(base_path):
        if entry.is_file() and entry.name.endswith('.dae'):
            convert_dae_file(entry.path)
        elif entry.is_dir():
            convert_recursive(entry.path)

convert_recursive(os.getcwd())


def script5_function():
    print("Cleaning Materials")

# This just works better than attempting material cleaning in Blender, and saves an import. The re.sub for .XXXX is really only used when I test collision dictionaries for now, but when native collision support is added this will come in handy.
import os
import re

cwd = os.getcwd()
for file in os.listdir(cwd):
    if file.endswith(".dae"):
        with open(os.path.join(cwd, file), "r") as f:
            lines = f.readlines()
        with open(os.path.join(cwd, file), "w") as f:
            for line in lines:
                line = re.sub(r'_\d+-material', '-material', line)
                line = re.sub(r'\.\d+">', '">', line)
                line = re.sub(r'\.png', '', line)  # Remove ".png" from the lines
                f.write(line)
