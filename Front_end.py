import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import back_end, database, history_viewer, new_form


def frame_transit(option, root):
    landing_frame.grid_forget()

    chosen_frame = ttk.Frame(root)
    chosen_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
    chosen_frame.grid_rowconfigure(0, weight=1)
    chosen_frame.grid_columnconfigure(0, weight=1)

    if option == 'new':
        new_form.launch_form_input(chosen_frame)
    else:
        history_viewer.launch_history_viewer(chosen_frame)

    def go_back():
        chosen_frame.grid_forget()
        landing_frame.grid(row=0, column=0, padx=20, pady=20)

    go_back_button = ttk.Button(chosen_frame, text="Go Back", command=go_back)
    go_back_button.grid(row=13, column=0, columnspan=2, pady=5)


# --- Initialize DB ---
database.init_db()

# --- Setup Main Window ---
root = tk.Tk()
root.tk.call("source", "theme/azure.tcl")
root.tk.call("set_theme", "dark")
root.title("Document Filler")
root.geometry("800x800")
root.minsize(400, 400)
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# --- Landing Frame ---
landing_frame = ttk.Frame(root, padding=10)
landing_frame.grid(row=0, column=0, padx=20, pady=20)

for i in range(3):
    landing_frame.grid_rowconfigure(i, weight=1)
landing_frame.grid_columnconfigure(0, weight=1)

ttk.Label(landing_frame, text="Choose One Option Below").grid(
    row=0, column=0, columnspan=2, pady=10, sticky="n"
)

ttk.Button(landing_frame, text="Start New Form",style="Accent.TButton", width=20,
           command=lambda: frame_transit('new', root)).grid(row=1, column=0, columnspan=2, sticky="n", pady=5)

ttk.Button(landing_frame, text="View History", width=20,
           command=lambda: frame_transit('history', root)).grid(row=2, column=0, columnspan=2, sticky="n", pady=5)

root.mainloop()
