import json

def parse_occlu_ipl(file_path):
    occlusion_volumes = []
    with open(file_path, 'r') as file:
        for i, line in enumerate(file):
            line_split = line.strip().split(',')
            #RAGE Volume Format: POS: midX midY bottomZ - SCALE: midX midY midZ - unused data (0.0)
            position = [float(line_split[0]), float(line_split[1]), float(line_split[2])]
            scale = [float(line_split[3]), float(line_split[4]), float(line_split[5])]
            #the reason the Z position is calculated like this is because RAGE calculates Z position based upon the bottom of a bounding volume, whereas T3D calculates the Z for the volume from the center. By dividing the scale by 2 and adding it to the position, the RAGE occlusion volumes can be ported.
            (position[2] + scale[2]) / 2
            occlusion_volume = {
                "name": f"OcclusionVolume1_{i+1}",
                "class": "OcclusionVolume",
                "persistentId": "",
                "__parent": "occluIPL",
                "position": position,
                "scale": scale
            }
            occlusion_volumes.append(occlusion_volume)
    return occlusion_volumes

def write_items_level_json(data, file_path):
    with open(file_path, 'w') as file:
        for occlusion_volume in data:
            file.write(json.dumps(occlusion_volume, separators=(',', ':')) + '\n')

occlu_ipl_path = 'occlu.ipl'
items_level_json_path = 'items.level.json'

occlusion_volumes = parse_occlu_ipl(occlu_ipl_path)
write_items_level_json(occlusion_volumes, items_level_json_path)