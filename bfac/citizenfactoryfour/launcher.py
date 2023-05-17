import os
import shutil
import subprocess
import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image
from tkinter.font import Font
from tkinter import ttk
import zipfile
import subprocess
import ctypes


import os

def create_folders_island(island):
    folders = []
    if island == 'Alderney':
        for i in range(1, 6):
            folder_name = f'nj_0{i}'
            if i == 4:
                if not os.path.exists(folder_name + 'e'):
                    os.mkdir(folder_name + 'e')
                if not os.path.exists(folder_name + 'w'):
                    os.mkdir(folder_name + 'w')
            else:
                if not os.path.exists(folder_name):
                    os.mkdir(folder_name)
        if not os.path.exists('nj_docks'):
            os.mkdir('nj_docks')
    elif island == 'Bohan':
        folders = [
            'bronx_e', 'bronx_e2', 'bronx_w', 'bronx_w2',
            'brook_n', 'brook_n2', 'brook_s', 'brook_s2',
            'brook_s3', 'east_xr', 'queens_e', 'queens_m',
            'queens_w', 'queens_w2'
        ]
        for folder in folders:
            if not os.path.exists(folder):
                os.mkdir(folder)
    elif island == 'Algonquin':
        for i in range(1, 13):
            folder_name = f'manhat{str(i).zfill(2)}'
            if not os.path.exists(folder_name):
                os.mkdir(folder_name)
    return folders

import os

def create_folders_island(island):
    if island == 'Alderney':
        for i in range(1, 6):
            folder_name = f'nj_0{i}'
            try:
                if i == 4:
                    os.mkdir(folder_name + 'e')
                    os.mkdir(folder_name + 'w')
                else:
                    os.mkdir(folder_name)
            except FileExistsError:
                pass
        try:
            os.mkdir('nj_docks')
        except FileExistsError:
            pass
    elif island == 'Bohan':
        folders = [
            'bronx_e', 'bronx_e2', 'bronx_w', 'bronx_w2',
            'brook_n', 'brook_n2', 'brook_s', 'brook_s2',
            'brook_s3', 'east_xr', 'queens_e', 'queens_m',
            'queens_w', 'queens_w2'
        ]
        for folder in folders:
            try:
                os.mkdir(folder)
            except FileExistsError:
                pass
    elif island == 'Algonquin':
        for i in range(1, 13):
            folder_name = f'manhat{str(i).zfill(2)}'
            try:
                os.mkdir(folder_name)
            except FileExistsError:
                pass

    
            
import glob
import shutil

def copy_files_to_folders(island):
    folders = []
    if island == 'Alderney':
        folders = [f'nj_0{i}' for i in range(1, 6)]
        folders[3] += 'e' 
        folders.insert(4, 'nj_04w') 
        folders.append('nj_docks') 
    elif island == 'Bohan':
        folders = [
            'bronx_e', 'bronx_e2', 'bronx_w', 'bronx_w2',
            'brook_n', 'brook_n2', 'brook_s', 'brook_s2',
            'brook_s3', 'east_xr', 'queens_e', 'queens_m',
            'queens_w', 'queens_w2'
        ]
    elif island == 'Algonquin':
        folders = [f'manhat{str(i).zfill(2)}' for i in range(1, 13)]

    current_directory = os.getcwd()
    files_to_copy = glob.glob('*.idx') + glob.glob('*.p4tkpl') + glob.glob('*.py')

    for folder in folders:
        folder_path = os.path.join(current_directory, folder)
        if not os.path.exists(folder_path):
            os.mkdir(folder_path)
        for file_path in files_to_copy:
            try:
                if os.path.exists(file_path):  # Check if file exists
                    file_name = os.path.basename(file_path)
                    destination_path = os.path.join(folder_path, file_name)
                    print(f"Copying {file_path} to {destination_path}")
                    shutil.copy(file_path, destination_path)
                else:
                    print(f"File {file_path} does not exist") 
            except Exception as e:
                print(f"An error occurred while copying {file_path} to {destination_path}: {e}")
    return folders



def execute_p4tk08_script(folders):
    current_directory = os.getcwd()
    for folder in folders:
        folder_path = os.path.join(current_directory, folder)
        script_file = 'p4tk01-bng.py'
        if os.path.isfile(os.path.join(folder_path, script_file)):
            subprocess.Popen(['start', 'cmd', '/c', 'python', script_file], cwd=folder_path, shell=True) # more useful to just force all prints to one console so users can see errors

def package_directory():
    levels_folder = os.path.join(os.getcwd(), 'levels')

    if os.path.exists(levels_folder):
        selected_island = island_var.get()
        zip_file_name = f'p4tk-map-city-{selected_island.lower()}.zip'
        zip_file_path = os.path.join(os.getcwd(), zip_file_name)
        with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for root, _, files in os.walk(levels_folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, os.path.dirname(levels_folder))
                    zip_file.write(file_path, arcname)

        print('Zip file created successfully.')

        selected_directory = filedialog.askdirectory(title="Select The Mods Directory")
        if selected_directory:
            # Move ZIP files with wildcard "p4tk" to the selected directory, so that the lchunk can be moved
            for file in os.listdir(os.getcwd()):
                if file.endswith(".zip") and "p4tk" in file.lower():
                    source = os.path.join(os.getcwd(), file)
                    destination = os.path.join(selected_directory, file)
                    shutil.move(source, destination)
            print("ZIP files moved successfully.")
    else:
        print('The "levels" folder was not found.')


