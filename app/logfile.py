import os
from config import *

def add_logEntry(message):
    
    # store CargoSail logpath
    logfile_path =  get_logfile_path()
    
    with open(logfile_path, 'a') as logfile:
        logfile.write(message)