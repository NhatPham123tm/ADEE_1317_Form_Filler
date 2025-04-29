import tkinter as tk
from tkinter import filedialog, messagebox
import back_end  # your backend processing file

# Hold input fields
Filling = {}

# --- GUI Setup ---
root = tk.Tk()
root.title("Document Filler")

# Helper function to create label+entry
def create_entry(label_text, row, field_key):
    tk.Label(root, text=label_text).grid(row=row, column=0, sticky="e", padx=5, pady=5)
    entry = tk.Entry(root, width=40)
    entry.grid(row=row, column=1, padx=5, pady=5)
    Filling[field_key] = entry

# Create all input fields
create_entry("First Name:", 0, 'first_name_entry')
create_entry("Last Name:", 1, 'last_name_entry')
create_entry("Road Rule Pts:", 2, 'road_rule_entry')
create_entry("Road Sign Pts:", 3, 'road_sign_entry')
create_entry("School Name:", 4, 'school_name_entry')
create_entry("TDLR Number:", 5, 'TDLR_entry')
create_entry("Driver Education School Number:", 6, 'driver_school_number_entry')
create_entry("Date Issued:", 7, 'date_issued_entry')

# Button
generate_button = tk.Button(root, text="Generate Document", command=lambda: back_end.generate_doc(Filling))
generate_button.grid(row=8, column=0, columnspan=2, pady=15)

root.mainloop()
