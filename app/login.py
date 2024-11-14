import os
import tkinter as tk
from tkinter import *
from app.load_balance_screen import load_balance
from app.logfile import add_logEntry

def login_store(input_field):
    name = input_field.get()
    
    # Test logging in with more than 30 characters
    # Test logging in with exactly 30 characters
    # Test leaving log in text box blank
    # Test logging in with numbers 
    # Test logging in with a regular name
    # Test logging in with a regular name with a space
    # Test logging in with a special character like (@#$%^)

    
    # if name.
    
    add_logEntry(name)
    

def login_screen(root):
    
    # create login screen frame
    login_frame = tk.Frame(root)
    login_frame.place(relx=0.5, rely=0.5, anchor="c")
    
    # message on top of input field
    message = Label(login_frame, text='Enter Name: ')
    message.grid(row=0, column=0)
    
    # input field
    input_field = Entry(login_frame)
    input_field.grid(column=0, row=1)
    
    # sign in button when pressed goes to load_balance
    sign_in = Button(login_frame, text="Sign in", command= lambda: [login_store(input_field), load_balance(root, login_frame)])
    sign_in.grid(column=0, row=2)
    

