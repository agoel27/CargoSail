import tkinter as tk
from tkinter import ttk
#from app.load_balance_screen import *
#from app.add_note import add_note
from tkinter import messagebox
import app.load_balance_screen as load_balance_screen
from config import *

class CurrentMoveFrame:
    def __init__(self, frame, current_move_number, total_moves):
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
        self.frame = frame
        self.current_move_number = current_move_number
        self.total_moves = total_moves
        # self.total_minutes = total_minutes
        # self.current_move_from = current_move_from
        # self.current_move_to = current_move_to
        # self.estimated_time_for_move = estimated_time_for_move

    def finish_move(self, master_frame, frame):
        if self.current_move_number == self.total_moves:
            messagebox.showinfo("Reminder", "Reminder to email the manifest!")
        load_balance_screen.load_balance(master_frame, frame)

    def create_current_move_frame(self):
        """
        create frame with the text displaying the move information
        """
        # place current move frame in parent frame
        move_info_frame = ttk.Frame(self.frame)
        move_info_frame.place(anchor="c", relx=0.25, rely=0.4)

        # place label in current move frame
        info_label = ttk.Label(move_info_frame, text=get_move_info(), font=("Arial", 16), anchor="center", justify="center")
        info_label.pack(fill="x", pady=10)
        
        style = ttk.Style()
        style.configure("Buttons.TButton", font=("Arial", 14), padding=(10, 10))

        if self.current_move_number < self.total_moves:
            next_button = ttk.Button(move_info_frame, text="Next", style="Buttons.TButton", command=lambda: self.create_current_move_frame())
        else:
            next_button = ttk.Button(move_info_frame, text="Done", style="Buttons.TButton", command=lambda: [self.finish_move(self.frame.master, self.frame), delete_save_file()])
        
        next_button.pack(pady=10)