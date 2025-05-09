import back_end 
import customtkinter
from tkinter import messagebox
from datetime import datetime

# Hold input fields
Filling = {}

# --- GUI Setup ---
root = customtkinter.CTk()
root.title("Document Filler")

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
        if not value.isdigit() or int(value) > 100 or int(value) < 0:
            errors.append(f"{label} must be a number between 0 and 100.")

    return errors

def on_submit():
    validation_errors = validate_inputs()
    if validation_errors:
        messagebox.showerror("Input Error", "\n".join(validation_errors))
    else:
        back_end.generate_doc(Filling)


# Helper function to create label+entry
def create_entry(label, row, field_key, default_text=""):
    customtkinter.CTkLabel(root, text=label).grid(row=row, column=0, padx=5, pady=5)
    entry = customtkinter.CTkEntry(root, width=200)
    entry.insert(0, default_text)
    entry.grid(row=row, column=1, padx=5, pady=5)
    Filling[field_key] = entry


# Create all input fields
create_entry("First Name:", 0, 'first_name_entry')
create_entry("Last Name:", 1, 'last_name_entry')
create_entry("Middle Name:", 2, 'middle_name_entry')
create_entry("Date of Birth:", 3, 'date_of_birth_entry')
create_entry("6h Classroom Course Completion Date:", 4, 'classroom_date_entry')
create_entry("6h Online Course Completion Date:", 5, 'online_date_entry')
create_entry("Road Rule Pts:", 6, 'road_rule_entry')
create_entry("Road Sign Pts:", 7, 'road_sign_entry')
create_entry("School Name:", 8, 'school_name_entry')
create_entry("TDLR Number:", 9, 'TDLR_entry')
create_entry("Driver Education School Number:", 10, 'driver_school_number_entry')
create_entry("Date Issued:", 11, 'date_issued_entry')

# Button
generate_button = customtkinter.CTkButton(root, text="Generate Document", command=on_submit)

generate_button.grid(row=12, column=0, columnspan=2, pady=15)

root.mainloop()
