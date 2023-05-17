def script0_function():
    print("Moving Textures")


import os
import shutil
from pathlib import Path

# hacky way of fixing the bug where bpy will endlessly duplicate the textures on an export. bpy removed the export textures false flag, so only fix for now. 
target_folder = '../map'
Path(target_folder).mkdir(exist_ok=True)

for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.dds'):
            source_file = os.path.join(root, file)
            destination_file = os.path.join(target_folder, file)
            shutil.move(source_file, destination_file)
            print(f"Moved {source_file} to {destination_file}")



def script1_function():
    print("Exploding WDDs")
# This script remaps the WDD mesh dictionary to individual WDR meshes, each with their own real material maps. Once it unpacks the dictionary it will continue converting them as normal.
# Allow the user to choose the option to build a "low-spec" map if they have an older PC, that script will only let them use WDD models for their entire map, and then build LODs for those LODs to make it even more performant.

import os

odd_files = [f for f in os.listdir('.') if f.endswith('.odd')]

for odd_file in odd_files:
    with open(odd_file, 'r') as f:
        contents = f.read()

    blocks = contents.split('gtaDrawable')
# this is HORRIBLE, it works but please fix this disaster at some point
    for block in blocks:
        if 'lodgroup' in block:
            drawable_name = block.split('\n')[0].strip()
            shading_group = block.split('shadinggroup')[1].strip()
            shading_group = shading_group.split('}}')[0].strip() + '\n}\n}'
            lod_group = block.split('lodgroup')[1].strip()
            lod_group = lod_group.split('}')[0].strip()
            with open(f'{drawable_name}.odr', 'w') as f:
                shading_group_lines = shading_group.split("\n")
                shading_group_lines = [line[2:] for line in shading_group_lines] 
                shading_group = "\n".join(shading_group_lines)
                lod_group_lines = lod_group.split("\n")
                lod_group_lines = [line[2:] for line in lod_group_lines]
                lod_group = "\n".join(lod_group_lines)
                f.write(f'version 110 12\nshadinggroup\n{{{shading_group}}}')

################################################################

def script11_function():
    print("Checking WDRs")

import os
import re

cwd = os.getcwd()

extensions = [".odr", ".mesh"]
keywords = ["emis", "weed", "glue", "gloo", "emmis", "nite", "emiss", "pedpost", "ropetyre", "glu", "seast", "seabed", "puerto", "pathpatch", "_nl_", "detail", "_det_", "_glue_", "night", "weeds", "em", "_glue", "canopys", "_det"]
#purging models that add detail not necessary for this type of game, only slows down loading times with little return keeping them.
for root, dirs, files in os.walk(cwd):
    for filename in files:
        if any(ext.lower() in filename.lower() for ext in extensions) and any(re.search(keyword, filename, re.IGNORECASE) for keyword in keywords):
            file_path = os.path.join(root, filename)
            os.remove(file_path)
            print(f"Deleted file: {file_path}")



            
def script2_function():
    print("Checking WDRs")

# This will not work for collision dictionaries currently as their structure is unlike libraries (.wdb) or main meshes (.wdr). For BeamNG you will want this for sticky barriers that are fixed by the wider meshes contained there, also allows tiremark support and lag improvements when implemented.
# Best way to do collisions here is just pick one model per zone and attach the entire collision file under Start01 for just one of them. This worked in the original version of the mod and will work just as well when implemented here.
import os
import re
import sys
import bpy
import mathutils

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()


for entry in os.scandir("."):
    if entry.is_file() and entry.name.endswith(".odr"):
        with open(entry.path, "r") as f:
            print('Indexing...')
                  
class Vertex:
    index = 0
    coordinates = [0, 0, 0]
    normal = [0, 0, 0]
    uv = [0, 0, 0]

    def __init__(self, index, coordinates, normal, uv) -> None:
        self.index = index
        self.coordinates = coordinates
        self.normal = normal
        self.uv = uv
    
    def get_v(self):
        coordinates = [str(coord) for coord in self.coordinates]
        return "v " + " ".join(coordinates)
    
    def get_vn(self):
        normal = [str(norm) for norm in self.normal]
        return "vn " + " ".join(normal)
    
    def get_vt(self):
        uv = [str(uv_coord) for uv_coord in self.uv]
        return "vt " + " ".join(uv)
    
    def get_index(self):
        return self.index

