def script0_function():
    print("Moving Textures")

script0_function()

import os
import shutil
import scandir

# Set the directory to search
root_dir = os.getcwd()

# Check if the destination folder exists, create it if not
destination = os.path.join(root_dir, 'text')
if not os.path.exists(destination):
    os.makedirs(destination)

# Keep track of processed files
processed_files = set()

# Search for files with .dds extension
for dirpath, dirnames, filenames in scandir.walk(root_dir):
    for file in filenames:
        if file.endswith('.dds'):
            src_path = os.path.join(dirpath, file)
            if src_path in processed_files:
                # If the file has already been processed, delete it
                os.remove(src_path)
                continue
            processed_files.add(src_path)
            dst_path = os.path.join(destination, file)
            shutil.move(src_path, dst_path)

print("All .dds files have been moved to the text folder.")