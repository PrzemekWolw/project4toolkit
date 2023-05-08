# Open the input file for reading
with open("mh01.p4tkBIG", "r") as input_file:
    # Read all lines from the input file
    lines = input_file.readlines()

# Open the output file for writing
with open("output.txt", "w") as output_file:
    # Write each line from the input file to the output file if it does not contain the strings "LOD" or "lod"
    for line in lines:
        if "LOD" not in line and "lod" not in line:
            output_file.write(line)