# global functions for easy access from all files
# to access from the app folder do: from config import *
def set_logfile_path(path):
    """
    Set the global logfile_path variable.

    Args:
    path (str): The absolute path of the logfile.
    """
    global logfile_path
    logfile_path = path
    
def get_logfile_path():
    print(logfile_path)
    return logfile_path