
import tkinter as Tk
from tkinter import *
from tkinter import filedialog, messagebox
from .add_note import *
from app.popup_login import login_popup    
from app.operations import display_operations

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

def load_operation(root, load_balance_frame):
    if load_file():
        display_operations(root, load_balance_frame)
        
def balance_operation(root, load_balance_frame):
    if load_file():
        display_operations(root) # for now. will have to change later when we have implementation done


def load_balance(root, login_frame, current_username):
    
    # destroys login page
    login_frame.place_forget()

    loginButton = Button(root, text="Login" , padx=10, pady=10, command= lambda:login_popup(root, current_username))
    loginButton.pack(anchor="ne", padx=5, pady=5)    

    # frame for load/unload and balance buttons to have them centered
    loadBalance_frame = Frame(root)
    loadBalance_frame.place(relx=0.5, rely=0.5, anchor="center")

    loadUnloadButton = Button(loadBalance_frame, text="Load/Unload", padx=10, pady=10, command=lambda:load_operation(root, loadBalance_frame))
    loadUnloadButton.grid(row=0, column=0, padx=5)

    balanceButton = Button(loadBalance_frame, text="Balance", padx=10, pady=10, command=lambda:balance_operation(root, loadBalance_frame))
    balanceButton.grid(row=0, column=1, padx=5)
    
    
    