import os
from app import *
from tkinter import Tk
from app.login import login_screen
from app.load_balance_screen import load_balance
from app.operations_screen import operations_screen

def create_root():
    root = Tk()
    root.title("CargoSail Solutions")
    root.geometry("1400x800")
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
operations_screen(root)
#login_screen(root)
#load_balance(root)

root.mainloop()