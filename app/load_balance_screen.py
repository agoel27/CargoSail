from tkinter import Button, Frame

def load_balance(root):
    loginButton = Button(root, text="Login" , padx=10, pady=10)
    loginButton.pack(anchor="ne", padx=5, pady=5)

    # frame for load/unload and balance buttons to have them centered
    loadBalance_frame = Frame(root)
    loadBalance_frame.place(relx=0.5, rely=0.5, anchor="center")

    loadUnloadButton = Button(loadBalance_frame, text="Load/Unload", padx=10, pady=10)
    loadUnloadButton.grid(row=0, column=0, padx=5)

    balanceButton = Button(loadBalance_frame, text="Balance", padx=10, pady=10)
    balanceButton.grid(row=0, column=1, padx=5)