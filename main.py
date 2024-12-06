import os, json
from app import *
from tkinter import Tk, ttk
from ttkthemes import ThemedTk
from config import *
from app.login import login_screen
from app.popup_login import login_popup
from app.operations import *

def create_root():
    root = ThemedTk(theme="arc")
    root.geometry("1400x800")
    root.configure(bg="#f5f6f7")
    root.title("CargoSail Solutions")
    return root

def crash_recovery(root, state):
    temp = ttk.Frame(root) 

    match state:
        case 1:
            # Go to (un)load selection screen
            display_operations(root, temp)
        case 2:
            # Go to operation screen for (un)load or balance
            print("operations for load/unload or balance")
        case _:
            # Default: Start at the login screen
            login_screen(root)


def open_logfile_and_save():
    # find localappdata directory
    appdata_path = os.getenv("LOCALAPPDATA")
    
    # if local app data directory cant be found, get desktop
    if appdata_path is None:
        appdata_path = os.path.normpath(os.path.expanduser("~/Desktop"))
    
    # create CargoSail folder on either localappdata or desktop
    cargosail_folder = os.path.join(appdata_path, 'CargoSail')
    os.makedirs(cargosail_folder, exist_ok=True)
    
    logfile_path = os.path.join(cargosail_folder, 'logfile2024.txt')
    set_logfile_path(logfile_path)
    
    save_file_path = os.path.join(cargosail_folder, 'save_file.json')
    set_save_file_path(save_file_path)
    
    # if the save file is not created yet it will create it with the fields specified here
    if not os.path.exists(save_file_path):
        data = {
            "name": "",
            "state" : "", # 1 = unload/load selection, 2 = operations
            "ordered_list" : [],
            "container_list": {
                "Unload": [],
                "Load": []
            },
            "manifest_data": []
        }
        
        with open(save_file_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)

root = create_root()
open_logfile_and_save()

# Read state files
last_state = read_save_file("state")
name = read_save_file("name")

# Add the name label 
name_label = ttk.Label(root, name="name_label", text=f"Logged in: {name}", font=("Arial", 14))
name_label.pack(side=tk.TOP, pady=5)  # Centered by default in the top-middle

crash_recovery(root, last_state)

# Add the login and note buttons to the root
loginButton = ttk.Button(root, text="Login", padding=(10, 10), command=lambda: login_popup(root))
loginButton.place(anchor="ne", relx=1, rely=0, x=-5, y=5)

addNoteButton = ttk.Button(root, text="Add Note", padding=(10, 10), command=lambda: add_note(root))
addNoteButton.place(anchor="nw", relx=0, rely=0, x=5, y=5)


root.mainloop()