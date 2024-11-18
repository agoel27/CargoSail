# stores name of current user
global current_username

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