import tkinter as Tk

def selection(root, prev_frame):
    prev_frame.place_forget()

    selectionFrame = Tk.Frame(root)
    selectionFrame.pack(fill='both', expand=True)

    # scroll container on the right 
    container = Tk.Canvas(selectionFrame, bg="white", width=200, height=400)
    container.pack(side='right', fill='y', expand=False, padx=50, pady=50)

    scrollbar = Tk.Scrollbar(container, orient='vertical', command=container.yview)
    scrollbar.pack(side='right', fill='y')

    container.configure(yscrollcommand=scrollbar.set)

    contentFrame = Tk.Frame(container, bg='white')
    container.create_window((0,0), window=contentFrame, anchor='nw')
    contentFrame.update_idletasks()  # makes sure the content frame is drawn inside the container 
    container.config(scrollregion=container.bbox('all'))