class Face:
    vertices = []

    def __init__(self, vertices) -> None:
        self.vertices = vertices
    

    def get_f(self):
        return "f " + " ".join(
            [
                f"{str(vert.get_index() + 1)}/{str(vert.get_index() + 1)}/{str(vert.get_index() + 1)}"
                for vert in self.vertices
            ]
        )

class Mesh:
    index = 0
    vertex_offset = 0
    idx_data = []
    vert_data = []

    vertices = []
    faces = []
    material = None

    def __init__(self, index) -> None:
        self.index = index
        self.vertex_offset = 0
        self.idx_data = []
        self.vert_data = []
        self.vertices = []
        self.faces = []
    
    def set_vertex_offset(self, vertex_offset) -> None:
        self.vertex_offset = vertex_offset
    
    def add_idx(self, data) -> None:
        for id in data:
            self.idx_data.append(int(id))
    
    def add_vert(self, data) -> None:
        self.vert_data.append(data)
    
    def generate(self) -> None:
        vert_index = self.vertex_offset

        
        for raw_vert in self.vert_data:
            coord = raw_vert.split(" / ")[0].split(" ")
            for i in range(len(coord)):
                coord[i] = float(coord[i])
            
            normal = raw_vert.split(" / ")[1].split(" ")
            for i in range(len(normal)):
                normal[i] = float(normal[i])
            
            uv = raw_vert.split(" / ")[3].split(" ")
            if len(uv) != 2:
                uv = raw_vert.split(" / ")[4].split(" ")
            uv[0] = float(uv[0])
            uv[1] = -float(uv[1])
           # something is wrong here?
            
            vertex = Vertex(vert_index, coord, normal, uv)
            self.vertices.append(vertex)
            vert_index += 1

        for i in range(0, len(self.idx_data), 3):
            v1 = self.vertices[self.idx_data[i]]
            v2 = self.vertices[self.idx_data[i + 1]]
            v3 = self.vertices[self.idx_data[i + 2]]

            face = Face([v1, v2, v3])
            self.faces.append(face)

class Material:
    name = ""
    Ka = [0, 0, 0]
    Kd = [0, 0, 0]
    Ks = [0, 0, 0]
    Ns = 0
    Ni = 0
    d = 0
    illum = 0
    map_Kd = ""
    map_bump = ""
    map_Ks = ""

    def __init__(self, name) -> None:
        self.name = name
        self.Ka = [0, 0, 0]
        self.Kd = [0, 0, 0]
        self.Ks = [0, 0, 0]
        self.Ns = 0
        self.Ni = 0
        self.d = 0
        self.illum = 0
        self.map_Kd = ""
        self.map_bump = ""
        self.map_Ks = ""
    
    def generate(self):
        if len(self.name) == 0:
            return ""

        mtl = ""
        mtl += f"newmtl {self.name}" + "\n"
        if len(self.map_Kd) > 0:
            mtl += f"map_Kd {self.map_Kd}" + "\n"
        if len(self.map_bump) > 0:
            mtl += f"map_bump {self.map_bump}" + "\n"
        if len(self.map_Ks) > 0:
            mtl += f"map_Ks {self.map_Ks}" + "\n"
        mtl += "\n"
        return mtl

class MaterialParser:
    shaders = []
    def __init__(self, raw_shader_list) -> None:
        self.shaders = raw_shader_list
    
    def generate(self):
        materials = []

        for index, shader in enumerate(self.shaders):
            material = Material(f"MAT_{str(index)}")
            material.map_Kd = shader
            materials.append(material)
        return materials

