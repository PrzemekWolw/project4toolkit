import xml.etree.ElementTree as ET

with open("stream.xml", "r") as stream:
    xml_string = stream.read()
    root = ET.fromstring(xml_string)
    for item in root.findall('Item'):
        archetype_name = item.find('archetypeName').text
        pos_x = float(item.find('position').get('x'))
        pos_y = float(item.find('position').get('y'))
        pos_z = float(item.find('position').get('z'))
        rot_x = float(item.find('rotation').get('x'))
        rot_y = float(item.find('rotation').get('y'))
        rot_z = float(item.find('rotation').get('z'))
        rot_w = float(item.find('rotation').get('w'))
        quat = mathutils.Quaternion((rot_w, rot_x, rot_y, rot_z))
        dae_name = archetype_name
        cwd = os.getcwd()
        filepath = os.path.join(cwd, f"{dae_name}.dae")
        if not os.path.exists(filepath):
            print(".dae file not found:", dae_name)
            continue
        bpy.ops.wm.collada_import(filepath=os.path.join(cwd, f"{dae_name}.dae"))
        for obj in bpy.context.scene.objects:
            obj.rotation_mode = "QUATERNION"
            obj.rotation_quaternion = quat
            obj.location = (pos_x, pos_y, pos_z)
        export_path = os.path.join(cwd, f"{dae_name}.dae")
        bpy.ops.wm.collada_export(filepath=export_path)
        bpy.ops.object.delete()
        print(dae_name