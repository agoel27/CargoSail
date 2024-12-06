import tkinter as tk
from tkinter import *
from tkinter import ttk
from app.popup_login import login_popup
from app.add_note import add_note
from app.table import Table
from app.current_move_frame import CurrentMoveFrame
from config import *

def operations_screen(root, prev_frame):
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
    truck_frame.place(relx=0.25, rely=0.5, anchor="c") # 0.64

    # place table in buffer area frame
    buffer_area_table = Table(buffer_area_frame, buffer_data)

    # place table in ship frame
    ship_table = Table(ship_frame, get_manifest())
    ship_table.flash_cells((0, 0), (2, 2))

    # place truck in truck frame
    truck_label = tk.Label(truck_frame, text="Truck", borderwidth=1, relief="solid", height=2, width=7, font=("Arial", 12), anchor="center")
    truck_label.grid(row=0, column=0, sticky="nsew")

    # place current move frame in operations screen frame
    current_move_frame = CurrentMoveFrame(root, operations_screen_frame, 19, 19)
    set_move_info(19, 48, 19, "truck", "[03,08]", 7)
    current_move_frame.create_current_move_frame()

    
