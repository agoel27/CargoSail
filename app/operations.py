import tkinter as tk
from tkinter import *

from app.popup_login import login_popup
from app.add_note import add_note
from app.operations_screen import operations_screen
from app.table import Table
from config import *

# root = tk.Tk()
# array = [
#     ["walmart", "costco", "uniqlo"],
#     ["Honda", "Subaru", "Jeep"],
#     ["Acura", "Toyota", "Saab"]
    
# ]
def display_operations(root, selection):
    # destroys login page
    selection.pack_forget()

    # parent frame of the page
    load_unload_frame = tk.Frame(root)
    load_unload_frame.pack(expand=1, fill="both")
    
    # create frames for visuals on screen
    done_button_frame = tk.Frame(load_unload_frame)
    done_button_frame.pack(side="bottom", fill="x")
    
    select_container_frame = tk.Frame(load_unload_frame)
    select_container_frame.place(relx=.05, rely=.25)
    
    list_container_frame = tk.Frame(load_unload_frame)
    list_container_frame.place(relx=.80, rely=.25)
    
    cargo_frame = tk.Frame(load_unload_frame)
    cargo_frame.place(relx=.5, rely=.5, anchor='center')

    # place and define buttons/labels/entry box etc.
    loginButton = Button(load_unload_frame, text="Login", padx=10, pady=10, command= lambda:login_popup(root))
    loginButton.place(anchor="ne", relx=1, rely=0, x=-5, y=5)
    
    addNoteButton = Button(load_unload_frame, text="Add Note", padx=10, pady=10, command=lambda:add_note(root))
    addNoteButton.place(anchor="nw", relx=0, rely=0, x=5, y=5)
    
    done_button = Button(done_button_frame, text="Done", command=lambda: operations_screen(root, load_unload_frame), padx=20, pady=10)
    done_button.pack(pady=20)
    
    container_input = tk.Entry(select_container_frame)
    container_input.grid(row=0, column=0)
    
    container_button = Button(select_container_frame, text="Load", bg="red", command=lambda: container_list.insert(0, container_input.get()))
    container_button.grid(row=1, column=0)
    
    container_list_label = Label(list_container_frame, text="Containers to Load/Unload:", wraplength=75, anchor="w", justify="left")
    container_list_label.grid(row=0, column=0)
    
    container_list = Listbox(list_container_frame)
    container_list.grid(row=1, column=0)
    hover_label = tk.Label(load_unload_frame, bg="yellow", text="", font=("Arial", 12), relief="solid", borderwidth=1)


    # display the ship's current cargo
    display_current_cargo(cargo_frame, get_manifest(), container_list,hover_label)
    #ship_table = Table(cargo_frame, get_manifest())

def darkenCell(label):
    label.config(bg="red")

#def operations_screen(root,frame1):
    #frame1.pack_forget()


def display_current_cargo(frame, current_cargo, container_list,hover_label):
    rows = len(current_cargo)
    columns = len(current_cargo[0])
    for i in range(rows):
        for j in range(columns):
            truncated_value = current_cargo[i][j][1][:7]

            if truncated_value == "UNUSED":
                cell = tk.Label(frame, borderwidth=1, relief="solid", width=7, height=2)
            elif truncated_value == "NAN":
                cell = tk.Label(frame, borderwidth=1, relief="solid", width=7, height=2, bg="gray")
            else:
                cell = tk.Label(frame, text=truncated_value, borderwidth=1, relief="solid", width=7, height=2, font=("Arial", 12), anchor="center")
            cell.grid(row=i, column=j, sticky="nsew")
            if not(truncated_value == "UNUSED" or truncated_value == "NAN"):
                cell.bind("<Button 1>",lambda event, name=truncated_value,label=cell:[container_list.insert(0,name),darkenCell(label)])
                cell.bind("<Enter>", lambda event, row=i, col=j,current_cargo=current_cargo,hover_label=hover_label:show_hover_label(event, row, col,current_cargo,hover_label))
                cell.bind("<Leave>", hide_hover_label)

def show_hover_label(event, row, col,data,hover_label):
        """
        show hover_label with text of hovered cell

        event:  tkinter event object
        row:    row index of hovered cell
        col:    column index of hovered cell
        """
        text = data[row][col][1]
        if text:  # only show hover_label if there's text
            hover_label.config(text=text)
            hover_label.place(relx=0.5, rely=0.1, anchor="c")

def hide_hover_label(event,hover_label):
        """
        hide hover_label when mouse leaves a cell.
        """
        if hover_label.winfo_exists():
            hover_label.place_forget()
def myFunc(name):
    print(name)



# display_operations(root)
# root.geometry("800x600")
# root.mainloop()



