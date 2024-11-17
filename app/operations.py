import tkinter as tk
from tkinter import *
from app.load_balance_screen import login_popup
from app.operations_screen import operations_screen

# root = tk.Tk()
array = [
    ["walmart", "costco", "uniqlo"],
    ["Honda", "Subaru", "Jeep"],
    ["Acura", "Toyota", "Saab"]
    
]
def displayOperations(root, selection):
    # destroys login page
    selection.pack_forget()
    
    #parent frame of the page
    loadUnloadFrame = tk.Frame(root)
    loadUnloadFrame.pack(expand=1,fill="both")
    
    #create frames for visuals on screen
    doneButtonFrame = tk.Frame(loadUnloadFrame)
    doneButtonFrame.place(relx=0,rely=1,anchor="sw")
    selectContainerFrame = tk.Frame(loadUnloadFrame)
    selectContainerFrame.place(relx=.05,rely=.25)
    listContainerFrame = tk.Frame(loadUnloadFrame)
    listContainerFrame.place(relx=.80,rely=.25)
    cargoFrame = tk.Frame(loadUnloadFrame)
    cargoFrame.place(relx=.5,rely=.5,anchor='center')

    #place and define buttons/labels/entryBox etc..
    doneButton = Button(doneButtonFrame, text="Done",command=lambda:operations_screen(loadUnloadFrame))
    doneButton.grid(row=0,column=0)
    containerInput = tk.Entry(selectContainerFrame)
    containerInput.grid(row=0,column=0)
    containerButton = Button(selectContainerFrame,text="load",bg="red",command=lambda:containerList.insert(0,containerInput.get()))
    containerButton.grid(row=1,column=0)
    containerListLabel = Label(listContainerFrame,text= "Containers to Load/Unload:",wraplength=75,anchor="w",justify="left")
    containerListLabel.grid(row=0,column=0)
    containerList = Listbox(listContainerFrame)
    containerList.grid(row=1,column=0)

    #display the ships current cargo
    displayCurrentCargo(cargoFrame,array,containerList)

# def operations_screen(root,frame1):
#     frame1.pack_forget()

def displayCurrentCargo(frame,CurrentCargo,containerList):
    for row_index, row in enumerate(CurrentCargo):
        for col_index, value in enumerate(row):
            label = tk.Label(frame, text=value, borderwidth=1, relief="solid")
            label.grid(row=row_index, column=col_index, sticky="nsew")
            label.bind("<Button 1>",lambda event, name=value:containerList.insert(0,name))


# def myFunc(name):
#     print(name)

# displayOperations(root)
# root.geometry("800x600")
# root.mainloop()


