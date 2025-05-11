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
root.tk.call("set_theme", "light")
root.title("Document Filler")
root.geometry("850x980")
root.minsize(400, 400)
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# --- Landing Frame ---
landing_frame = ttk.Frame(root, padding=10)
landing_frame.grid(row=0, column=0, padx=20, pady=20)
landing_frame.grid_columnconfigure(0, weight=1)
landing_frame.grid_rowconfigure(0, weight=1)
landing_frame.grid_rowconfigure(1, weight=1)

# Top Info Frame (Date + Monthly Count)
top_info_frame = ttk.Frame(landing_frame)
top_info_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
top_info_frame.grid_columnconfigure(0, weight=1)

# Current Date
today = datetime.now()
formatted_date = today.strftime("%m/%d/%Y")
ttk.Label(top_info_frame, text="Today's Date:",  font=("-size", 13)).grid(row=0, column=0, padx=5, pady=(0, 5), sticky="e")
ttk.Label(
    top_info_frame,
    text=formatted_date,
    font=("-size", 13, "-weight", "bold"),
    anchor="center"
).grid(row=0, column=1, padx=10, pady=(0, 5), sticky="w")

# Monthly Count
monthly_total = database.get_current_month_submission_count()
ttk.Label(top_info_frame, text="Forms Submitted This Month:",  font=("-size", 13)).grid(row=0, column=3, padx=5, pady=5, sticky="e")
ttk.Label(
    top_info_frame,
    text=monthly_total,
    font=("-size", 13, "-weight", "bold"),
    anchor="center"
).grid(row=0, column=4, padx=5, pady=5, sticky="w")

# vertical separator
vertical_separator = ttk.Separator(top_info_frame, orient="vertical")
vertical_separator.grid(row=0, column=2,rowspan=1, padx=(0, 10), pady=5, sticky="ns")
# Horizontal Separator
separator = ttk.Separator(top_info_frame, orient="horizontal")
separator.grid(row=1, column=0,columnspan=4, padx=(20, 10), pady=10, sticky="ew")

# Option Buttons Frame
button_frame = ttk.Frame(landing_frame)
button_frame.grid(row=1, column=0, sticky="n")

ttk.Label(button_frame, text="Choose One Option Below",  font=("-size", 13)).grid(
    row=0, column=0, columnspan=2, pady=(0, 10)
)

ttk.Button(button_frame, text="Start New Form", style="Accent.TButton", width=20,
           command=lambda: frame_transit('new', root)).grid(row=1, column=0, columnspan=2, pady=5)

ttk.Button(button_frame, text="View History", width=20,
           command=lambda: frame_transit('history', root)).grid(row=2, column=0, columnspan=2, pady=5)
root.mainloop()
