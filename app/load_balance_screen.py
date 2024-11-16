
import tkinter as Tk
from tkinter import *
from .add_note import *
from app.popup_login import login_popup    
from app.operations import displayOperations

def load_balance(root, login_frame, current_username):
    
    # destroys login page
    login_frame.place_forget()

    loginButton = Button(root, text="Login" , padx=10, pady=10, command= lambda:login_popup(root, current_username))
    loginButton.pack(anchor="ne", padx=5, pady=5)    

    # frame for load/unload and balance buttons to have them centered
    loadBalance_frame = Frame(root)
    loadBalance_frame.place(relx=0.5, rely=0.5, anchor="center")

    loadUnloadButton = Button(loadBalance_frame, text="Load/Unload", padx=10, pady=10, command=lambda:displayOperations(root))
    loadUnloadButton.grid(row=0, column=0, padx=5)

    balanceButton = Button(loadBalance_frame, text="Balance", padx=10, pady=10, command=lambda:displayOperations(root))
    balanceButton.grid(row=0, column=1, padx=5)
    
    
    