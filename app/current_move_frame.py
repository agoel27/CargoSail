import tkinter as tk
from tkinter import ttk
#from app.load_balance_screen import *
#from app.add_note import add_note
import app.load_balance_screen as load_balance_screen

class CurrentMoveFrame:
    def __init__(self, frame, total_moves, total_minutes, current_move_number, current_move_from, current_move_to, estimated_time_for_move, current_username):
        """
        initialize CurrentMoveFrame class
        
        frame:                      frame to place the current move frame in
        total_moves:                total number of moves
        total_minutes:              total estimated time for all moves (in minutes)
        current_move_number:        number of the current move being executed
        current_move_from:          the starting point of the current move
        current_move_to:            the endpoint of the current move
        estimated_time_for_move:    estimated time (in minutes) for the current move
        """
        self.frame = frame
        self.total_moves = total_moves
        self.total_minutes = total_minutes
        self.current_move_number = current_move_number
        self.current_move_from = current_move_from
        self.current_move_to = current_move_to
        self.estimated_time_for_move = estimated_time_for_move
        self.current_username = current_username
        
        self.create_current_move_frame()

    def create_current_move_frame(self):
        """
        create frame with the text displaying the move information
        """
        # place current move frame in parent frame
        move_info_frame = ttk.Frame(self.frame)
        move_info_frame.place(anchor="c", relx=0.25, rely=0.4)
        
        move_info_text = (
            f"It will take {self.total_moves} moves and {self.total_minutes} minutes.\n"
            f"Move {self.current_move_number}/{self.total_moves}: "
            f"Move from {self.current_move_from} to {self.current_move_to}, "
            f"estimated: {self.estimated_time_for_move} minutes."
        )

        # place label in current move frame
        info_label = tk.Label(move_info_frame, text=move_info_text, font=("Arial", 16), anchor="center", justify="center")
        info_label.pack(fill="x", pady=10)

        next_button = tk.Button(move_info_frame, text="Next", font=("Arial", 16), padx=10, pady=10, command=lambda: load_balance_screen.load_balance(self.frame.master, self.frame, self.current_username))
        next_button.pack(pady=10)