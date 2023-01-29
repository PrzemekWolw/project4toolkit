# Name of the input file
file_name = 'combined_output.txt'

# Name of the output file
output_file = 'output.txt'

with open(file_name, 'r') as input_file, open(output_file, 'w') as output:
    for line in input_file:
        # Split the line by comma
        values = line.strip().split(',')
        # Check if the number of values in the line is 12
        if len(values) == 12:
            output.write(line)