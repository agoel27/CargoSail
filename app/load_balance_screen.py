import tkinter as tk
from tkinter import *
from tkinter import filedialog, messagebox, ttk
from app.operations import display_operations
from app.operations_screen import operations_screen
from config import *
from app.popup_login import login_popup
from app.add_note import add_note

def load_file():
    e = None

    file_path = filedialog.askopenfilename(
        title="Select file",
        filetypes=(("Text files", "*.txt"), ("All files", "*.*"))
    )
    
    if file_path:
        try:
            # open the file and store its contents
            with open(file_path, 'r') as file:
                content = file.readlines()

        except Exception as exc:
            messagebox.showerror("Error", f"Could not read file: {exc}")
            e = exc
            return False

        data = [[None for _ in range(12)] for _ in range(8)]
        
        desktop_path = os.path.normpath(os.path.expanduser("~/Desktop"))
        file_name = os.path.splitext(os.path.basename(file_path))[0]
        file_name += 'OUTBOUND.txt'
        write_save_file('manifest_name', file_name)
        
        outbound_manifest_path = os.path.join(desktop_path, file_name)
        set_outbound_manifest_path(outbound_manifest_path)

        # parse lines in the format: [row,column], {weight}, name
        for line in content:
            try:
                parts = line.strip().split(", ")
                row, col = map(int, parts[0][1:-1].split(","))
                weight = int(parts[1][1:-1])
                name = parts[2]
                data[8 - row][col - 1] = (weight, name)
            except Exception as exc:
                messagebox.showerror("Error", f"Could not read Manifest")
                e = exc
                return False
        
        if not e:
            set_manifest(data)
            return True     # return here so make sure the file is actually read

    return False

def load_operation(root, load_balance_frame):
    if load_file():
        write_save_file("operation", "load_unload")
        display_operations(root, load_balance_frame)
        
def balance_operation(root, load_balance_frame):
    if load_file():
        write_save_file("operation", "balance")    
        operations_screen(root, load_balance_frame)


def load_balance(root, prev_frame):
    # destroys login page
    prev_frame.pack_forget()
    # frame for load/unload and balance buttons to have them centered
    loadBalance_frame = ttk.Frame(root)
    loadBalance_frame.pack(fill=tk.BOTH, expand=True)  # Only occupies remaining space below the header

    loadUnloadButton = ttk.Button(loadBalance_frame, text="Load/Unload", padding=(10,10), command=lambda:load_operation(root, loadBalance_frame))
    loadUnloadButton.place(anchor="c", relx=0.4, rely=0.5)

    balanceButton = ttk.Button(loadBalance_frame, text="Balance", padding=(10,10), command=lambda:balance_operation(root, loadBalance_frame))
    balanceButton.place(anchor="c", relx=0.6, rely=0.5)
    
    reposition_buttons(root, login_popup=login_popup, add_note=add_note)