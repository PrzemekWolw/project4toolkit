import os
import shutil

def delete_files(path):
    for root, dirs, files in os.walk(path):
        for file in files:
            if file == ".001.dds" or file == ".002.dds" or file == ".003.dds" or file == ".004.dds" or file == ".005.dds" or file == ".006.dds" or file == ".007.dds":
                os.remove(os.path.join(root, file))

def move_files(path):
    destination_folder = os.path.join(path, 'map', 'mh')
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.dae') or file.endswith('.dds'):
                shutil.move(os.path.join(root, file), destination_folder)

current_dir = os.getcwd()
delete_files(current_dir)
move_files(current_dir)