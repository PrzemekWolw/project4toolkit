import mathutils

def quat_to_rot_mat(quat):
    rot_mat = quat.to_matrix().to_4x4()
    return [rot_mat[0][0], rot_mat[0][1], rot_mat[0][2], rot_mat[1][0], rot_mat[1][1], rot_mat[1][2], rot_mat[2][0], rot_mat[2][1], rot_mat[2][2]]

output_files = {}
with open("stream.wpl") as file:
    for line in file:
        values = line.strip().split(" ")
        pos_x = float(values[0].replace(",", ""))
        pos_y = float(values[1].replace(",", ""))
        pos_z = float(values[2].replace(",", ""))
        rot_x = float(values[3].replace(",", ""))
        rot_y = float(values[4].replace(",", ""))
        rot_z = float(values[5].replace(",", ""))
        rot_w_str = values[6].replace(",", "")
        rot_w = -float(rot_w_str[1:]) if rot_w_str[0] == "-" else float(rot_w_str)
        quat = mathutils.Quaternion((rot_w, rot_x, rot_y, rot_z))
        dae_name = (values[7].replace(",", "")).lower()
        if dae_name in ["c_apple_md_ingame", "cj_telgrphpole", "cj_telgrphpole_2", "cj_telgrphpole_3", "cj_telgrphpole_4", "cj_telgrphpole_5", "cj_telgrphpole_6", "c_apple_md_ingame_2", "c_apple_md_ingame01", "c_fern_md_ingame", "c_fern_md_ingame_2", "c_fern_md_ingame_3", "elm_md_ingame", "elm_md_ingame_2", "h_c_md_f_ingame", "h_c_md_f_ingame_2", "l_p_sap_ingame_2", "liveoak_md_ingame", "liveoak_md_ingame_2", "londonp_md_ingame", "londonp_md_ingame_2", "pinoak_md_ingame", "pinoak_md_ingame_2", "w_birch_md_ingame", "w_birch_md_ingame_2", "w_birch_md_ingame2", "w_r_cedar_md_ingame"]:
            if dae_name not in output_files:
                output_files[dae_name] = open(dae_name + ".forest4" + ".json", "w")
            rot_mat = quat_to_rot_mat(quat)
            output_string = '{"pos":['+str(pos_x)+','+str(pos_y)+','+str(pos_z)+'],"rotationMatrix":['+str(rot_mat[0])+','+str(rot_mat[1])+','+str(rot_mat[2])+','+str(rot_mat[3])+','+str(rot_mat[4])+','+str(rot_mat[5])+','+str(rot_mat[6])+','+str(rot_mat[7])+','+str(rot_mat[8])+'],"scale":1,"type":"'+dae_name+'"}\n'
            output_files[dae_name].write(output_string)

for dae_name in output_files:
    output_files[dae_name].close()