import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
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

def get_weight(container_name):
    for row in get_manifest():
        for col in row:
            if col[1] == container_name:
                return col[0]
    return 0

def display_operations(root, prev_frame):
    # destroys login page
    prev_frame.pack_forget()

    container_list = {
        "Unload": [],
        "Load": []
    }
    
    ordered_list = []
    
    # read from file if data is found add items else it is empty
    if read_save_file("ordered_list"):
        ordered_list = read_save_file("ordered_list")
    if read_save_file("container_list"):
        container_list = read_save_file("container_list")
    
    def update_list():
        container_listbox.delete(0, tk.END)  # Clear existing items
        for operation, value in ordered_list:
            container_listbox.insert(tk.END, f"{operation}: {value}")
            
        # Update data in the save file
        write_save_file("ordered_list", ordered_list)
        write_save_file("container_list", container_list)  
        
    def add_container(name, container_input):
        if name == '':
            return
        # get the weight
        weight = get_weight(name)
        # add the contaienr name and weight
        container_list["Load"].append([weight,name])
        ordered_list.append(["Load", name])
        container_input.delete(0, tk.END)
        update_list()

    def start_operation(root, load_unload_frame):
        if len(container_list["Load"]) == 0 and len(container_list["Unload"]) == 0:
            messagebox.showerror("Error", "Please select at least one container.")
        else:
            operations_screen(root, load_unload_frame, False)


    def get_container_list(container_list):
        return container_list

    # save current state for crash recovery
    write_save_file("state", 1)
            
    def remove_operation(root, listbox):
        for i in reversed(listbox.curselection()):
            if ordered_list[i][0] == 'Unload':
                for widget in cargo_frame.winfo_children():
                    if widget.cget("text") == ordered_list[i][1]:
                        widget.config(bg="SystemButtonFace")
                        break
                
            weight = get_weight(ordered_list[i][1])
            container_list[ordered_list[i][0]].remove([weight,ordered_list[i][1]])
            ordered_list.pop(i)
            update_list()
    

    # parent frame of the page
    load_unload_frame = ttk.Frame(root)
    load_unload_frame.pack(expand=1, fill="both")

    # create frames for visuals on screen
    done_button_frame = ttk.Frame(load_unload_frame)
    done_button_frame.pack(side="bottom", fill="x")
    
    select_container_frame = ttk.Frame(load_unload_frame)
    select_container_frame.place(relx=.05, rely=.25)
    
    list_container_frame = ttk.Frame(load_unload_frame)
    list_container_frame.place(relx=.80, rely=.25)
    
    cargo_frame = ttk.Frame(load_unload_frame)
    cargo_frame.place(relx=.5, rely=.5, anchor='center')
    
    reposition_buttons(root)

    done_button = ttk.Button(done_button_frame, text="Done", padding=(20, 10), command=lambda: start_operation(root, load_unload_frame))
    done_button.pack(pady=20)
    
    container_input = ttk.Entry(select_container_frame)
    container_input.grid(row=0, column=0)
    
    container_button = ttk.Button(select_container_frame, text="Load", command=lambda: add_container(container_input.get(), container_input))
    container_button.grid(row=1, column=0)
    
    container_listbox = tk.Listbox(list_container_frame, width=30, height=10, selectmode=MULTIPLE)
    container_listbox.grid(row=1, column=0, padx=10, pady=10)
    
    container_button = ttk.Button(list_container_frame, text="Remove", command=lambda: remove_operation(root, container_listbox))
    container_button.grid(row=2, column=0)

    listbox_label = ttk.Label(list_container_frame, text="Containers to Load/Unload:", anchor="w", justify="left")
    listbox_label.grid(row=0, column=0)
    
    hover_label = ttk.Label(load_unload_frame, text="", font=("Arial", 12), relief="solid", borderwidth=1)

    
    # display the ship's current cargo
    display_current_cargo(cargo_frame, get_manifest(), container_list, hover_label, update_list, ordered_list)
    #ship_table = Table(cargo_frame, get_manifest())



#def operations_screen(root,frame1):
    #frame1.pack_forget()

def darkenCell(label, container_list, name, update_list, ordered_list):
    current_color = label.cget("bg")
    
    if current_color == "red":
        label.config(bg="SystemButtonFace")
        weight = get_weight(name)
        if [weight,name] in container_list["Unload"]:
            container_list["Unload"].remove([weight,name])
            ordered_list.remove(["Unload", name])
            update_list()
    else:
        label.config(bg="red")
        # get the weight
        weight = get_weight(name)
        # add the container name and weight
        container_list["Unload"].append([weight,name])
        ordered_list.append(["Unload", name])
        update_list()
        
def display_current_cargo(frame, current_cargo, container_list, hover_label, update_list, ordered_list):
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
            
            recover_darkenCells(cell, truncated_value, update_list)
            
            if not(truncated_value == "UNUSED" or truncated_value == "NAN"):
                cell.bind("<Button 1>",lambda event, name=current_cargo[i][j][1],label=cell:[darkenCell(label, container_list, name, update_list, ordered_list)])
                cell.bind("<Enter>", lambda event, row=i, col=j,current_cargo=current_cargo,hover_label=hover_label:show_hover_label(event, row, col,current_cargo,hover_label))
                cell.bind("<Leave>", lambda event, hover_label=hover_label:hide_hover_label(event, hover_label))


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


def recover_darkenCells(cell, truncated_value, update_list):
        saved_list = read_save_file("ordered_list")
        if saved_list:
            r = len(saved_list)
            for k in range(r):
                if truncated_value == saved_list[k][1][:7]:
                    cell.config(bg="red")
                    update_list()