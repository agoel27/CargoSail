# stores name of current user
global current_username

# global functions for easy access from all files
# to access from the app folder do: from config import *
def set_logfile_path(path):
    global logfile_path
    logfile_path = path
    
def get_logfile_path():
    return logfile_path

def add_logEntry(message):
    logfile_path =  get_logfile_path()
    with open(logfile_path, 'a') as logfile:
        logfile.write(message)