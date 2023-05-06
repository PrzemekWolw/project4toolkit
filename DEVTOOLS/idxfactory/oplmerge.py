import os

# Create a list of all ".opl" files in the current working directory
opl_files = [f for f in os.listdir('.') if f.endswith('.opl')]

# Open a new output file for writing
with open('combined.opl', 'w') as combined_file:
    # Iterate over each ".opl" file and copy its contents to the output file
    for opl_file in opl_files:
        with open(opl_file, 'r') as input_file:
            combined_file.write(input_file.read())
            # Add a newline character to separate the contents of each input file
            combined_file.write('\n')