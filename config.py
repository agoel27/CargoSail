# global functions for easy access from all files
# to access from the app folder do: from config import *

import requests

def set_logfile_path(path):
    global logfile_path
    logfile_path = path
    
def get_logfile_path():
    return logfile_path

def set_username(username):
    global user
    user = username
    
def get_username():
    return user

def set_manifest(data):
    global manifest_data
    manifest_data = data

def get_manifest():
    return manifest_data

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