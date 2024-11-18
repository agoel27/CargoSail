import re
import datetime
import tkinter as Tk
from tkinter import *
from app.login import *
from app.input_valid import *
import config
    
def login_store(root, new_username, login_popup_frame, error_message):
    
    validation_test = input_validation(new_username, error_message)
      
    if validation_test:

        # date and time formatted
        date = datetime.datetime.now().strftime("%B %d %G: %H:%M")
        
        # signing out previous name
        entryOld = date + " "+ config.current_username  + " signs out\n" 
        add_logEntry(entryOld)
        
        # signing in new name
        entryNew = date + " "+ new_username.get() + " signs in\n" 
        add_logEntry(entryNew)
        
        # store new name to global variable
        config.current_username = new_username.get()
        
        # exits popup return to load balance
        login_popup_frame.destroy()
     
        

def login_popup(root):
    
    # create login popup frame
    login = Toplevel()
    login.title("Login")
    login.geometry("250x150") 
    
    # selects popup as active window
    login.focus()
    
    # position pop up to center of window
    x = root.winfo_x()
    y = root.winfo_y()
    login.geometry("+%d+%d" %(x+275,y+250))
    
    # prevents user from interacting w/ parent window
    login.grab_set()
    
    # prevents resizing window
    login.resizable(False, False)
    
    # message top of input field
    message = Label(login, text='Enter Name: ')
    message.place(relx = 0.4, rely = 0.35, anchor = 'center')
    
    # error message on top of input
    error_message = Label(login, text="")
    error_message.grid(row=1, column=0)
    
    # input field
    input_field = Entry(login)
    input_field.place(relx = 0.5, rely = 0.5, anchor = 'center')
    
    # sign in button when pressed closes top window
    sign_in = Button(login, text="Sign in", command= lambda: [login_store(root, input_field, login, error_message)])
    sign_in.place(x=100, y=95)
    