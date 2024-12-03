import os
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from config import *

def add_note(root):
    '''
        Call this function to get a popup window to add a note
        
        To call it, do: 
            command=lambda:add_note(root)
        in the button
    '''    

    popup = Toplevel(root)
    popup.configure(bg="#f5f6f7")
    popup.geometry("400x180")
    popup.title("Add Note")
    
    # https://stackoverflow.com/questions/73184529/tkinter-make-my-pop-up-window-in-middle-of-the-screen
    root_x = root.winfo_x()
    root_y = root.winfo_y()
    root_width = root.winfo_width()
    root_height = root.winfo_height()
    
    add_note_width = 400
    add_note_height = 180

    # Center the popup relative to the root window
    x = root_x + (root_width // 2) - (add_note_width // 2)
    y = root_y + (root_height // 2) - (add_note_height // 2)
    popup.geometry(f"{add_note_width}x{add_note_height}+{x}+{y}")

    # https://stackoverflow.com/questions/41946222/how-do-i-create-a-popup-window-in-tkinter
    popup.grab_set()
    
    # https://www.geeksforgeeks.org/python-tkinter-text-widget/
    def add_note_to_log(): 
        user_input = text_box.get("1.0", "end-1c")
        
        error_message.config(text="")
        
        if user_input == '':
            error_message.config(text="Error: Message cannot be blank", fg="red")
            return
        elif len(user_input) > 2000:
            error_message.config(text="Error: Message cannot exceed 2000 characters", fg="red")
            return
        user_input += '\n'
        add_logEntry(user_input)
        popup.destroy()

    label = ttk.Label(popup, text="Add a Note:")
    label.pack(pady=(10,0))

    error_message = ttk.Label(popup, text="", foreground="red")
    error_message.pack(pady=(1,4))

    text_box = Text(popup, height=4, width=40)
    text_box.pack(pady=1)

    close_button = ttk.Button(popup, text="Add Note", command=add_note_to_log)
    close_button.pack(pady=5)