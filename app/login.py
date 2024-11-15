import os
import re
import datetime
import tkinter as tk
from tkinter import *
from app.logfile import add_logEntry
from app.input_valid import input_validation
from app.load_balance_screen import load_balance

def login_store(root, input_field, login_frame, error_message):
    
    validation_test = input_validation(input_field,error_message)
      
    if validation_test:
        # date and time formatted
        date = datetime.datetime.now().strftime("%B %d %G: %H:%M")
        entry = date + " "+ input_field.get() + " signs in\n" 
        
         # signing in new name
        add_logEntry(entry)
        
        # proceed to the load balance page
        load_balance(root, login_frame, input_field) 

def login_screen(root):
    
    # create login screen frame
    login_frame = tk.Frame(root)
    login_frame.place(relx=0.5, rely=0.5, anchor="c")
    
    # message on top of input field
    message = Label(login_frame, text='Enter Name ')
    message.grid(row=0, column=0)
    
    # error message on top of input
    error_message = Label(login_frame, text="")
    error_message.grid(row=1, column=0)
    
    # input field
    input_field = Entry(login_frame)
    input_field.grid(row=3, column=0)
    
    # sign in button when pressed goes to load_balance
    sign_in = Button(login_frame, text="Sign in", command= lambda: login_store(root, input_field, login_frame, error_message))
    sign_in.grid(row=4, column=0, padx=10, pady=10)
    
