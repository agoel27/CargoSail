import os 
import re
import tkinter as tk
from tkinter import *
from config import *

def input_validation(input_field, error_message):
    
    # if true input is correct, otherwise false
    flag = False
    
    # store name from input field
    name = input_field.get()
    
    # regex used to find symbols or no input in username
    symbols = "[@_!#$%^&*()<>?/|}{~:]"
    blank = " +"

    # input restrictions
    if len(name) > 30:
        error_message.config(text="Error: name cannot exceeds 30-characters.", fg="red")
       
    elif name.isdigit():
        error_message.config(text="Error: name cannot consist of digits only", fg="red")
       
    elif name == "":
        error_message.config(text="Error: name cannot be blank", fg="red")  
    
    elif re.search(blank, name):
        error_message.config(text="Error: name cannot be blank", fg="red")  
       
    elif re.search(symbols, name):
        error_message.config(text="Error: name cannot contain any symbols", fg="red")
    
    else:
        # input accepted
        return True  