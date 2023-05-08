with open('mh01.p4tkLITTLE') as little_file:
    with open('mh01.p4tkBIG') as big_file:
          with open('output.txt', 'w') as output_file:
            for little_line in little_file:
                little_parts = little_line.strip().split(',')
                little_name = little_parts[7].strip()
                big_line_number = int(little_parts[9].strip())
                if big_line_number != -1:
                    for i, big_line in enumerate(big_file):
                        if i == big_line_number -1:
                            big_parts = big_line.strip().split(',')
                            big_name = big_parts[7].strip()
                            output_file.write(f"{little_name}, {big_name}, {big_line_number}\n")
                            big_file.seek(0)
                            break
                        elif i >= big_line_number:
                            big_file.seek(0)
                            break
