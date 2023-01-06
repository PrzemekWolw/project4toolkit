import os
import shutil
import zipfile

# Find all .dds and .dae files in the current directory and its subdirectories
dds_files = []
for root, dirs, files in os.walk("."):
    for file in files:
        if file.endswith(".dds") or file.endswith(".dae"):
            dds_files.append(os.path.join(root, file))

# Create a new directory called "brook"
os.makedirs("brook", exist_ok=True)

# Move all .dds and .dae files into the new directory
for file in dds_files:
    shutil.move(file, "brook")