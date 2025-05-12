import back_end
import database
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# Hold input fields
Filling = {}


def validate_inputs():
    errors = []

    control_number = Filling['control_number'].get().strip()

    if database.is_control_number_exists(control_number):
        latest = database.get_latest_number()
        next_available = "DEE " + back_end.digit_control(latest + 1)
        proceed = messagebox.askyesno(
            "Duplicate Control Number",
            f"The control number '{control_number}' already exists.\n"
            f"Suggested next available: {next_available}\n\n"
            "Do you want to continue anyway?"
        )
        if not proceed:
            return ["Submission cancelled due to duplicate control number."]
        
    # Validate dates
    date_fields = {
        "Date of Birth": 'date_of_birth_entry',
        "Date Issued": 'date_issued_entry'
    }
    for label, key in date_fields.items():
        value = Filling[key].get().strip()
        try:
            datetime.strptime(value, "%m/%d/%Y")
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
        return

    conn = database.get_connection()
    try:
        # Transaction
        cursor = conn.cursor()

        # Prepare data
        data = {
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
            "male": int(Filling["Male"].get()),
            "female": int(Filling["Female"].get()),
            "driver_ed": int(Filling['driver_ed'].get()),
            "private_school": int(Filling['private_school'].get()),
            "duplicate": int(Filling['duplicate'].get()),
            "public_school": int(Filling['public_school'].get()),
            "service_center": int(Filling['service_center'].get()),
            "college": int(Filling['college'].get()),
            "at_dps": int(Filling['At_DPS'].get()),
            "vision_exam": int(Filling['Vision_examination'].get())
        }

        # Save submission but do not commit yet
        database.save_submission(data, conn=conn, cursor=cursor)

        # Generate PDF
        back_end.generate_doc(Filling)

        # Commit if everything is successful
        conn.commit()
        back_end.save_next_number('counter.txt', int(Filling['control_number'].get().split()[1]) + 1)

        messagebox.showinfo("Success", "Document generated and saved successfully!")

        # Reset form fields
        for widget in Filling.values():
            if hasattr(widget, 'delete'):
                widget.delete(0, tk.END)
        new_number = "DEE " + back_end.digit_control(back_end.load_current_number("counter.txt"))
        Filling['control_number'].delete(0, tk.END)
        Filling['control_number'].insert(0, new_number)

    except Exception as e:
        conn.rollback()
        messagebox.showerror("Error", f"An error occurred: {str(e)}")
    finally:
        conn.close()

# function to create label+entry
def create_entry(label, row, field_key, default_text="", parent_frame=None):
    ttk.Label(parent_frame, text=label, font=("-size", 12)).grid(row=row, column=0, sticky="e", padx=5, pady=5)
    entry = ttk.Entry(parent_frame, width=30)
    entry.insert(0, default_text)
    entry.grid(row=row, column=1, sticky="ew", padx=5, pady=(5,10))
    Filling[field_key] = entry

# Frame: Form Input
def launch_form_input(form_input_frame):
    # Canvas and scrollbar setup
    canvas = tk.Canvas(form_input_frame)
    scrollbar = ttk.Scrollbar(form_input_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    # Create the window inside the canvas and keep a reference
    canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="n")

    def center_scrollable_frame(event):
        canvas_width = event.width
        frame_width = scrollable_frame.winfo_reqwidth()
        x = max((canvas_width - frame_width) // 2, 0)
        canvas.coords(canvas_window, x, 0)  # Update x position to center

    canvas.bind("<Configure>", center_scrollable_frame)

    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.grid(row=0, column=0, sticky="nsew")
    scrollbar.grid(row=0, column=1, sticky="ns")

    form_input_frame.grid_rowconfigure(0, weight=1)
    form_input_frame.grid_columnconfigure(0, weight=1)

    # Form content inside scrollable frame
    widgets_frame = ttk.Frame(scrollable_frame, padding=10)
    widgets_frame.grid(row=0, column=0, sticky="nsew")
    widgets_frame.columnconfigure(1, weight=1)

    # Control number
    counter_file = 'counter.txt'
    current_number = back_end.load_current_number(counter_file)
    control_number = "DEE " + back_end.digit_control(current_number)

    ttk.Label(widgets_frame, text="Control Number:", font=("-size", 12)).grid(row=13, column=0, padx=5, pady=(0, 10), sticky="e")
    control_entry = ttk.Entry(widgets_frame, width=30)
    control_entry.insert(0, control_number)
    control_entry.grid(row=13, column=1, padx=5, pady=(0, 10), sticky="ew")
    Filling["control_number"] = control_entry

    # Form entries
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

    # Checkboxes
    checkbox_options = {
        "driver_ed": tk.BooleanVar(),
        "private_school": tk.BooleanVar(),
        "duplicate": tk.BooleanVar(),
        "public_school": tk.BooleanVar(),
        "service_center": tk.BooleanVar(),
        "college": tk.BooleanVar(),
        "At_DPS": tk.BooleanVar(),
        "Vision_examination": tk.BooleanVar(),
        "Male": tk.BooleanVar(),
        "Female": tk.BooleanVar(),
    }

    checkbox_labels = [
        ("Driver Education Provider", "driver_ed"),
        ("Private School", "private_school"),
        ("Duplicate", "duplicate"),
        ("Public School", "public_school"),
        ("Education Service Center", "service_center"),
        ("College/University", "college"),
    ]

    for i, (label, key) in enumerate(checkbox_labels):
        r = 14 + i // 3
        c = i % 3
        ttk.Checkbutton(
            widgets_frame,
            text=label,
            variable=checkbox_options[key]
        ).grid(row=r, column=c, sticky="w", padx=10, pady=5)

    # Long checkboxes
    ttk.Checkbutton(
        widgets_frame,
        text="Must take Class C-Road Rules and Class C-Road Signs examinations at the Department of Public Safety",
        variable=checkbox_options["At_DPS"],
    ).grid(row=20, column=0, columnspan=3, sticky="w", padx=10, pady=(10, 5))

    ttk.Checkbutton(
        widgets_frame,
        text="Must take vision examination at the Department of Public Safety.",
        variable=checkbox_options["Vision_examination"],
    ).grid(row=21, column=0, columnspan=3, sticky="w", padx=10, pady=(0, 10))

    ttk.Checkbutton(
        widgets_frame,
        text="Male",
        variable=checkbox_options["Male"],
    ).grid(row=0, column=2, columnspan=3, sticky="w", padx=10, pady=(10, 5))

    ttk.Checkbutton(
        widgets_frame,
        text="Female",
        variable=checkbox_options["Female"],
    ).grid(row=1, column=2, columnspan=3, sticky="w", padx=10, pady=(10, 5))

    Filling.update(checkbox_options)

    # Submit button
    generate_button = ttk.Button(scrollable_frame, text="Generate Document", style="Accent.TButton", command=lambda: on_submit())
    generate_button.grid(row=99, column=0, columnspan=2, pady=10, sticky="ew")

    # Enable mousewheel scrolling
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    canvas.bind_all("<MouseWheel>", _on_mousewheel)
