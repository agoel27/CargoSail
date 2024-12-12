import tkinter as tk
from tkinter import ttk
#from app.load_balance_screen import *
#from app.add_note import add_note
from tkinter import messagebox
import app.load_balance_screen as load_balance_screen
from config import *
import json

class CurrentMoveFrame:
    def __init__(self, root, frame, total_moves, total_minutes, operations_list):
        """
        initialize CurrentMoveFrame class

        USAGE: create CurrentMoveFrame obj, use set_move_info() in config.py to set data, call obj.create_current_move_frame()
        
        frame:                      frame to place the current move frame in
        total_moves:                total number of moves
        total_minutes:              total estimated time for all moves (in minutes)
        current_move_number:        number of the current move being executed
        current_move_from:          the starting point of the current move
        current_move_to:            the endpoint of the current move
        estimated_time_for_move:    estimated time (in minutes) for the current move
        """
        self.root = root # keep track of the root 
        self.frame = frame
        self.current_move_number = 1
        self.total_moves = total_moves
        self.total_minutes = total_minutes
        self.operations_list = operations_list
        self.saved = 0

    def finish_move(self, root, frame, table):
        # save the new manifest
        write_manifest(table.data)

        if self.current_move_number == self.total_moves:
            write_save_file("move_number", 0)
            messagebox.showinfo("Reminder", "Reminder to email the manifest!")
        load_balance_screen.load_balance(root, frame)
        

    def create_current_move_frame(self, current_move_number, table, manifest_data_of_solution_path):
        """
        create frame with the text displaying the move information
        """ 
        if current_move_number == 1:
            table.set_data(get_manifest())

        self.current_move_number = current_move_number
        set_move_info(self.total_moves, self.total_minutes, current_move_number, self.operations_list[current_move_number-1][0], self.operations_list[current_move_number-1][1], 7)
        if(self.operations_list[current_move_number-1][0] != "[truck]"):
            my_row, my_col = map(int, self.operations_list[current_move_number-1][0][1:-1].split(","))
        else:
            my_row, my_col = -1, -1
        if(self.operations_list[current_move_number-1][1] != "[truck]"):
            other_row, other_col = map(int, self.operations_list[current_move_number-1][1][1:-1].split(","))
        else:
            other_row, other_col = -1, -1
        
        # UI cue
        table.start_flashing()
        table.flash_cells((my_row, my_col), (other_row, other_col))

        # Update the table object
        table.set_data(manifest_data_of_solution_path[current_move_number-1])
       
        # place current move frame in parent frame
        move_info_frame = ttk.Frame(self.frame)
        move_info_frame.place(anchor="c", relx=0.25, rely=0.4)

        # place label in current move frame
        info_label = ttk.Label(move_info_frame, text=get_move_info(), font=("Arial", 16), anchor="center", justify="center")
        info_label.pack(fill="x", pady=10)
        
        style = ttk.Style()
        style.configure("Buttons.TButton", font=("Arial", 14), padding=(10, 10))

        # Recover from save file until current_move reaches to saved move
        if self.current_move_number < int(read_save_file("move_number") or 0):
            self.create_current_move_frame(current_move_number+1, table, manifest_data_of_solution_path)
        
        if self.current_move_number < self.total_moves:
            next_button = ttk.Button(move_info_frame, text="Next", style="Buttons.TButton", command=lambda: [self.create_current_move_frame(current_move_number+1, table, manifest_data_of_solution_path), save(current_move_number)])
        else:
            next_button = ttk.Button(move_info_frame, text="Done", style="Buttons.TButton", command=lambda: [self.finish_move(self.root, self.frame, table), clear_save_file()])
        
        next_button.pack(pady=10)
        
        def save(current_move_number):
            write_save_file("move_number", current_move_number+1)