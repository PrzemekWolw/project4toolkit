# Open the input file
with open("stream.wpl", "r") as input_file:
    # Open the output file
    with open("stream2.wpl", "w") as output_file:
        # Iterate over the lines in the input file
        for line in input_file:
            # Split the line into a list of values
            values = line.strip().split(",")
            # remove whitespaces and check if the value is a number
            value = values[6].replace(" ", "")
            if value.replace("-", "").replace(".", "").isnumeric():
                # Check if the 6th value starts with a minus sign
                if value.startswith("-"):
                    # Add another negative sign in front of the negative sign
                    values[6] = "-" + value
                else:
                    values[6] = value
            # Join the values back into a string
            new_line = ",".join(values)
            # Write the modified line to the output file
            output_file.write(new_line + "\n")