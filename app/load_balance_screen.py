
import tkinter as Tk
from tkinter import *
from tkinter import filedialog, messagebox
from .add_note import *
from app.popup_login import login_popup    
from app.operations import display_operations
from app.operations_screen import operations_screen
from app.add_note import add_note

def load_file():
    file_path = filedialog.askopenfilename(
        title="Select file",
        filetypes=(("Text files", "*.txt"), ("All files", "*.*"))
    )
    
    if file_path:
        try:
            # Open the file and store its content
            with open(file_path, 'r') as file:
                content = file.read()
                return True
        except Exception as e:
            messagebox.showerror("Error", f"Could not read file: {e}")
    
    return False

def load_operation(root, load_balance_frame, current_username):
    if load_file():
        display_operations(root, load_balance_frame, current_username)
        
def balance_operation(root, load_balance_frame, current_username):
    if load_file():
        operations_screen(root, load_balance_frame, current_username)


def load_balance(root, login_frame):
    
    # destroys login page
    login_frame.pack_forget()


    # frame for load/unload and balance buttons to have them centered
    loadBalance_frame = Frame(root)
    loadBalance_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

    loginButton = Button(loadBalance_frame, text="Login", padx=10, pady=10, command= lambda:login_popup(root, current_username))
    loginButton.place(anchor="ne", relx=1, rely=0, x=-5, y=5)

    addNoteButton = Button(loadBalance_frame, text="Add Note", padx=10, pady=10, command=lambda:add_note(root))
    addNoteButton.place(anchor="nw", relx=0, rely=0, x=5, y=5)

    loadUnloadButton = Button(loadBalance_frame, text="Load/Unload", padx=10, pady=10, command=lambda:load_operation(root, loadBalance_frame, current_username))
    loadUnloadButton.place(anchor="c", relx=0.4, rely=0.5)

    balanceButton = Button(loadBalance_frame, text="Balance", padx=10, pady=10, command=lambda:balance_operation(root, loadBalance_frame, current_username))
    balanceButton.place(anchor="c", relx=0.6, rely=0.5)
    
    
    