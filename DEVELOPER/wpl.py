with open('manhat01.big', 'r') as big_file:
    big_lines = big_file.readlines()
# Kind of hacky here subtracting 1 from the actual index value but I am not sure why it was ignoring trying to un-zero the prior file, who knows, or cares, it works.
with open('output.txt', 'w') as output_file:
    with open('manhat01_stream7.opl', 'r') as little_file:
        for i, line in enumerate(little_file):
            # Obtain model name and reference number from the little file line
            little_model_name = line.split(",")[7].strip()
            little_ref_num = int(line.split(",")[9].strip())

            # Skip lines that have a reference number of -1
            if little_ref_num == -1:
                output_file.write(f"{little_model_name}, None, None\n")
                continue

            little_ref_num -= 1

            # Find the big file line referenced by the little file line
            if little_ref_num < len(big_lines):
                big_line = big_lines[little_ref_num]
                big_model_name = big_line.split(",")[7].strip()
                big_ref_num = int(big_line.split(",")[9].strip())

                # Skip lines that have a reference number of -1
                if big_ref_num == -1:
                    output_file.write(f"{little_model_name}, {big_model_name}, None\n")
                    continue

                big_ref_num -= 1

                # Follow the reference numbers until the final model name is found or -1 is reached
                final_model_name = None
                final_ref_num = None
                while big_ref_num != -1 and big_ref_num < len(big_lines):
                    final_line = big_lines[big_ref_num]
                    final_model_name = final_line.split(",")[7].strip()
                    final_ref_num = int(final_line.split(",")[9].strip())

                    if final_ref_num == -1:
                        break

                    final_ref_num -= 1
                    big_ref_num = final_ref_num

                # Write the three model names to the output file
                output_file.write(f"{little_model_name}, {big_model_name}, {final_model_name}\n")
                print(f"Processed line {i+1}: {little_model_name}, {big_model_name}, {final_model_name}")

            else:
                output_file.write(f"{little_model_name}, None, None\n")
                print(f"Processed line {i+1}: {little_model_name}, None, None")