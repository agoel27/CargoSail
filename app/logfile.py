import os

def add_logEntry(message):
    # store localappdata directory
    appdata_path = os.getenv("LOCALAPPDATA")
    
    # if local app data directory cant be found, get desktop
    if appdata_path is None:
        appdata_path = os.path.normpath(os.path.expanduser("~/Desktop"))
    
    # store CargoSail folder on either localappdata or desktop
    cargosail_folder = os.path.join(appdata_path, 'CargoSail')
 
    # store CargoSail logpath
    logfile_path = os.path.join(cargosail_folder, 'logfile2024.txt')
    
    with open(logfile_path, 'a') as logfile:
        logfile.write(message)