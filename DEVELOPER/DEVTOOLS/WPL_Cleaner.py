import os

folder_path = "C:/Users/user/Documents/New Folder (6)" # replace with the actual path to the folder
output_file = "combined_output.txt"

def process_file(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()

    with open(file_path, "w") as file:
        for line in lines:
            if "hash" not in line and "stevem" not in line and "phantom" not in line and "alastair.mclauchlan" not in line and "mule" not in line and "sentinel" not in line and "nrg900" not in line and "airtug" not in line and "ripley" not in line and "gavin.greaves" not in line and "end" not in line and "grge" not in line and "cars" not in line and "tcyc" not in line and "mlop" not in line and "lodm" not in line and "version 3" not in line and "inst" not in line and "# GTA IV Binary Placement File" not in line and "tim.gilbert" not in line and "slow" not in line and "blok" not in line and "jima" not in line:
                file.write(line)

with open(output_file, "w") as output:
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".opl"):
            file_path = os.path.join(folder_path, file_name)
            process_file(file_path)
            with open(file_path, "r") as file:
                output.write(file.read())