import os
import subprocess
from multiprocessing import Pool

def convert_obj_to_dae(file_path):
    input_file = os.path.abspath(file_path).replace('\\', '/')
    output_file = os.path.splitext(input_file)[0] + ".dae"

    blender_command = [
        "C:\\Program Files\\Blender Foundation\\Blender 3.5\\blender.exe",
        "--background",
        "--factory-startup",
        "--python-expr",
        f"import bpy; bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False); bpy.ops.import_scene.obj(filepath='{input_file}'); bpy.ops.wm.collada_export(filepath='{output_file}'); bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)",
    ]
    subprocess.run(blender_command, check=True)

def find_obj_files(folder):
    return [os.path.join(folder, file) for file in os.listdir(folder) if file.endswith(".obj")]

if __name__ == "__main__":
    folder_path = os.getcwd()

    obj_files = find_obj_files(folder_path)

    with Pool() as pool:
        pool.map(convert_obj_to_dae, obj_files)
