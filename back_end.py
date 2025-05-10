from tkinter import filedialog, messagebox
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from pypdf import PdfReader, PdfWriter
from io import BytesIO
import os
import sqlite3
from datetime import datetime
import webbrowser
def digit_control(counter):
    return str(counter).zfill(8)

def load_current_number(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            return int(f.read().strip())
    return 1

def save_next_number(file_path, number):
    with open(file_path, 'w') as f:
        f.write(str(number))

# add spaces to date
def spaced_date(date_str):
    try:
        parts = date_str.split("/")
        if len(parts) == 3:
            return f"{parts[0]}    {parts[1]}  {parts[2]}"
    except Exception:
        pass
    return date_str

def get_val(filling, key):
    value = filling.get(key)
    return value.get() if hasattr(value, 'get') else value

def create_overlay(data):
    packet = BytesIO()
    c = canvas.Canvas(packet, pagesize=letter)

    # Draw text onto the PDF at specific (x, y) positions
    c.drawString(205, 546, f"{data['first_name']}")
    c.drawString(52, 546, f"{data['last_name']}")
    c.drawString(349, 546, f"{data['middle_name']}")
    c.drawString(429, 546, f"{spaced_date(data['date_of_birth'])}")
    c.drawString(210, 665, f"{spaced_date(data['classroom_date_entry'])}")
    c.drawString(493, 665, f"{spaced_date(data['online_date_entry'])}")
    c.drawString(380, 624, f"{data['road_rule']}")
    c.drawString(480, 624, f"{data['road_sign']}")
    c.drawString(430, 484, f"{data['school_name']}")
    c.drawString(280, 484, f"{data['tdlr']}")
    c.drawString(255, 458, f"{data['educator']}")
    c.drawString(450, 458, f"{data['date']}")
    c.drawString(500, 742, f"{data['control_number']}")

    c.save()
    packet.seek(0)
    return PdfReader(packet)

def merge_overlay(template_pdf_path, output_pdf_path, overlay_data):
    base_pdf = PdfReader(template_pdf_path)
    overlay_pdf = create_overlay(overlay_data)
    writer = PdfWriter()

    for i, page in enumerate(base_pdf.pages):
        base_page = page
        base_page.merge_page(overlay_pdf.pages[0])  # merge overlay onto first page
        writer.add_page(base_page)

    with open(output_pdf_path, "wb") as f:
        writer.write(f)

def get_output_path(filling):
    # Generate timestamp-based folder
    now = datetime.now()
    month_folder = now.strftime("%Y-%m")  # e.g. 2025-05
    day_folder = now.strftime("%d")       # e.g. 08

    # Create folder path
    output_dir = os.path.join("output", month_folder, day_folder)
    os.makedirs(output_dir, exist_ok=True)

    # Build filename from extracted values
    first = get_val(filling, "first_name_entry")
    last = get_val(filling, "last_name_entry")
    control = get_val(filling, "control_number")

    filename = f"{first}_{last}_{control}".strip().replace(" ", "_") or "output"
    output_path = os.path.join(output_dir, f"{filename}.pdf")
    return output_path

def generate_doc(filling, form_id=None):
    counter_file = 'counter.txt'
    current_number = load_current_number(counter_file)
    template_path = "Template/ADEE-1317-texas-adult-driver-education-certificate-template.pdf"
    output_path = get_output_path(filling)
    if not output_path:
        return

    overlay_data = {
        "first_name": get_val(filling, 'first_name_entry'),
        "last_name": get_val(filling, 'last_name_entry'),
        "middle_name": get_val(filling, 'middle_name_entry'),
        "date_of_birth": get_val(filling, 'date_of_birth_entry'),
        "road_rule": get_val(filling, 'road_rule_entry'),
        "road_sign": get_val(filling, 'road_sign_entry'),
        "classroom_date_entry": get_val(filling, 'classroom_date_entry'),
        "online_date_entry": get_val(filling, 'online_date_entry'),
        "school_name": get_val(filling, 'school_name_entry'),
        "tdlr": get_val(filling, 'TDLR_entry'),
        "educator": get_val(filling, 'driver_school_number_entry'),
        "date": get_val(filling, 'date_issued_entry'),
        "control_number": get_val(filling, 'control_number'),
    }

    merge_overlay(template_path, output_path, overlay_data)

    if not form_id:
        save_next_number(counter_file, current_number + 1)

    messagebox.showinfo("Success", f"PDF generated and saved to:\n{output_path}")

def generate_pdf_by_id(form_id):
    conn = sqlite3.connect("submissions.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM submissions WHERE id=?", (form_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        raise ValueError("No record found for this ID")

    # Map row to dictionary
    fields = [
        "id","control_number", "first_name_entry", "last_name_entry", "middle_name_entry", "date_of_birth_entry",
        "classroom_date_entry", "online_date_entry", "road_rule_entry", "road_sign_entry", "school_name_entry",
        "TDLR_entry", "driver_school_number_entry", "date_issued_entry", "generated_at"
    ]
    data = dict(zip(fields, row))
    generate_doc(data, form_id=form_id)