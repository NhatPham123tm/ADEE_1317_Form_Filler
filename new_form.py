import back_end
import database
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# Hold input fields
Filling = {}

def validate_inputs():
    errors = []

    # Validate dates
    date_fields = {
        "Date of Birth": 'date_of_birth_entry',
        "Date Issued": 'date_issued_entry'
    }

    for label, key in date_fields.items():
        value = Filling[key].get().strip()
        try:
            datetime.strptime(value, "%m/%d/%Y")  # Use desired format
        except ValueError:
            errors.append(f"{label} must be in MM/DD/YYYY format.")

    # Validate numeric fields
    numeric_fields = {
        "Road Rule Pts": 'road_rule_entry',
        "Road Sign Pts": 'road_sign_entry'
    }

    for label, key in numeric_fields.items():
        value = Filling[key].get().strip()
        if not value.isdigit() or not (0 <= int(value) <= 100):
            errors.append(f"{label} must be a number between 0 and 100.")

    return errors

def on_submit():
    validation_errors = validate_inputs()
    if validation_errors:
        messagebox.showerror("Input Error", "\n".join(validation_errors))
    else:
        # Save to DB
        database.save_submission({
            "control_number": Filling['control_number'].get(),
            "first_name": Filling['first_name_entry'].get(),
            "last_name": Filling['last_name_entry'].get(),
            "middle_name": Filling['middle_name_entry'].get(),
            "date_of_birth": Filling['date_of_birth_entry'].get(),
            "classroom_date": Filling['classroom_date_entry'].get(),
            "online_date": Filling['online_date_entry'].get(),
            "road_rule": Filling['road_rule_entry'].get(),
            "road_sign": Filling['road_sign_entry'].get(),
            "school_name": Filling['school_name_entry'].get(),
            "tdlr": Filling['TDLR_entry'].get(),
            "educator_number": Filling['driver_school_number_entry'].get(),
            "date_issued": Filling['date_issued_entry'].get(),
        })

        back_end.generate_doc(Filling)

# function to create label+entry
def create_entry(label, row, field_key, default_text="", parent_frame=None):
    ttk.Label(parent_frame, text=label).grid(row=row, column=0, sticky="e", padx=5, pady=5)
    entry = ttk.Entry(parent_frame, width=30)
    entry.insert(0, default_text)
    entry.grid(row=row, column=1, sticky="ew", padx=5, pady=(5,10))
    Filling[field_key] = entry

# Frame: Form Input
def launch_form_input(form_input_frame):
    for i in range(0, 13):
        form_input_frame.grid_rowconfigure(i, weight=1)
    form_input_frame.grid_columnconfigure(0, weight=1)
    form_input_frame.grid_columnconfigure(1, weight=2)

    widgets_frame = ttk.Frame(form_input_frame, padding=10)
    widgets_frame.grid(row=0, column=0, sticky="nsew")
    widgets_frame.columnconfigure(1, weight=1)

    # Control number label and entry
    counter_file = 'counter.txt'
    current_number = back_end.load_current_number(counter_file)
    control_number = "DEE " + back_end.digit_control(current_number)

    ttk.Label(widgets_frame, text="Control Number:").grid(row=13, column=0, padx=5, pady=(0, 10), sticky="e")
    control_entry = ttk.Entry(widgets_frame, width=30)
    control_entry.insert(0, control_number)
    control_entry.grid(row=13, column=1, padx=5, pady=(0, 10), sticky="ew")

    Filling["control_number"] = control_entry  # Save for later use in on_submit

    # Create entries inside widgets_frame
    for i, (label, field) in enumerate([
        ("First Name:", 'first_name_entry'),
        ("Last Name:", 'last_name_entry'),
        ("Middle Name:", 'middle_name_entry'),
        ("Date of Birth:", 'date_of_birth_entry'),
        ("6h Classroom Course Completion Date:", 'classroom_date_entry'),
        ("6h Online Course Completion Date:", 'online_date_entry'),
        ("Road Rule Pts:", 'road_rule_entry'),
        ("Road Sign Pts:", 'road_sign_entry'),
        ("School Name:", 'school_name_entry'),
        ("TDLR Number:", 'TDLR_entry'),
        ("Driver Education School Number:", 'driver_school_number_entry'),
        ("Date Issued:", 'date_issued_entry'),
    ]):
        create_entry(label, i, field, parent_frame=widgets_frame)

    generate_button = ttk.Button(form_input_frame, text="Generate Document", command=on_submit)
    generate_button.grid(row=12, column=0, columnspan=2, pady=10, sticky="n")
