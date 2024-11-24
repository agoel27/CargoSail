# global functions for easy access from all files
# to access from the app folder do: from config import *

import requests, json, os

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

def get_manifest():
    # retrieve data during runtime
    #return manifest_data 
    
    # retrieve data from save file
    return read_save_file("manifest_data")


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