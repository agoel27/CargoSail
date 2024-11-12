import os
from tkinter import *

def add_note(root):
    '''
        Call this function to get a popup window to add a note
        
        To call it, do: 
            command=lambda:add_note(root)
        in the button
        
        Note: I cant figure out how to make the logfile path a 
        global variable so for now it doesnt do anything
    '''    

    popup = Toplevel(root)
    popup.geometry("300x150")
    popup.title("Add Note")
    
    width = 400
    height = 180
    
    # https://stackoverflow.com/questions/73184529/tkinter-make-my-pop-up-window-in-middle-of-the-screen
    screen_width = popup.winfo_screenwidth()
    screen_height = popup.winfo_screenheight()
    x_cordinate = int((screen_width / 2) - (width / 2))
    y_cordinate = int((screen_height / 2) - (height / 2))
    popup.geometry(f"{width}x{height}+{x_cordinate}+{y_cordinate}")
    
    # https://stackoverflow.com/questions/41946222/how-do-i-create-a-popup-window-in-tkinter
    popup.grab_set()
    
    def add_note_to_log(): # https://www.geeksforgeeks.org/python-tkinter-text-widget/
        user_input = text_box.get("1.0", "end-1c")
        
        # with open(logfile_path, 'a') as logfile:
        #     logfile.write(user_input)
        popup.destroy()

    label = Label(popup, text="Enter some text:")
    label.pack(pady=10)

    text_box = Text(popup, height=4, width=40)
    text_box.pack(pady=5)

    close_button = Button(popup, text="Add Note", command=add_note_to_log, height=2, width=15)
    close_button.pack(pady=5)