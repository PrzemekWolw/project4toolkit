import os

# Get the current working directory
folder_path = os.getcwd()

# Get all .dae files in the current working directory
dae_files = [f for f in os.listdir(folder_path) if f.endswith('.dae')]

# Open a .txt file for writing
with open('output.txt', 'w') as f:
    for dae_file in dae_files:
        # Write the line to the file, replacing "XXX" with the current .dae file's name
        f.write(f'{"{"}"class":"TSStatic","persistentId":"","__parent":"NJ","position":[1,0,0],"collisionType":"Visible Mesh Final","decalType":"None","dynamic":true,"meshCulling":true,"prebuildCollisionData":true,"scale":[1,1,1],"shapeName":"/levels/smallgriddark/map/nj/{dae_file}","useInstanceRenderData":true {"}"}\n')