class MeshParser:
    mesh_file_lines = ""
    meshes = []
    materials = []

    def __init__(self, mesh_filepath, materials) -> None:
        self.meshes = []
        self.materials = materials

        with open(mesh_filepath) as f:
            self.mesh_file_lines = f.read()
    
    def generate(self, debug):
        self.mesh_file_lines = re.sub(r"\t", "", self.mesh_file_lines)
        depth = 0
        mesh = None
        in_idx = -1
        in_verts = -1

        mesh_index = -1
        for line in self.mesh_file_lines.splitlines():
            if "{" in line:
                depth += 1
            if "}" in line:
                depth -= 1

            if "mtl" in line.lower() or "geometry" in line.lower():
                
                if mesh is not None:
                    self.meshes.append(mesh)

                
                mesh_index += 1
                mesh = Mesh(mesh_index)
                try:
                    mesh.material = self.materials[mesh_index]
                except Exception:
                    pass


            if "idx" in line.lower() or "indices" in line.lower():
                in_idx = depth + 1
                continue

            if "verts" in line.lower() or "vertices" in line.lower():
                in_verts = depth + 1
                continue

            if in_idx > 0:
                if depth < in_idx:
                    in_idx = -1
                if "{" not in line and "}" not in line:
                    mesh.add_idx(line.split(" "))

            if in_verts > 0:
                if depth < in_verts:
                    in_verts = -1
                if "{" not in line and "}" not in line:
                    mesh.add_vert(line)

        if mesh is not None:
            self.meshes.append(mesh)

        for i in range(len(self.meshes)):
            if i == 0:
                self.meshes[i].set_vertex_offset(0)
            else:
                index = i
                offset = 0
                while index > 0:
                    index -= 1
                    offset += len(self.meshes[index].vert_data)
                self.meshes[i].set_vertex_offset(offset)

        for mesh in self.meshes:
            mesh.generate()

        obj = ""

        for mesh in self.meshes:
            for vert in mesh.vertices:
                obj += vert.get_v() + "\n"

        for mesh in self.meshes:
            for vert in mesh.vertices:
                obj += vert.get_vn() + "\n"

        for mesh in self.meshes:
            for vert in mesh.vertices:
                obj += vert.get_vt() + "\n"

        for mesh in self.meshes:
            if mesh.material is not None:
                obj += f"usemtl {mesh.material.name}" + "\n"
            for face in mesh.faces:
                obj += face.get_f() + "\n"

        vert_count = 0
        face_count = 0
        material_count = 0
        for mesh in self.meshes:
            vert_count += len(mesh.vertices)
            face_count += len(mesh.faces)
            material_count += 1 if mesh.material is not None else 0

        mtl = "".join(material.generate() for material in self.materials)
        return {"obj": obj, "mtl": mtl}

def parse_odr(lines):
    odr_data = {"shaders": [], "skeletons": [], "lodgroup": {}}

    shadinggroups = []
    skeletons = ""

    regex_shadinggroup = r"(s|S)hadinggroup(\n|\s|){\n\t{0,1}(s|S)haders \d{1,999}\n\t{0,1}{\n\t{2}[^}]+}\n}"

    if match_shadinggroup := re.search(regex_shadinggroup, lines):
        tmp_shadinggroups = match_shadinggroup[0]
        tmp_shadinggroups = re.sub(r"(s|S)hadinggroup(\n|\s|){\n\t{0,1}(s|S)haders \d{1,999}\n\t{0,1}{\n", "", tmp_shadinggroups)
        tmp_shadinggroups = re.sub(r"\n\t{0,2}}\n}", "", tmp_shadinggroups)
        tmp_shadinggroups = re.sub(r"\t", "", tmp_shadinggroups)
        tmp_shadinggroups = re.sub(r"\\", "/", tmp_shadinggroups)

        if len(tmp_shadinggroups) > 0:
            for shadinggroup in tmp_shadinggroups.splitlines():
                try:
                    shadinggroups.append(shadinggroup.split(" ")[1])
                except Exception:
                    pass

    if not shadinggroups:
        sps_data = []
        depth = 0
        sps_name = ""
        in_shaders = -1

        previous_line = ""

        for line in lines.splitlines():
            if "{" in line:
                depth += 1
            if "}" in line:
                depth -= 1

            if "shaders" in line.lower():
                in_shaders = depth + 1
                continue

            if depth < in_shaders:
                in_shaders = -1

            if in_shaders != -1:
                if "{" in line and "{" not in previous_line:
                    sps_name = re.sub(r"\t", "", previous_line)
                if "}" in line and len(sps_name) > 0:
                    sps_name = ""

                if (
                    len(sps_name) > 0
                    and "{" not in line
                    and "DiffuseSampler" in line
                ):
                    sps_data.append(re.sub(r"\\", "/", re.sub(line.split(" ")[0], "", line).lstrip()).replace(".otx", ".png"))
            previous_line = line
        shadinggroups = sps_data
    regex_skeletons = r"(s|S)kel(eton|)((\n|\s|){\n\t{0,1}[\w\.\s\t\\\-]+\n}|[ \w\\\.\d\-]+)"

    if match_skeletons := re.search(regex_skeletons, lines):
        skeletons = match_skeletons[0]
        skeletons = re.sub(r"(s|S)kel(eton|)(\n|\s|) {*", "", skeletons)
        skeletons = re.sub(r"\n}", "", skeletons)
        skeletons = re.sub(r"\t", "", skeletons)
        skeletons = re.sub(r"\\", "/", skeletons)

    new_skeletons = [
        skel
        for skel in skeletons.splitlines()
        if skel.lower().endswith(".skel")
    ]
    skeletons = new_skeletons
    depth = 0
    in_lodgroup = -1
    lodgroup_lines = []

    for line in lines.splitlines():
        if "{" in line:
            depth += 1
        if "}" in line:
            depth -= 1

        if "lodgroup" in line.lower():
            in_lodgroup = depth + 1
            continue

        if in_lodgroup != -1:
            if depth < in_lodgroup:
                in_lodgroup = -1

            lodgroup_lines.append(line)

    lodgroup_lines = "\n".join(lodgroup_lines)
    regex_lod = r"(((h|H)igh)|((m|M)ed)|((l|L)ow)|((v|V)low)) [\d\.\w \\\-]+(\n\t+{\n\t+[\w\\\. \d]+\n\t+})*"
    # This is not needed for GTAIV, since no .wdr is actually assigned anything other than High (mesh), only for GTAV does Med or Low actually get used. If building a seperate script entirely for GTAV, just cut this regex down to just High for speed improvement.
    if match_lod := re.finditer(regex_lod, lodgroup_lines):
        for o in [x.group() for x in match_lod]:
            lod_type = o.split(" ")[0].lower()
            lod_value = ""
            if "{" in o:
                for t in o.split("\t"):
                    for tt in t.split(" "):
                        if tt.lower().endswith(".mesh"):
                            lod_value = re.sub(r"\\", "/", tt)
                            break
            else:
                for t in o.split(" "):
                    if t.lower().endswith(".mesh"):
                        lod_value = re.sub(r"\\", "/", t)
                        break

            if len(lod_value) > 0:
                odr_data["lodgroup"][lod_type] = lod_value


    if shadinggroups:
        odr_data["shaders"] = shadinggroups

    if skeletons:
        odr_data["skeletons"] = skeletons

    return odr_data


