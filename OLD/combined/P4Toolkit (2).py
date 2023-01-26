def script1_function():
    print("Running script 1 function")

print("Running script 1")
script1_function()

import os
import re
import sys
import bpy
import mathutils

# Select all objects in the scene
bpy.ops.object.select_all(action='SELECT')

# Delete all selected objects
bpy.ops.object.delete()


for root, dirs, files in os.walk("."):
    for file in files:
        if file.endswith(".odr"):
            with open(os.path.join(root, file), "r") as f:
                  print('check')
                  
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

        # print(str(self.index) + " - " + str(len(self.vert_data)))
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
            # for i in range(len(uv)):
            #     uv[i] = float(uv[i])
            
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
        # mtl += "Ka " + " ".join([str(o) for o in self.Ka]) + "\n"
        # mtl += "Kd " + " ".join([str(o) for o in self.Kd]) + "\n"
        # mtl += "Ks " + " ".join([str(o) for o in self.Ks]) + "\n"
        # mtl += "Ns " + str(self.Ns) + "\n"
        # mtl += "Ni " + str(self.Ni) + "\n"
        # mtl += "d " + str(self.d) + "\n"
        # mtl += "illum " + str(self.illum) + "\n"
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
            material.map_Kd = shader # TODO make something better
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

                # mesh_index = int(re.sub(r"\D", "", line))
                mesh_index += 1
                # print(mesh_index)
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
        print("--------------------")
        print(f"Mesh count: {len(self.meshes)}")
        print(f"Vertex count: {vert_count}")
        print(f"Face count: {face_count}")
        print(f"Material count: {material_count}")
        print("--------------------")

        return {"obj": obj, "mtl": mtl}


            
def parse_odr(lines):
    odr_data = {"shaders": [], "skeletons": [], "lodgroup": {}}

    shadinggroups = []
    skeletons = ""

    # Shader groups
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
                    sps_data.append(re.sub(r"\\", "/", re.sub(line.split(" ")[0], "", line).lstrip()).replace(".otx", ".png")) # TODO make something better
            previous_line = line
        shadinggroups = sps_data
    # Shader groups

    # Skeletons
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
    # Skeletons

    # LOD groups

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

    # LOD groups

    if shadinggroups:
        odr_data["shaders"] = shadinggroups

    if skeletons:
        odr_data["skeletons"] = skeletons

    return odr_data

if __name__ == "__main__" and len(sys.argv) != 2:
    print("Invalid arguments")
    exit(0)

# Code to recursively process all .odr files in the current directory and subdirectories
for root, dirs, files in os.walk("."):
    for file in files:
        if file.endswith(".odr"):
            input_file_path = os.path.join(root, file)
            input_name, ext = os.path.splitext(os.path.basename(input_file_path))
            with open(input_file_path, "r") as f:
                raw_odr_lines = f.read()
                odr_data = parse_odr(raw_odr_lines)
                # rest of the code to process the .odr file goes here

            for lodgroup in odr_data["lodgroup"]:
                output_obj_name = f"{input_name}.obj"
                output_mtl_name = f"{input_name}.mtl"

                material_parser = MaterialParser(odr_data["shaders"])
                mesh_parser = MeshParser(odr_data["lodgroup"][lodgroup], material_parser.generate())

                model_data = mesh_parser.generate(True)

                obj_headers = "# Converted by OpenFormatConverter\n\n"
                obj_headers += f"mtllib {output_mtl_name}\n\n"

                mtl_headers = "# Converted by OpenFormatConverter\n\n"

                model_data["obj"] = obj_headers + model_data["obj"]
                model_data["mtl"] = mtl_headers + model_data["mtl"]

                with open(output_obj_name, "w") as f:
                    f.write(model_data["obj"])

                with open(output_mtl_name, "w") as f:
                    f.write(model_data["mtl"])


import bpy
import os

# Select all objects in the scene
bpy.ops.object.select_all(action='SELECT')

# Delete all selected objects
bpy.ops.object.delete()

# Set the active rendering engine to 'BLANK'


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

# Set the path to the folder containing the .obj files here
path = os.getcwd()

# Iterate over all .obj files in the folder
for obj_file in os.listdir(path):
    if obj_file.endswith(".obj"):
        # Import the .obj file
        bpy.ops.import_scene.obj(filepath=os.path.join(path, obj_file))

        # Get all materials with names starting with "Standardmaterial"
        mat_names = [
            mat.name for mat in bpy.data.materials
            if mat.name.startswith("MAT")
        ]

        # Rename the materials
        for mat_name in mat_names:
            mat = bpy.data.materials[mat_name]
            node = find_base_color_node(mat)
            if new_name := get_node_name(node):
                mat.name = new_name

        # Export the .obj file with the new material names
        bpy.ops.export_scene.obj(filepath=os.path.join(path, obj_file))

        # Remove the object from the scene
        bpy.ops.object.delete()

CONVERT_DIR = os.getcwd()

import os

def file_iter(path, ext):
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            ext = os.path.splitext(filename)[1]
            if ext.lower().endswith(ext):
                yield os.path.join(dirpath, filename)

import os
import bpy

