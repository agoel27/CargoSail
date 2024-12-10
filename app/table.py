import tkinter as tk
from tkinter import ttk

class Table:
    def __init__(self, frame, data, truck_label):
        """
        initialize table class

        frame: frame where table will be placed
        data:  2D list containing table data
        """
        self.frame = frame
        self.rows = len(data)
        self.columns = len(data[0])
        self.data = data
        self.cell_widgets = {}
        self.is_flashing = False
        self.flash_cells_to_flash = None  # Store cells to flash
        self.truck_label = truck_label

        # label for hovering over cell
        self.hover_label = tk.Label(frame.master, bg="yellow", text="", font=("Arial", 12), relief="solid", borderwidth=1)
        
        self.create_table()

    def create_table(self):
        """
        create table UI
        """
        # clear existing table
        for widget in self.frame.winfo_children():
            if widget != self.hover_label:  # skip hover_label widget
                widget.destroy()

        self.cell_widgets = {}

        # create labels for each cell
        for i in range(self.rows):
            for j in range(self.columns):
                # truncate text to first 7 characters
                truncated_value = self.data[i][j][1][:7]

                if truncated_value == "UNUSED":
                    cell = tk.Label(self.frame, borderwidth=1, relief="solid", width=7, height=2)
                elif truncated_value == "NAN":
                    cell = tk.Label(self.frame, borderwidth=1, relief="solid", width=7, height=2, bg="gray")
                else:
                    cell = tk.Label(self.frame, text=truncated_value, borderwidth=1, relief="solid", width=7, height=2, font=("Arial", 12), anchor="center")
                cell.grid(row=i, column=j, sticky="nsew")

                # bind hover events to the cell
                cell.bind("<Enter>", lambda event, row=i, col=j: self.show_hover_label(event, row, col))
                cell.bind("<Leave>", self.hide_hover_label)

                self.cell_widgets[(i, j)] = cell

        self.cell_widgets[(-1, -1)] = self.truck_label

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
            self.create_table()  # update table UI
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
            self.create_table()  # update table UI
        else:
            print("Error: Invalid cell coordinates.")

    def show_hover_label(self, event, row, col):
        """
        show hover_label with text of hovered cell

        event:  tkinter event object
        row:    row index of hovered cell
        col:    column index of hovered cell
        """
        text = self.data[row][col][1]
        if text:  # only show hover_label if there's text
            self.hover_label.config(text=text)
            self.hover_label.place(relx=0.5, rely=0.1, anchor="c")

    def hide_hover_label(self, event):
        """
        hide hover_label when mouse leaves a cell.
        """
        if self.hover_label.winfo_exists():
            self.hover_label.place_forget()

    def flash_cells(self, cell1, cell2):
        """
        flash the background of two cells red indefinitely until stopped.

        cell1: tuple (row, column) of first cell
        cell2: tuple (row, column) of second cell
        """
        # Store the cells to flash
        self.flash_cells_to_flash = (cell1, cell2)
        self.is_flashing = True

        def toggle_flash():
            # Check if flashing is still active
            if not self.is_flashing:
                # Reset cells to default background when stopped
                for cell in self.flash_cells_to_flash:
                    widget = self.cell_widgets.get(cell)
                    if widget:
                        widget.config(bg="SystemButtonFace")
                return  # stop flashing

            for cell in self.flash_cells_to_flash:
                widget = self.cell_widgets.get(cell)
                if widget:
                    current_color = widget.cget("bg")
                    new_color = "red" if current_color != "red" else "SystemButtonFace"
                    widget.config(bg=new_color)

            # next flash
            self.frame.after(500, toggle_flash)

        toggle_flash()

    def stop_flashing(self):
        """
        Stop the flashing of cells
        """
        self.is_flashing = False

    def start_flashing(self):
        """
        Resume flashing of previously selected cells
        """
        if self.flash_cells_to_flash:
            self.is_flashing = True
            self.flash_cells(*self.flash_cells_to_flash)