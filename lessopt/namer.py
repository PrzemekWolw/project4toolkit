import os

#does what it says, renames the files for proper use in the .json instance file

# Set the directory you want to start from
rootDir = 'C:/Users/user/Documents/quaternion tests/new'
i = 1

for dirName, subdirList, fileList in os.walk(rootDir):
    print('Found directory: %s' % dirName)
    for fname in fileList:
        if fname.endswith('.dae'):
            old_name = os.path.join(dirName, fname)
            new_name = os.path.join(dirName, 'bk_' + str(i) + '.dae')
            os.rename(old_name, new_name)
            i += 1
            
            
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