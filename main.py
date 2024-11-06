import os
from app.load_balance_screen import load_balance
from tkinter import Tk

def create_root():
    root = Tk()
    root.title("CargoSail Solutions")
    root.geometry("800x600")
    return root

def open_logfile():
    # find localappdata directory
    appdata_path = os.getenv("LOCALAPPDATA")
    
    # if local app data directory cant be found, get desktop
    if appdata_path is None:
        appdata_path = os.path.normpath(os.path.expanduser("~/Desktop"))
    
    # create CargoSail folder on either localappdata or desktop
    cargosail_folder = os.path.join(appdata_path, 'CargoSail')
    os.makedirs(cargosail_folder, exist_ok=True)
    
    logfile_path = os.path.join(cargosail_folder, 'logfile2024.txt')
    
    with open(logfile_path, 'a') as logfile:
        logfile.write("hello\n")


root = create_root()
open_logfile()
load_balance(root)

root.mainloop()