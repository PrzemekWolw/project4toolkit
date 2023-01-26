# Open the file
with open('stream.txt', 'r') as f:
    # Read each line of the file
    for line in f:
        # Split the line into a list of values
        values = line.split()
        
        # Print the label and the first 8 values
        print("X:", values[0])
        print("Y:", values[1])
        print("Z:", values[2])
        print("RX:", values[3])
        print("RY:", values[4])
        print("RZ:", values[5])
        print("RW:", values[6])
        print("Model:", values[7])