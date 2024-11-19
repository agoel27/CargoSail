
import tkinter as Tk
from tkinter import *
from tkinter import filedialog, messagebox
from app.popup_login import login_popup    
from app.operations import display_operations
from app.operations_screen import operations_screen
from app.add_note import add_note
from config import *

def load_file():
    ret = False

    file_path = filedialog.askopenfilename(
        title="Select file",
        filetypes=(("Text files", "*.txt"), ("All files", "*.*"))
    )
    
    if file_path:
        try:
            # open the file and store its contents
            with open(file_path, 'r') as file:
                content = file.readlines()
                ret = True

        except Exception as e:
            messagebox.showerror("Error", f"Could not read file: {e}")

        data = [[None for _ in range(12)] for _ in range(8)]
        
        manifest_error = False

        # parse lines in the format: [row,column], {weight}, name
        for line in content:
            try:
                parts = line.strip().split(", ")
                row, col = map(int, parts[0][1:-1].split(","))
                weight = int(parts[1][1:-1])
                name = parts[2]
                data[8 - row][col - 1] = (weight, name)
            except Exception as e:
                messagebox.showerror("Error", f"Could not read Manifest")
                manifest_error = True
                break
        
        if not manifest_error:
            set_manifest(data)

    return ret

def load_operation(root, load_balance_frame):
    if load_file():
        display_operations(root, load_balance_frame)
        
def balance_operation(root, load_balance_frame):
    if load_file():
        operations_screen(root, load_balance_frame)


def load_balance(root, login_frame):
    
    # destroys login page
    login_frame.pack_forget()

    # frame for load/unload and balance buttons to have them centered
    loadBalance_frame = Frame(root)
    loadBalance_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

    loginButton = Button(loadBalance_frame, text="Login", padx=10, pady=10, command= lambda:login_popup(root))
    loginButton.place(anchor="ne", relx=1, rely=0, x=-5, y=5)

    addNoteButton = Button(loadBalance_frame, text="Add Note", padx=10, pady=10, command=lambda:add_note(root))
    addNoteButton.place(anchor="nw", relx=0, rely=0, x=5, y=5)

    loadUnloadButton = Button(loadBalance_frame, text="Load/Unload", padx=10, pady=10, command=lambda:load_operation(root, loadBalance_frame))
    loadUnloadButton.place(anchor="c", relx=0.4, rely=0.5)

    balanceButton = Button(loadBalance_frame, text="Balance", padx=10, pady=10, command=lambda:balance_operation(root, loadBalance_frame))
    balanceButton.place(anchor="c", relx=0.6, rely=0.5)
    
    
    