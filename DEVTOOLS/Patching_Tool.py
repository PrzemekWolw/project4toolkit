def script1_function():


    script1_function()
import bpy
import os
import mathutils

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

#This will convert the models position and rotation (w, x, y, z) quaternion by using the decrypted .wpl stream files. There is a known error here that in some fringe cases the w rotation is flipped positive when it should be negative, or vice versa. 
#It is possible that RAGE is making a correction on its own here, possibly by using the last two values of the .wpl, but it is unknown. implement a fix for the known flipped w rotations.
#The likely fix is that on LOD import, check if the W rotation matches on both files, if they do not match, find the one with the +W to a -W to match, RAGE is only making positive W errors. This will only work if the LODMATCH function is reimplemented, currently it is disabled.

with open("stream.wpl", "r") as stream:
    lines = stream.readlines()

for line in lines:
    values = line.split()

    # Extract the position and rotation values from .wpl. RAGE uses Euler for position and quaternion for its rotations, it is also possible to convert to a rotation matrix that T3D would understand since it does not currently support .json quaternion to my knowledge. If the mechanism for doing so can be found, error correction for W need not be implemented.
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
        obj.location = (pos_x, pos_y, pos_z)

    export_path = os.path.join(cwd, f"{dae_name}.dae")

    bpy.ops.wm.collada_export(filepath=export_path)
    bpy.ops.object.delete()

    print(dae_name)
    print(pos_x, pos_y, pos_z)
    print(quat)    

def script2_function():


    script2_function()
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