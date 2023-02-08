import os

odd_files = [f for f in os.listdir('.') if f.endswith('.odd')]

for odd_file in odd_files:
    with open(odd_file, 'r') as f:
        contents = f.read()

    blocks = contents.split('gtaDrawable')
# this is HORRIBLE, it works but please fix this disaster at some point
    for block in blocks:
        if 'lodgroup' in block:
            drawable_name = block.split('\n')[0].strip()
            shading_group = block.split('shadinggroup')[1].strip()
            shading_group = shading_group.split('}}')[0].strip() + '\n}\n}'
            lod_group = block.split('lodgroup')[1].strip()
            lod_group = lod_group.split('}')[0].strip()
            with open(f'{drawable_name}.odr', 'w') as f:
                shading_group_lines = shading_group.split("\n")
                shading_group_lines = [line[2:] for line in shading_group_lines] 
                shading_group = "\n".join(shading_group_lines)
                lod_group_lines = lod_group.split("\n")
                lod_group_lines = [line[2:] for line in lod_group_lines]
                lod_group = "\n".join(lod_group_lines)
                f.write(f'version 110 12\nshadinggroup\n{{{shading_group}}}')