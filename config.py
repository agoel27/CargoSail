# global functions for easy access from all files
# to access from the app folder do: from config import *

import requests, json, os
from tkinter import ttk

def set_logfile_path(path):
    global logfile_path
    logfile_path = path
    
def get_logfile_path():
    return logfile_path

def set_save_file_path(path):
    global save_file_path
    save_file_path = path
    
def get_save_file_path():
    return save_file_path

def set_username(username):
    global user
    user = username
    
def get_username():
    return user

def set_manifest(data):
    global manifest_data
    manifest_data = data
    write_save_file("manifest_data", data)

def set_outbound_manifest_path(path):
    global outbound_manifest_path
    outbound_manifest_path = path

def get_outbound_manifest_name():
    file_name = os.path.basename(outbound_manifest_path)
    return file_name

# retrieve data from save file
def get_manifest():
    return [[tuple(item) for item in row] for row in read_save_file("manifest_data")]

# write to a new manifest file
def write_manifest(data):
    try:
        with open(outbound_manifest_path, 'w+') as f:
            for row_idx in reversed(range(len(data))):
                row = data[row_idx]
                for col_idx in range(len(row)):
                    item = row[col_idx]
                    index = f"[{len(data) - row_idx :02d},{col_idx + 1:02d}]" # indexed from reverse so subtract the row length
                    weight = f"{{{int(item[0]):05d}}}"
                    container = item[1] 
                    f.write(f"{index}, {weight}, {container}\n")
    except Exception:
        try:
            new_desktop = os.path.splitext(os.path.basename(outbound_manifest_path))[0] + '.txt'
            new_desktop = os.path.join('C:\\Users\\Public\\Desktop', new_desktop)
            with open(new_desktop, 'w+') as f:
                for row_idx in reversed(range(len(data))):
                    row = data[row_idx]
                    for col_idx in range(len(row)):
                        item = row[col_idx]
                        index = f"[{len(data) - row_idx :02d},{col_idx + 1:02d}]" # indexed from reverse so subtract the row length
                        weight = f"{{{int(item[0]):05d}}}"
                        container = item[1] 
                        f.write(f"{index}, {weight}, {container}\n")
        except Exception:
            try:
                appdata_path = os.getenv("LOCALAPPDATA")
                cargosail_folder = os.path.join(appdata_path, 'CargoSail')
                new_desktop = os.path.splitext(os.path.basename(outbound_manifest_path))[0] + '.txt'
                new_desktop = os.path.join(cargosail_folder, new_desktop)
                with open(new_desktop, 'w+') as f:
                    for row_idx in reversed(range(len(data))):
                        row = data[row_idx]
                        for col_idx in range(len(row)):
                            item = row[col_idx]
                            index = f"[{len(data) - row_idx :02d},{col_idx + 1:02d}]" # indexed from reverse so subtract the row length
                            weight = f"{{{int(item[0]):05d}}}"
                            container = item[1] 
                            f.write(f"{index}, {weight}, {container}\n")
            except Exception:
                pass
            

def set_move_info(total_moves, total_minutes, current_move_number, current_move_from, current_move_to, estimated_time_for_move):
    """
        total_moves:                total number of moves
        total_minutes:              total estimated time for all moves (in minutes)
        current_move_number:        number of the current move being executed
        current_move_from:          the starting point of the current move
        current_move_to:            the endpoint of the current move
        estimated_time_for_move:    estimated time (in minutes) for the current move
    """
    
    global move_info
    move_info = (
        f"It will take {total_moves} moves and {total_minutes} minutes.\n"
        f"Move {current_move_number}/{total_moves}: "
        f"Move from {current_move_from} to {current_move_to}, "
        f"estimated: {estimated_time_for_move} minutes."
    )
    
    # Store changes per move - TEMP
    # with open(get_save_file_path(), 'a') as json_file:
    #         json.dump(move_data, json_file, indent=4)

def get_move_info():
    return move_info

def add_logEntry(message):
    url = "http://worldtimeapi.org/api/timezone/America/Los_Angeles"
    
    response = requests.get(url)
    
    date_and_time = ''
    
    if response.status_code == 200:
        data = response.json()
        
        date = data['datetime']
        date_and_time = date[:10] + ' ' + date[11:16] + '\t'
    
    logfile_path =  get_logfile_path()
    with open(logfile_path, 'a') as logfile:
        logfile.write('\n')
        logfile.write(date_and_time)
        logfile.write(message)
        
def write_save_file(key, entry):
    '''
        Give the key in the json file you want to access
        and the entry of what you want to be there
    '''
    
    if not save_file_path:
        return
    
    try:
        with open(save_file_path, 'r') as json_file:
            data = json.load(json_file)    
    except Exception:
        data = {}
        
    data[key] = entry
    
    with open(save_file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)
            
def read_save_file(key):
    '''
        Give the key in the json file you want to access 
        and it will return whatever is saved in the file 
    '''
    
    if not save_file_path:
        return ""
    
    try:
        with open(save_file_path, 'r') as json_file:
            data = json.load(json_file)
        entry = data.get(key)
    except Exception:
        entry = ""
    return entry

def delete_save_file():
    if os.path.exists(save_file_path):
        os.remove(save_file_path)      
        
def clear_save_file():
    name = read_save_file("name")
    delete_save_file()
    write_save_file("name", name)    
    
# pass in login popup and add note as arguments to avoid circular import 
def reposition_buttons(root, login_popup, add_note):
    loginButton = ttk.Button(root, text="Login", padding=(10, 10), command=lambda: login_popup(root))
    loginButton.place(anchor="ne", relx=1, rely=0, x=-5, y=5)

    addNoteButton = ttk.Button(root, text="Add Note", padding=(10, 10), command=lambda: add_note(root))
    addNoteButton.place(anchor="nw", relx=0, rely=0, x=5, y=5)