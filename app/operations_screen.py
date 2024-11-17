import tkinter as tk
from tkinter import *
from app.popup_login import login_popup
from app.add_note import add_note
from app.table import Table
from app.current_move_frame import CurrentMoveFrame

def operations_screen(root, prevFrame, current_username):

    buffer_data = [
        ["Lion", "", "Elephant", "", "Zebra", "", "", "", "Dolphin", "", "Shark", "", "", "Koala", "", "", "Fox", "Rabbit", "Deer", "Eagle","Hawk", "Owl", "", ""],
        ["", "Dog", "", "", "", "", "", "Bison", "Bison", "Monkey", "Chimpanzee", "", "", "", "", "", "", "Bat", "Squirrel", "Beaver", "Badger", "", "Meerkat", ""],
        ["", "Panda", "Giraffe", "", "", "Cheetah", "Tiger", "", "Wolf", "", "", "", "Penguin", "Kangaroo", "", "Whale", "", "Leopard", "Gorilla", "", "", "", "Parrot", "Crow"],
        ["", "Cat", "", "Horse", "Cow", "Goat", "", "", "Bison", "", "Chimpanzee", "Sloth", "", "Bat", "", "Otter", "", "Ocelot", "", "Zebra", "", "Bear", "", "Fox"]
    ]

    ship_data = [
        ["", "", "", "", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", "", "", "Bag", ""],
        ["", "", "", "", "", "", "", "", "", "Mouse", "Desk", ""],
        ["", "", "", "", "", "", "", "", "Shoes", "Bag", "Wallet", "Printer"],
        ["", "", "", "", "", "", "", "Headphones", "Bag", "Charger", "Speaker", "Printer"],
        ["", "", "", "", "", "", "Bag", "Desk", "Wallet", "Speakers", "Speaker", "Printer"],
        ["Speaker", "", "", "", "", "Headphones", "Monitor", "Bag", "Pen", "Notebook", "Lamp", "Tablet"],
        ["Chair", "", "", "", "Headphones", "Chair", "Desk", "Speaker", "Tablet", "Laptop", "Speaker", "Printer"]
    ]

    # destroys previous frame
    prevFrame.pack_forget()

    # create operations screen frame
    operations_screen_frame = tk.Frame(root)
    operations_screen_frame.pack(expand=1, fill="both")

    # # create login button frame
    # login_button_frame = tk.Frame(operations_screen_frame)
    # login_button_frame.place(relx=1, rely=0, anchor="ne")

    # # create add note frame
    # add_note_frame = tk.Frame(operations_screen_frame)
    # add_note_frame.place(relx=0, rely=0, anchor="nw")

    loginButton = Button(operations_screen_frame, text="Login", padx=10, pady=10, command= lambda:login_popup(root, current_username))
    loginButton.place(anchor="ne", relx=1, rely=0, x=-5, y=5)

    addNoteButton = Button(operations_screen_frame, text="Add Note", padx=10, pady=10, command=lambda:add_note(root))
    addNoteButton.place(anchor="nw", relx=0, rely=0, x=5, y=5)

    # create buffer area frame
    buffer_area_frame = tk.Frame(operations_screen_frame)
    buffer_area_frame.place(relx=0.5, rely=0.9, anchor="c")

    # create ship frame
    ship_frame = tk.Frame(operations_screen_frame)
    ship_frame.place(relx=0.75, rely=0.5, anchor="c")

    # create truck frame
    truck_frame = tk.Frame(operations_screen_frame)
    truck_frame.place(relx=0.25, rely=0.64, anchor="c")

    # # place login button in login button frame
    # loginButton = Button(login_button_frame, text="Login" , padx=10, pady=10, command= lambda:login_popup(root, current_username))
    # loginButton.pack(anchor="ne", padx=5, pady=5)

    # # place add note button in add note frame
    # addNoteButton = Button(add_note_frame, text="Add Note" , padx=10, pady=10, command= lambda:add_note(root))
    # addNoteButton.pack(anchor="nw", padx=5, pady=5)
    
    # place table in buffer area frame
    buffer_area_table = Table(buffer_area_frame, buffer_data)

    # place table in ship frame
    ship_table = Table(ship_frame, ship_data)

    # place truck in truck frame
    truck_label = tk.Label(truck_frame, text="Truck", borderwidth=1, relief="solid", width=7, height=2, font=("Arial", 12), anchor="center")
    truck_label.grid(row=0, column=0, sticky="nsew")

    # place current move frame in operations screen frame
    current_move_frame = CurrentMoveFrame(operations_screen_frame, 19, 48, 2, "truck", "[03,12]", 5, current_username)