import tkinter as Tk
from tkinter import ttk
from tkinter import *
from app.login import *
from config import *
from app.input_valid import *
    
def login_store(root, new_username, login_popup_frame, error_message):
    
    validation_test = input_validation(new_username, error_message)
      
    if validation_test:
        entryNew = new_username.get() + " has signed in\n" 
        add_logEntry(entryNew)
        
        set_username(new_username.get())
        
        write_save_file("name", new_username.get())

        # update the current name label
        name_label = root.nametowidget("name_label")
        name_label.configure(text=f"Logged in: {new_username.get()}")
        
        # exits popup return to load balance
        login_popup_frame.destroy()
     

def login_popup(root):
    # create login popup frame
    login = Toplevel()
    login.title("Login")
    login.configure(bg="#f5f6f7")
    login.geometry("250x150") 
    
    # selects popup as active window
    login.focus()
    
    # position pop up to center of window
    root_x = root.winfo_x()
    root_y = root.winfo_y()
    root_width = root.winfo_width()
    root_height = root.winfo_height()
    
    login_width = 250
    login_height = 150

    # Center the popup relative to the root window
    x = root_x + (root_width // 2) - (login_width // 2)
    y = root_y + (root_height // 2) - (login_height // 2)
    login.geometry(f"{login_width}x{login_height}+{x}+{y}")
    
    # prevents user from interacting w/ parent window
    login.grab_set()
    
    # prevents resizing window
    login.resizable(False, False)
    
    # message top of input field
    message = ttk.Label(login, text='Enter Name: ')
    message.place(relx = 0.5, rely = 0.33, anchor = 'center')
    
    # error message on top of input
    error_message = ttk.Label(login, text="")
    error_message.place(relx=0.5, rely=0.15, anchor='center')
    
    # input field
    input_field = ttk.Entry(login)
    input_field.place(relx = 0.5, rely = 0.5, anchor='center')
    
    # sign in button when pressed closes top window
    sign_in = ttk.Button(login, text="Sign in", command= lambda: [login_store(root, input_field, login, error_message)])
    sign_in.place(relx=0.5, rely=0.7, anchor='center')
