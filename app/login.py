import os, re, json
import tkinter as tk
from tkinter import *
from tkinter import ttk
from config import *
from app.input_valid import input_validation
from app.load_balance_screen import load_balance

def login_store(root, input_field, login_frame, error_message):
    
    validation_test = input_validation(input_field, error_message)
      
    if validation_test:
        entry = input_field.get() + " has signed in" 
        
        # signing in new name
        add_logEntry(entry)
        
        set_username(input_field.get())
        
        write_save_file("name", input_field.get())
        
        name_label = root.nametowidget("name_label")
        name_label.configure(text=f"Logged in: {input_field.get()}")
        
        # proceed to the load balance page
        load_balance(root, login_frame)

def login_screen(root):
    login_frame = ttk.Frame(root)
    login_frame.pack(expand=True)

    name = read_save_file("name")

    if name:
        name_label = root.nametowidget("name_label")
        name_label.configure(text=f"Logged in: {name}")

        set_username(name)
        return load_balance(root, login_frame)
    
    # create login screen frame
    
    # message on top of input field
    message = ttk.Label(login_frame, text='Enter Name ')
    message.grid(row=0, column=0)
    
    # error message on top of input
    error_message = ttk.Label(login_frame, text="")
    error_message.grid(row=1, column=0)
    
    # input field
    input_field = ttk.Entry(login_frame)
    input_field.grid(row=3, column=0)
    
    # sign in button when pressed goes to load_balance
    sign_in = ttk.Button(login_frame, text="Sign in", padding=(5,5), command= lambda: login_store(root, input_field, login_frame, error_message))
    sign_in.grid(row=4, column=0, padx=10, pady=10)