def select_directory():
    folder_path = filedialog.askdirectory()
    if folder_path:
        os.chdir(folder_path)

        
        create_folders_island(island_var.get())
        folders = copy_files_to_folders(island_var.get())
        execute_p4tk08_script(folders)

def open_blender():
    drive_letter = os.getenv('SystemDrive')
    blender_folder = 'Program Files'  # Assuming the Blender folder is in the Program Files directory, probably shouldnt since there is a steam version
    blender_version = 'Blender 3.5'
    blender_executable = os.path.join(drive_letter, blender_folder, blender_version, 'blender.exe')
    subprocess.Popen([blender_executable])

# Create the GUI window
window = tk.Tk()
window.title("Project 4: Toolkit Manager")
window.geometry("1100x350")

dark_style = ttk.Style()
dark_style.theme_use('clam') 



dark_style.configure('Dark.TButton',
                      background='#4C4C4C',  
                      foreground='#FFFFFF',  
                      font=('Segoe UI Variable', 12, 'bold'))  

# Island selection
title_font = Font(family="Segoe UI Variable", size=14)

title_label = tk.Label(window, text="Select the island you want to export:", font=title_font)
title_label.pack()

island_frame = tk.Frame(window)
island_frame.pack()

islands = ["Bohan", "Algonquin", "Alderney"]

island_var = tk.StringVar()

for island in islands:
    button_frame = tk.Frame(island_frame)
    button_frame.pack(side="left", padx=10)

    island_title = tk.Label(button_frame, text=island, font=title_font)
    island_title.pack()

    image_path = os.path.join(os.getcwd(), f"{island.lower()}_image.jpg")
    if os.path.isfile(image_path):
        image = Image.open(image_path)
        image = image.resize((200, 150), Image.ANTIALIAS)
        photo_image = ImageTk.PhotoImage(image)

        image_label = tk.Label(button_frame, image=photo_image)
        image_label.image = photo_image
        image_label.pack()

        select_button = ttk.Button(button_frame, text="Select", command=lambda chosen_island=island: (island_var.set(chosen_island), select_directory()))
        select_button.pack(pady=10)
    else:
        error_label = tk.Label(button_frame, text="Image Not Found", font="Arial 12", fg="red")
        error_label.pack()


def launch_sp():
    sp_executable = os.path.join(os.getcwd(), "p4tk-sp.exe")
    if os.path.exists(sp_executable):
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sp_executable, None, None, 1)
    else:
        print("p4tk-sp.exe not found.")

def launch_mp():
    mp_executable = os.path.join(os.getcwd(), "p4tk-mp.exe")
    if os.path.exists(mp_executable):
        ctypes.windll.shell32.ShellExecuteW(None, "runas", mp_executable, None, None, 1)
    else:
        print("p4tk-mp.exe not found.")

import traceback

def launch_p4tk():
    try:
        p4tk_executable = os.path.join(os.getcwd(), "p4tk.exe")
        if os.path.exists(p4tk_executable):
            ctypes.windll.shell32.ShellExecuteW(None, "runas", p4tk_executable, None, None, 1)
        else:
            print("p4tk.exe not found.")
    except Exception as e:
        print("An error occurred:")
        traceback.print_exc()

# Directory selection
directory_button = ttk.Button(window, text="Select The Tools Directory", command=select_directory)
directory_button.pack(side="left", padx=(10, 10))


dark_style.configure('Blue.TButton',
                      background='#B6D0E2', 
                      foreground='#000000',  
                      font=('Segoe UI', 12)) 

dark_style.configure('Light.TButton',
                      background='#A8DDB5',  
                      foreground='#000000',  
                      font=('Segoe UI', 12))  
# Package button

package_button = ttk.Button(window, text="Packager", command=package_directory)
package_button.pack(side="left", padx=10)

updater_button = ttk.Button(window, text="Updater", command=package_directory)
updater_button.pack(side="left", padx=10)

modpack_button = ttk.Button(window, text="Install Modpacks", command=package_directory)
modpack_button.pack(side="left", padx=10)

blender_button = ttk.Button(window, text="P4TK Level Editor", command=open_blender)
blender_button.pack(side="left", padx=10)

lchunk_button = ttk.Button(window, text="Unlock LCHUNK", command=open_blender)
lchunk_button.pack(side="left", padx=10)

# Play Singleplayer button
sp_button = ttk.Button(window, text="Play Singleplayer", command=launch_sp, style='Blue.TButton')
sp_button.pack(side="left", padx=10)

# Play Multiplayer button
mp_button = ttk.Button(window, text="Play Multiplayer", command=launch_mp, style='Light.TButton')
mp_button.pack(side="left")


window.mainloop()