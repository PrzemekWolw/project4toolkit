import os
import json

def main():
    cwd = os.getcwd()
    materials = {}
    for filename in os.listdir(cwd):
        if filename.endswith(".dds"):
            dds_name = filename.split(".dds")[0]
            materials[dds_name] = {
                "name": dds_name,
                "mapTo": dds_name,
                "class": "Material",
                "Stages": [
                    {
                        "colorMap": f"/levels/p4tk/map/mh/{dds_name}.dds",
                        "diffuseColor": [
                            0.999989986,
                            1,
                            0.999992013,
                            1
                        ]
                    },
                    {
                        "diffuseColor": None,
                        "emissive": None,
                        "glow": None,
                        "glowFactor": None
                    },
                    {
                        "diffuseColor": None,
                        "emissive": None,
                        "glow": None,
                        "glowFactor": None
                    },
                    {
                        "diffuseColor": None,
                        "emissive": None,
                        "glow": None,
                        "glowFactor": None
                    }
                ]
            }
    with open("main.materials.json", "w") as f:
        json.dump(materials, f, indent=2)

if __name__ == '__main__':
    main()