for dir_entry in os.scandir("."):
    if dir_entry.is_file() and dir_entry.name.endswith(".odr"):
            input_file_path = dir_entry.path
            input_name, ext = os.path.splitext(os.path.basename(input_file_path))
            with open(input_file_path, "r") as f:
                raw_odr_lines = f.read()
                odr_data = parse_odr(raw_odr_lines)

            for lodgroup in odr_data["lodgroup"]:
                output_obj_name = f"{input_name}.obj"
                output_mtl_name = f"{input_name}.mtl"

                material_parser = MaterialParser(odr_data["shaders"])
                mesh_parser = MeshParser(odr_data["lodgroup"][lodgroup], material_parser.generate())

                model_data = mesh_parser.generate(True)

                obj_headers = "# bng\n\n"
                obj_headers += f"mtllib {output_mtl_name}\n\n"

                mtl_headers = "# bng\n\n"

                model_data["obj"] = obj_headers + model_data["obj"]
                model_data["mtl"] = mtl_headers + model_data["mtl"]

                with open(output_obj_name, "w") as f:
                    f.write(model_data["obj"])

                with open(output_mtl_name, "w") as f:
                    f.write(model_data["mtl"])
                print(output_obj_name)

CONVERT_DIR = os.getcwd()

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()
# This could just be fixed in the .obj export, but for now this works so I am not changing it.
# or just subprocess this, but for some reason pushing it to sbp makes it not work correctly, neither does batching before doing this. for some reason this part of the script is permalinked to this section lol, please fix
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
# on the obj export the material name is never actually the material name, it gets pushed to the basecolor name, here we are moving it up to the BDSF
def convert_recursive(base_path):
    for entry in os.scandir(base_path):
        if entry.is_file() and entry.name.endswith('.obj'):
                filepath_src = entry.path
                filepath_dst = f"{os.path.splitext(filepath_src)[0]}.dae"

                print("Converting Meshes...")
                bpy.ops.import_scene.obj(filepath=filepath_src)
                mat_names = [
                    mat.name for mat in bpy.data.materials
                    if mat.name.startswith("MAT")
                ]

                for mat_name in mat_names:
                    mat = bpy.data.materials[mat_name]
                    node = find_base_color_node(mat)
                    if new_name := get_node_name(node):
                        mat.name = new_name
                bpy.ops.wm.collada_export(filepath=filepath_dst)
                bpy.ops.object.select_all(action='SELECT')
                bpy.ops.object.delete()

