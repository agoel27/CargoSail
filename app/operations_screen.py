import tkinter as tk
from tkinter import *
from tkinter import ttk
from app.popup_login import login_popup
from app.add_note import add_note
from app.table import Table
from app.current_move_frame import CurrentMoveFrame
from config import *
from balance_problem import a_star, get_balance_operations_info
from a_star import a_star_load_unload, get_operations_info

def operations_screen(root, prev_frame, is_balance):
    buffer_data = [[(0, "UNUSED") for _ in range(24)] for _ in range(4)]

    # destroys previous frame
    prev_frame.pack_forget()
    
    # save current state for crash recovery 
    # write_save_file("state", 2)

    # create operations screen frame
    operations_screen_frame = ttk.Frame(root)
    operations_screen_frame.pack(expand=1, fill="both")

    # create buffer area frame
    buffer_area_frame = ttk.Frame(operations_screen_frame)
    buffer_area_frame.place(relx=0.5, rely=0.85, anchor="c") # 0.7 

    # create ship frame
    ship_frame = ttk.Frame(operations_screen_frame)
    ship_frame.place(relx=0.75, rely=0.5, anchor="c") # 0.5 

    # create truck frame
    truck_frame = ttk.Frame(operations_screen_frame)
    truck_frame.place(relx=0.25, rely=0.65, anchor="c") # 0.64

    # place truck in truck frame
    truck_label = tk.Label(truck_frame, text="Truck", borderwidth=1, relief="solid", height=2, width=7, font=("Arial", 12), anchor="center")
    truck_label.grid(row=0, column=0, sticky="nsew")

    # place table in buffer area frame
    buffer_area_table = Table(buffer_area_frame, buffer_data, truck_label)

    # place table in ship frame
    ship_table = Table(ship_frame, get_manifest(), truck_label)

    #this is for balancing
    #----------------------------------------------------------------------------------------------
    if is_balance:
        solution_node = a_star(get_manifest())
        total_minutes, total_moves, balance_operations_list, manifest_data_of_solution_path = get_balance_operations_info(solution_node)

        # place current move frame in operations screen frame
        current_move_frame = CurrentMoveFrame(root, operations_screen_frame, total_moves, total_minutes, balance_operations_list)

        current_move_frame.create_current_move_frame(1, ship_table, manifest_data_of_solution_path)
    else:
    #---------------------------------------------------------------------------------------------
    #this will be for load/unload
        if read_save_file("container_list"):
            container_list = read_save_file("container_list")
        unload_list = container_list["Unload"]
        load_list = container_list["Load"]
        print(unload_list)
        print(load_list)
        solution_node = a_star_load_unload(get_manifest(),load_list,unload_list)
        total_minutes, total_moves, operations_list, manifest_data_of_solution_path = get_operations_info(solution_node)
        
        current_move_frame = CurrentMoveFrame(root, operations_screen_frame, total_moves, total_minutes, operations_list)
        current_move_frame.create_current_move_frame(1, ship_table, manifest_data_of_solution_path)
    #---------------------------------------------------------------------------------------------
    #create var to tell operations if its a load/unload or a balance operation


    
    reposition_buttons(root)