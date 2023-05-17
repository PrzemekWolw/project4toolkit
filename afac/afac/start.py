import os
import shutil
import subprocess

def create_folders_island(island):
    if island == 'NJ':
        for i in range(1, 6):
            folder_name = f'NJ_0{i}'
            if not os.path.exists(folder_name):
                os.mkdir(folder_name)
    elif island == 'BROOK':
        folders = [
            'bronx_e', 'bronx_e2', 'bronx_w', 'bronx_w2',
            'brook_n', 'brook_n2', 'brook_s', 'brook_s2',
            'brook_s3', 'east_xr', 'queens_e', 'queens_m',
            'queens_w', 'queens_w2'
        ]
        for folder in folders:
            if not os.path.exists(folder):
                os.mkdir(folder)
    elif island == 'MANHAT':
        for i in range(1, 13):
            folder_name = f'manhat{i}'
            if not os.path.exists(folder_name):
                os.mkdir(folder_name)

def copy_files_to_folders(island):
    folders = []
    if island == 'NJ':
        folders = [f'NJ_0{i}' for i in range(1, 6)]
    elif island == 'BROOK':
        folders = [
            'bronx_e', 'bronx_e2', 'bronx_w', 'bronx_w2',
            'brook_n', 'brook_n2', 'brook_s', 'brook_s2',
            'brook_s3', 'east_xr', 'queens_e', 'queens_m',
            'queens_w', 'queens_w2'
        ]
    elif island == 'MANHAT':
        folders = [f'manhat{i}' for i in range(1, 13)]

    current_directory = os.getcwd()  # Store the current working directory
    for folder in folders:
        for file in os.listdir(current_directory):
            if file.endswith(('.p4tkpl', '.py', '.idx')):
                source = os.path.join(current_directory, file)
                destination = os.path.join(current_directory, folder, file)
                if not os.path.exists(destination):
                    shutil.copy(source, destination)

    return folders  # Return the list of folders where files were copied

def execute_p4tk08_script(folders):
    current_directory = os.getcwd()  # Store the current working directory
    for folder in folders:  # Only use the folders where files were copied
        folder_path = os.path.join(current_directory, folder)
        script_file = 'p4tk01-ac.py'
        if os.path.isfile(os.path.join(folder_path, script_file)):
            subprocess.Popen(['start', 'cmd', '/k', 'python', script_file], cwd=folder_path, shell=True)

def main():
    island = input("What island are you exporting? (BROOK, MANHAT, NJ): ")
    create_folders_island(island)
    folders = copy_files_to_folders(island)  # Get the list of folders where files were copied
    execute_p4tk08_script(folders)  # Execute the script only in these folders

if __name__ == '__main__':
    main()
