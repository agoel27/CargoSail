import tkinter as tk
from tkinter import ttk

class Table:
    def __init__(self, frame, data):
        """
        initialize table class

        frame: frame where table will be placed
        data:  2D list containing table data
        """
        self.frame = frame
        self.rows = len(data)
        self.columns = len(data[0])
        self.data = data
        
        self.create_table()

    def create_table(self):
        """
        create table UI
        """
        # clear existing table
        for widget in self.frame.winfo_children():
            widget.destroy()

        # create labels for each cell
        for i in range(self.rows):
            for j in range(self.columns):
                # Truncate the text to the first 7 characters
                truncated_value = self.data[i][j][:7]

                cell = tk.Label(self.frame, text=truncated_value, borderwidth=1, relief="solid", width=7, height=2, font=("Arial", 12), anchor="center")
                cell.grid(row=i, column=j, sticky="nsew")

        # make uniform rows and columns
        for i in range(self.rows):
            self.frame.grid_rowconfigure(i, weight=1)
        for j in range(self.columns):
            self.frame.grid_columnconfigure(j, weight=1)

    def set_data(self, new_data):
        """
        set new data for table. this replaces current data (might not be necessary)

        new_data: 2D list containing new table data
        """
        if len(new_data) == self.rows and len(new_data[0]) == self.columns:
            self.data = new_data
            self.create_table()  # Update the table UI
        else:
            print("Error: The data dimensions do not match the table size.")

    def change_cell(self, row, col, value):
        """
        change the value of a specific cell in the table

        row: row index
        col: column index
        value: new value for cell
        """
        if 0 <= row < self.rows and 0 <= col < self.columns:
            self.data[row][col] = value
            self.create_table()  # Update the table UI
        else:
            print("Error: Invalid cell coordinates.")