# Select all objects in the scene
bpy.ops.object.select_all(action='SELECT')

# Delete all selected objects
bpy.ops.object.delete()

# Set the active rendering engine to 'BLANK'


def reset_blend():
    bpy.ops.wm.read_factory_settings(use_empty=True)

def convert_recursive(base_path):
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith('.obj'):
                filepath_src = os.path.join(root, file)
                filepath_dst = f"{os.path.splitext(filepath_src)[0]}.dae"

                print("Converting %r -> %r" % (filepath_src, filepath_dst))

                reset_blend()

                bpy.ops.import_scene.obj(filepath=filepath_src)
                bpy.ops.wm.collada_export(filepath=filepath_dst)

if __name__ == "__main__":
    convert_recursive(CONVERT_DIR)

      

def script2_function():
    print("Running script 2 function")

print("Running script 2")
script2_function()

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

#the likely fix is that on LOD import, check if the W rotation matches on both files, if they do not match, find the one with the +W to a -W to match, RAGE is only making positive W errors
      
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
    rot_w_str = values[6].replace(",", "")
    if rot_w_str[0] == "-":
        rot_w = -float(rot_w_str[1:])
    else:
        rot_w = float(rot_w_str)
        
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
    
    print(dae_name)
    
def script3_function():
    print("Running script 3 function")

print("Running script 3")
script3_function()



import bpy
import os
import re

# Select all objects in the scene
bpy.ops.object.select_all(action='SELECT')

# Delete all selected objects
bpy.ops.object.delete()

# Get the current working directory (cwd)
cwd = os.getcwd()

# Iterate through all files in the cwd
for file in os.listdir(cwd):
    # Check if the file is a .dae file
    if file.endswith(".dae"):
        # Import the .dae file
        bpy.ops.wm.collada_import(filepath=file)

        # Apply the original function to each object in the .dae file
        for ob in bpy.context.selected_editable_objects:    
            # Iterate over each material slot of the object
            for m_slot in ob.material_slots:
                # Skip the material slot if it does not have a material
                if not m_slot.material:
                    continue
                # Get the material's name
                s1 = m_slot.material.name
                # Split the name by the "." character and keep only the first part
                sArr = s1.split(".")
                m_slot.material.name = sArr[0]

        # Apply the modified function to each object in the .dae file
        for ob in bpy.context.selected_editable_objects:    
            # Iterate over each material slot of the object
            for m_slot in ob.material_slots:
                # Skip the material slot if it does not have a material
                if not m_slot.material:
                    continue
                # Get the material's name
                s1 = m_slot.material.name
                # Use a regular expression to replace any occurrence of ".\d{3}" with an empty string
                s1 = re.sub(r"\.\d{3}", "", s1)
                m_slot.material.name = s1

        # Export and overwrite the old .dae file
        bpy.ops.wm.collada_export(filepath=file)
        
        # Remove the object from the scene
        bpy.ops.object.delete()
        
def script4_function():
    print("Running script 4 function")

print("Running script 4")
script4_function()

import bpy
import os
import re

# Select all objects in the scene
bpy.ops.object.select_all(action='SELECT')

# Delete all selected objects
bpy.ops.object.delete()

# Get the current working directory (cwd)
cwd = os.getcwd()

# Iterate through all files in the cwd
for file in os.listdir(cwd):
    # Check if the file is a .dae file
    if file.endswith(".dae"):
        # Import the .dae file
        bpy.ops.wm.collada_import(filepath=file)

        # Apply the original function to each object in the .dae file
        for ob in bpy.context.selected_editable_objects:    
            # Iterate over each material slot of the object
            for m_slot in ob.material_slots:
                # Skip the material slot if it does not have a material
                if not m_slot.material:
                    continue
                # Get the material's name
                s1 = m_slot.material.name
                # Split the name by the "." character and keep only the first part
                sArr = s1.split(".")
                m_slot.material.name = sArr[0]

        # Apply the modified function to each object in the .dae file
        for ob in bpy.context.selected_editable_objects:    
            # Iterate over each material slot of the object
            for m_slot in ob.material_slots:
                # Skip the material slot if it does not have a material
                if not m_slot.material:
                    continue
                # Get the material's name
                s1 = m_slot.material.name
                # Use a regular expression to replace any occurrence of ".\d{3}" with an empty string
                s1 = re.sub(r"\.\d{3}", "", s1)
                m_slot.material.name = s1

        # Export and overwrite the old .dae file
        bpy.ops.wm.collada_export(filepath=file)
        
        # Remove the object from the scene
        bpy.ops.object.delete()
        
def script5_function():
    print("Running script 5 function")

print("Running script 5")
script5_function()        
        
        
import os
# Set the root directory to the cwd
root_directory = os.getcwd()
# Iterate over all the files and subdirectories in the directory
for root, dirs, files in os.walk(root_directory):
    # Iterate over all the files in the current directory
    for filename in files:
    # Check if the file is a .mtl or .obj file
        if filename.endswith('.mtl') or filename.endswith('.obj'):
    # Construct the file path
            filepath = os.path.join(root, filename)
        # Delete the file
            os.remove(filepath)
        
        