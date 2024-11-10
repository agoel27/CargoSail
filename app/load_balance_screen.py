
import tkinter as Tk
from tkinter import *

def login_popup(root):
    
    # create login popup frame
    login = Toplevel()
    login.title("Login")
    login.geometry("250x150") 
    
    # selects popup as active window
    login.focus()
    
    # prevents user from interacting w/ parent window
    login.grab_set()
    
    # position pop up to center of window
    x = root.winfo_x()
    y = root.winfo_y()
    login.geometry("+%d+%d" %(x+275,y+250))
    
    # prevents resizing window
    login.resizable(False, False)
    
    # message top of input field
    message = Label(login, text='Enter Name: ')
    message.place(relx = 0.4, rely = 0.35, anchor = 'center')
    
    # input field
    input_field = Entry(login)
    input_field.place(relx = 0.5, rely = 0.5, anchor = 'center')
    
    # sign in button when pressed closes top window
    sign_in = Button(login, text="Sign in", command= login.destroy)
    sign_in.place(x=100, y=95)
    

def load_balance(root,frame1):
    
    # destroys previous frame
    frame1.place_forget()

    loginButton = Button(root, text="Login" , padx=10, pady=10, command= lambda:login_popup(root))
    loginButton.pack(anchor="ne", padx=5, pady=5)    

    # frame for load/unload and balance buttons to have them centered
    loadBalance_frame = Frame(root)
    loadBalance_frame.place(relx=0.5, rely=0.5, anchor="center")

    loadUnloadButton = Button(loadBalance_frame, text="Load/Unload", padx=10, pady=10)
    loadUnloadButton.grid(row=0, column=0, padx=5)

    balanceButton = Button(loadBalance_frame, text="Balance", padx=10, pady=10)
    balanceButton.grid(row=0, column=1, padx=5)
    
    
    