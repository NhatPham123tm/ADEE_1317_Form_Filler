import back_end 
import database
import customtkinter
from tkinter import messagebox
from datetime import datetime

# Hold input fields
Filling = {}

def frame_transit(option):
    landing_frame.grid_forget()
    if option == 'new':
        form_input_frame.grid(row=0, column=0, padx=20, pady=20)
    else:
        # Placeholder for history frame
        messagebox.showinfo("History", "History feature is not implemented yet.")

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
        # Save to DB
        database.save_submission({
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

        # Then generate the PDF
        back_end.generate_doc(Filling)


# function to create label+entry
def create_entry(label, row, field_key, default_text=""):
    customtkinter.CTkLabel(form_input_frame, text=label).grid(row=row, column=0, padx=5, pady=5, sticky="e")
    entry = customtkinter.CTkEntry(form_input_frame, width=200)
    entry.insert(0, default_text)
    entry.grid(row=row, column=1, padx=5, pady=5)
    Filling[field_key] = entry

# --- Database Initialization ---
database.init_db()

# --- CustomTkinter Setup ---
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("Theme/midnight.json") # Download from a13xe's GitHub repo CTkThemesPark

root = customtkinter.CTk()
root.title("Document Filler")
root.geometry("600x600")

# Frame: Form Selection
landing_frame = customtkinter.CTkFrame(root)
landing_frame.grid(row=0, column=0, padx=20, pady=20)
customtkinter.CTkLabel(landing_frame, text="Choose One Option Below").pack(pady=10)

customtkinter.CTkButton(landing_frame, text="Start New Form", command=lambda: frame_transit('new').pack(pady=5))
customtkinter.CTkButton(landing_frame, text="view History", command=lambda: frame_transit('history').pack(pady=5))

# Frame: Form Input
form_input_frame = customtkinter.CTkFrame(root)

# Create all input fields for ADEE form
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
generate_button = customtkinter.CTkButton(form_input_frame, text="Generate Document", command=on_submit)
generate_button.grid(row=12, column=0, columnspan=2, pady=15)

go_back_button = customtkinter.CTkButton(form_input_frame, text="Go Back", command=lambda: [form_input_frame.grid_forget(), landing_frame.grid()])
go_back_button.grid(row=13, column=0, columnspan=2, pady=5)

landing_frame.grid()

root.mainloop()
