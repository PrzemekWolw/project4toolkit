# Open the file in read mode
with open('C:/Users/user/Downloads/P4Toolkit/brook/stream.txt', 'r') as file:
    # Read the lines of the file
    lines = file.readlines()

# Open the file in write mode
with open('C:/Users/user/Downloads/P4Toolkit/brook/stream.txt', 'w') as file:
    # Iterate over the lines
    for line in lines:
        # Split the line by ',' to get a list of values
        values = line.split(',')
        # Iterate over the values in groups of 12
        for i in range(0, len(values), 12):
            # Write the group of 12 values to the file
            file.write(','.join(values[i:i+12]) + '\n')