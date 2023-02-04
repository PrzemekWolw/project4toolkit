import os
import json
import uuid

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
                        "colorMap": f"/levels/p4tk/ext_veg/{dds_name}.dds",
                        "diffuseColor": [
                            0.119062997,
                            0.249724001,
                            0.151963994,
                            1
                        ],
                        "emissive": False,
                        "glow": False,
                        "glowFactor": [
                            0.471401006,
                            0.787751019,
                            0.391137987
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