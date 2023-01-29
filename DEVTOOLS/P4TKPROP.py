import time
start_time = time.time()

# Need to replace all listdir implementations with scandir to improve speed, multiple duplicate or split functions that can be combined will also serve to improve speed
def script0_function():
    print("Breaking WDDs")

script0_function()

import os

# Get a list of all .odd files in the current directory
odd_files = [f for f in os.listdir('.') if f.endswith('.odd')]

for odd_file in odd_files:
    with open(odd_file, 'r') as f:
        contents = f.read()

    blocks = contents.split('gtaDrawable')

    for block in blocks:
        if 'lodgroup' in block:
            drawable_name = block.split('\n')[0].strip()
            with open(f'{drawable_name}.odr', 'w') as f:
                f.write(f'gtaDrawable {block}')
                
def script1_function():
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

import os
from concurrent.futures import ThreadPoolExecutor

def process_file(file_path):
    input_name, ext = os.path.splitext(os.path.basename(file_path))
    with open(file_path, "r") as f:
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

# Create a thread pool with 4 threads
with ThreadPoolExecutor(max_workers=4) as executor:
    file_paths = [dir_entry.path for dir_entry in os.scandir(".") if dir_entry.is_file() and dir_entry.name.endswith(".odr")]
    # Submit the process_file function for each file in file_paths
    results = [executor.submit(process_file, file_path) for file_path in file_paths]
    
CONVERT_DIR = os.getcwd()

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

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

def convert_recursive(base_path):
    files_to_convert = []
    for entry in os.scandir(base_path):
        if entry.is_file() and entry.name.endswith('.obj'):
            files_to_convert.append(entry.path)

    batch_size = 50
    for i in range(0, len(files_to_convert), batch_size):
        batch = files_to_convert[i:i+batch_size]
        for filepath_src in batch:
            filepath_dst = f"{os.path.splitext(filepath_src)[0]}.dae"

            print("Converting Meshes...")
            bpy.ops.import_scene.obj(filepath=filepath_src)
            for obj in bpy.context.selected_objects:
                obj.rotation_euler = (0, 0, 0)
            mat_names = [
                mat.name for mat in bpy.data.materials
                if mat.name.startswith("MAT")
            ]

            for mat_name in mat_names:
                mat = bpy.data.materials[mat_name]
                node = find_base_color_node(mat)
                if new_name := get_node_name(node):
                    mat.name = new_name
            # This is really slow, use numpy to convert to .dae
            bpy.ops.wm.collada_export(filepath=filepath_dst)
            bpy.ops.object.select_all(action='SELECT')
            bpy.ops.object.delete()

if __name__ == "__main__":
    convert_recursive(CONVERT_DIR)
    

            
def script3_function():
    print("Creating LODs")
    
script3_function()

import os
import bpy

def process_dae(file_path):
    bpy.ops.wm.collada_import(filepath=file_path)

    imported_obj = bpy.context.selected_objects[0]

    bpy.context.view_layer.objects.active = imported_obj
    bpy.ops.object.duplicate()
    obj1 = bpy.context.selected_objects[0]
    obj1.name = f"{imported_obj.name}_a250"
    bpy.context.view_layer.objects.active = imported_obj
    bpy.ops.object.duplicate()
    obj2 = bpy.context.selected_objects[0]
    obj2.name = f"{imported_obj.name}_a130"
    imported_obj.name = f"{imported_obj.name}_a430"

    for obj in [obj1, obj2]:
        obj.modifiers.new("Decimate", type='DECIMATE')
        if "_a250" in obj.name:
            obj.modifiers["Decimate"].ratio = 0.5
        elif "_a130" in obj.name:
            obj.modifiers["Decimate"].ratio = 0.25
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.modifier_apply(modifier="Decimate")

# Need a function here that will reduce drawcalls by changing the entire UV mapped material set to just one .dds since we are neither implementing LODMATCH here nor using the .wdb textures. This one .dds method should only be used when employing the simple LOD creator shown here.     
    bpy.ops.object.empty_add(type='ARROWS', radius=1, location=(0, 0, 0))
    base00 = bpy.context.object
    base00.name = "base00"
    bpy.ops.object.empty_add(type='ARROWS', radius=1, location=(0, 0, 0))
    start01 = bpy.context.object
    start01.name = "start01"

    start01.parent = base00
    imported_obj.parent = start01
    obj1.parent = start01
    obj2.parent = start01

    bpy.ops.wm.collada_export(filepath=file_path)

    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

working_dir = os.getcwd()

for file in os.listdir(working_dir):
    if file.endswith(".dae"):
        file_path = os.path.join(working_dir, file)
        process_dae(file_path)

def script4_function():
    print("Cleaning Materials")

script4_function()

# Material cleaning is done twice due to the indexing log that Blender begins to build after each function is run. Either combine the functions into better sets or keep this here. Even with this implemented some indexes will still slip through.
import bpy
import os
import re

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()


cwd = os.getcwd()
for file in os.listdir(cwd):
    if file.endswith(".dae"):
        bpy.ops.wm.collada_import(filepath=file)


        for ob in bpy.context.selected_editable_objects:    
            for m_slot in ob.material_slots:
                if not m_slot.material:
                    continue
                s1 = m_slot.material.name
                sArr = s1.split(".")
                m_slot.material.name = sArr[0]

        for ob in bpy.context.selected_editable_objects:    
            for m_slot in ob.material_slots:
                if not m_slot.material:
                    continue
                s1 = m_slot.material.name
                s1 = re.sub(r"\.\d{3}", "", s1)
                m_slot.material.name = s1

        for mat in bpy.data.materials:
            if mat.name[-4:].isdigit():
                mat.name = mat.name[:-4]

        bpy.ops.wm.collada_export(filepath=file)
 
        bpy.ops.object.delete()
        


end_time = time.time()
time_elapsed = end_time - start_time
print("Time elapsed: {:.2f} seconds".format(time_elapsed))
