import os, json
from app import *
from tkinter import Tk
from config import *
from app.login import login_screen

def create_root():
    root = Tk()
    root.title("CargoSail Solutions")
    root.geometry("1400x800")
    return root

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
            "name": ""
        }
        
        with open(save_file_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)

root = create_root()
open_logfile_and_save()
login_screen(root)

root.mainloop()