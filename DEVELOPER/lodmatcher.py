positions = {}

with open("stream.p4tkpl", "r") as stream:
    lines = stream.readlines()

with open("duplicate_positions.txt", "w") as dup_file:
    with open("unique_positions.txt", "w") as uniq_file:
        for line in lines:
            values = line.split()

            pos_x = float(values[0].replace(",", ""))
            pos_y = float(values[1].replace(",", ""))
            pos_z = float(values[2].replace(",", ""))
            rot_x = float(values[3].replace(",", ""))
            rot_y = float(values[4].replace(",", ""))
            rot_z = float(values[5].replace(",", ""))
            rot_w_str = values[6].replace(",", "")
            rot_w = -float(rot_w_str[1:]) if rot_w_str[0] == "-" else float(rot_w_str)
            dae_name = (values[7].replace(",", ""))

            pos_key = f"{pos_x},{pos_y},{pos_z}"
            if pos_key in positions:
                positions[pos_key].append(dae_name)
                if len(positions[pos_key]) == 2:
                    dup_file.write(f"{positions[pos_key][0]},{positions[pos_key][1]}\n")
            else:
                uniq_file.write(f"{dae_name}\n")
                positions[pos_key] = [dae_name]
