import os

with open("stream.txt", "r") as stream:
    lines = stream.readlines()

with open("output.txt", "w") as output:
    for line in lines:
        values = line.split()
        dae_name = values[7].replace(",", "")

        output.write(f'{{"class":"TSStatic","persistentId":"","__parent":"MissionGroup","position":[1,0,0],"collisionType":"Visible Mesh Final","decalType":"Visible Mesh Final","dynamic":true,"meshCulling":true,"prebuildCollisionData":true,"scale":[1,1,1],"shapeName":"/levels/ProjectIV_Brooklyn/brook/{dae_name}.dae","useInstanceRenderData":true}}\n')

print("output.txt file created with extracted values")