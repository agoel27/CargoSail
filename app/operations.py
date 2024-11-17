import tkinter as tk
from tkinter import *
from app.load_balance_screen import login_popup
from app.operations_screen import operations_screen
from app.table import Table

# root = tk.Tk()
array = [
    ["walmart", "costco", "uniqlo"],
    ["Honda", "Subaru", "Jeep"],
    ["Acura", "Toyota", "Saab"]
    
]
def display_operations(root, selection):
    # destroys login page
    selection.pack_forget()

    # parent frame of the page
    load_unload_frame = tk.Frame(root)
    load_unload_frame.pack(expand=1, fill="both")
    
    # create frames for visuals on screen
    done_button_frame = tk.Frame(load_unload_frame)
    done_button_frame.place(relx=0, rely=1, anchor="sw")
    select_container_frame = tk.Frame(load_unload_frame)
    select_container_frame.place(relx=.05, rely=.25)
    list_container_frame = tk.Frame(load_unload_frame)
    list_container_frame.place(relx=.80, rely=.25)
    cargo_frame = tk.Frame(load_unload_frame)
    cargo_frame.place(relx=.5, rely=.5, anchor='center')

    # place and define buttons/labels/entry box etc.
    done_button = Button(done_button_frame, text="Done", command=lambda: operations_screen(root, load_unload_frame))
    done_button.grid(row=0, column=0)
    container_input = tk.Entry(select_container_frame)
    container_input.grid(row=0, column=0)
    container_button = Button(select_container_frame, text="load", bg="red", command=lambda: container_list.insert(0, container_input.get()))
    container_button.grid(row=1, column=0)
    container_list_label = Label(list_container_frame, text="Containers to Load/Unload:", wraplength=75, anchor="w", justify="left")
    container_list_label.grid(row=0, column=0)
    container_list = Listbox(list_container_frame)
    container_list.grid(row=1, column=0)

    # display the ship's current cargo
    #display_current_cargo(cargo_frame, array, container_list)
    Table(cargo_frame, array)

# def operations_screen(root, frame1):
#     frame1.pack_forget()

def display_current_cargo(frame, current_cargo, container_list):
    for row_index, row in enumerate(current_cargo):
        for col_index, value in enumerate(row):
            label = tk.Label(frame, text=value, borderwidth=1, relief="solid")
            label.grid(row=row_index, column=col_index, sticky="nsew")
            label.bind("<Button 1>", lambda event, name=value: container_list.insert(0, name))

# def myFunc(name):
#     print(name)

# display_operations(root)
# root.geometry("800x600")
# root.mainloop()