if __name__ == "__main__":
    convert_recursive(CONVERT_DIR)

def script3_function():
    print("Converting Quaternions")


import bpy
import os
import mathutils

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

#This will convert the models position and rotation (w, x, y, z) quaternion by using the .wpl stream files. 
with open("stream.p4tkpl", "r") as stream:
    lines = stream.readlines()

for line in lines:
    values = line.split()

    # Extract the position and rotation values from .wpl. RAGE uses Euler for position and quaternion for its rotations, it is also possible to convert to a rotation matrix that T3D would understand since it does not currently support .json quaternion to my knowledge. If the mechanism for doing so can be found, error correction for W need not be implemented.
    # WDD dictionaries when exploded still use this format in the WPL, it is just contained in the non '_stream' WPLs. You cannot remove the '_stream' WPLs for the script using just the LODs as R* sometimes includes LOD positions in the stream.
    pos_x = float(values[0].replace(",", ""))
    pos_y = float(values[1].replace(",", ""))
    pos_z = float(values[2].replace(",", ""))
    rot_x = float(values[3].replace(",", ""))
    rot_y = float(values[4].replace(",", ""))
    rot_z = float(values[5].replace(",", ""))
    rot_w_str = values[6].replace(",", "")
    rot_w = -float(rot_w_str[1:]) if rot_w_str[0] == "-" else float(rot_w_str)
    quat = mathutils.Quaternion((rot_w, rot_x, rot_y, rot_z))
    dae_name = (values[7].replace(",", ""))

    cwd = os.getcwd()
    filepath = os.path.join(cwd, f"{dae_name}.dae")
    if not os.path.exists(filepath):
        continue

    bpy.ops.wm.collada_import(filepath=os.path.join(cwd, f"{dae_name}.dae"))

    for obj in bpy.context.scene.objects:
        obj.rotation_mode = "QUATERNION"
        obj.rotation_quaternion = quat
        # fix for the above quat bug is forcing all non w=1 quats to a negative, even if the engine does not consider them as such. this works for all models and fixes the rotation bug.
        obj.rotation_quaternion.w *= -1
        obj.location = (pos_x, pos_y, pos_z)

    export_path = os.path.join(cwd, f"{dae_name}.dae")

    bpy.ops.wm.collada_export(filepath=export_path)
    bpy.ops.object.delete()

    print(dae_name)
    print(pos_x, pos_y, pos_z)
    print(quat)

################################################################
def script4_function():
    print("Merging LODs")

import bpy
import os


bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

path = os.getcwd()

filename = input("Enter the name of the zone you are exporting (without the .idx extension): ")
filename += ".idx"
with open(filename, 'r') as f:
    lines = f.readlines()

for line in lines:
    models = [model.lower() for model in line.strip().split(', ')]
    model1, model2, model3 = models[0], models[1], models[2]
# if we are linking 4+ models, these should probably be pushed to _a1500 and _a750 
    if not os.path.exists(os.path.join(path, model1 + '.dae')):
        continue
    
    # Import LOD0 and set it to the highest pixel density
    bpy.ops.wm.collada_import(filepath=os.path.join(path, model1 + '.dae'))
    obj1 = bpy.context.selected_objects[0]
    obj1.name = obj1.name + '_a1000'
    
    
    if os.path.exists(os.path.join(path, model2 + '.dae')):
        # Import LOD1 if it exists and set it to the second highest pixel density
        bpy.ops.wm.collada_import(filepath=os.path.join(path, model2 + '.dae'))
        obj2 = bpy.context.selected_objects[0]
        obj2.name = obj2.name + '_a500'
    else:
        # If it doesn't exist, create a nulldetail to deload it
        null_obj2 = bpy.data.objects.new('nulldetail500', None)
        bpy.context.scene.collection.objects.link(null_obj2)
        null_obj2.location = (0, 0, 0)
        obj2 = null_obj2
    
    
    merged_filename = model1.capitalize() + '_merged.dae'
    bpy.ops.wm.collada_export(filepath=os.path.join(path, merged_filename))
    
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

# merged file originals are deleted, this allows us to find models that have no index level
    if os.path.exists(os.path.join(path, model1 + '.dae')):
        os.remove(os.path.join(path, model1 + '.dae'))
    else:
        continue
    if os.path.exists(os.path.join(path, model2 + '.dae')):
        os.remove(os.path.join(path, model2 + '.dae'))
    else:
        continue

################################################################

def script5_function():
    print("Linking Models")

# this nightmare script is merging the 4 closest models using the p4tkpl placement list based on their XYZ position. if t3d didnt suck, and could actually instance objects like a normal engine, this would not need to be done.
# so long as each mesh has the exact same _aXXX lod values, they can all work packed into one.
# this whole thing is done to improve loading times, the less instancing of individual .dae, the faster this all goes. By going 4:1, we can bring load times down significantly, and this will unlock potential for having the entire map load in a few minutes instead of hours.
import os
import math
import bpy
def calculate_distance(pos1, pos2):
    return math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2 + (pos1[2] - pos2[2])**2)
object_positions = {}
cwd = os.getcwd()
dae_files = [f.replace('_merged.dae', '').lower() for f in os.listdir(cwd) if f.endswith('_merged.dae')]
with open("stream.p4tkpl", "r") as stream:
    lines = stream.readlines()
for line in lines:
    values = line.split()
    dae_name = values[7].replace(",", "").strip().lower() 
    if dae_name in dae_files:
        pos_x = float(values[0].replace(",", ""))
        pos_y = float(values[1].replace(",", ""))
        pos_z = float(values[2].replace(",", ""))
        object_positions[dae_name] = (pos_x, pos_y, pos_z)
quartet_objects = set()
quartet_count = 0 
for name1, pos1 in object_positions.items():
    if name1 in quartet_objects:
        continue
    closest_names = []
    closest_distances = [float('inf')] * 3
    for name2, pos2 in object_positions.items():
        if name1 == name2 or name2 in quartet_objects:
            continue
        distance = calculate_distance(pos1, pos2)
        for i in range(3):
            if distance < closest_distances[i]:
                closest_distances.insert(i, distance)
                closest_names.insert(i, name2)
                if len(closest_distances) > 3:
                    closest_distances.pop()
                if len(closest_names) > 3:
                    closest_names.pop()
                break
    if len(closest_names) == 3:
        quartet_objects.add(name1)
        quartet_objects.update(closest_names)
        quartet_count += 1
        for name in [name1] + closest_names:
            bpy.ops.wm.collada_import(filepath=os.path.join(cwd, name + "_merged.dae"))
        bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0))
        base00 = bpy.context.object
        base00.name = "base00"
        bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0))
        start01 = bpy.context.object
        start01.name = "start01"
        start01.parent = base00
        bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0))
        nulldetail50 = bpy.context.object
        nulldetail50.name = "nulldetail50"
        nulldetail50.parent = start01
        nulldetail500 = bpy.data.objects.get("nulldetail500")
        if nulldetail500:
            nulldetail500.parent = start01
        for obj in bpy.context.scene.objects:
            if obj.type == 'MESH':
                obj.parent = start01
        bpy.ops.wm.collada_export(filepath=os.path.join(cwd, f"{name1}_{closest_names[0]}_{closest_names[1]}_{closest_names[2]}_linked.dae"))
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete(use_global=False)

###########################


def script6_function():
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
                f.write(line)

################################################################

def script7_function():
    print("Moving Files")


import os
import shutil

cwd = os.getcwd()

delete_types = ['.obj', '.mtl', '.odr', '.mesh', '.odd', '.otd']

for item in os.listdir(cwd):
    item_path = os.path.join(cwd, item)
    if os.path.isfile(item_path):
        if any(item.endswith(x) for x in delete_types):
            os.remove(item_path)
        elif item.lower().endswith(".dae") and ("slod" in item.lower() or "lod" in item.lower() or "merged" in item.lower()):
            os.remove(item_path)
    elif os.path.isdir(item_path):
        shutil.rmtree(item_path)

# Create the target directory outside the current working directory
parent_dir = os.path.abspath(os.path.join(cwd, os.pardir))
target_dir = os.path.join(parent_dir, "map")
if not os.path.exists(target_dir):
    os.mkdir(target_dir)

# Move all remaining .dae files to the target directory
for item in os.listdir(cwd):
    item_path = os.path.join(cwd, item)
    if os.path.isfile(item_path) and item.lower().endswith(".dae"):
        target_path = os.path.join(target_dir, item)
        shutil.move(item_path, target_path)
