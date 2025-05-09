from tkinter import filedialog, messagebox
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from pypdf import PdfReader, PdfWriter
from io import BytesIO
import os

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

def create_overlay(data):
    packet = BytesIO()
    c = canvas.Canvas(packet, pagesize=letter)

    # Draw text onto the PDF at specific (x, y) positions
    c.drawString(205, 546, f"{data['first_name']}")
    c.drawString(52, 546, f"{data['last_name']}")
    c.drawString(349, 546, f"{data['middle_name']}")
    c.drawString(431, 548, f"{spaced_date(data['date_of_birth'])}")
    c.drawString(210, 665, f"{spaced_date(data['classroom_date_entry'])}")
    c.drawString(490, 665, f"{spaced_date(data['online_date_entry'])}")
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

def generate_doc(filling):
    counter_file = 'counter.txt'
    current_number = load_current_number(counter_file)
    control_number = "DEE " + digit_control(current_number)

    template_path = filedialog.askopenfilename(title="Choose a base PDF template", filetypes=[("PDF files", "*.pdf")])
    if not template_path:
        return

    output_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
    if not output_path:
        return

    overlay_data = {
        "first_name": filling['first_name_entry'].get(),
        "last_name": filling['last_name_entry'].get(),
        "middle_name": filling['middle_name_entry'].get(),
        "date_of_birth": filling['date_of_birth_entry'].get(),
        "road_rule": filling['road_rule_entry'].get(),
        "road_sign": filling['road_sign_entry'].get(),
        "classroom_date_entry": filling['classroom_date_entry'].get(),
        "online_date_entry": filling['online_date_entry'].get(),
        "school_name": filling['school_name_entry'].get(),
        "tdlr": filling['TDLR_entry'].get(),
        "educator": filling['driver_school_number_entry'].get(),
        "date": filling['date_issued_entry'].get(),
        "control_number": control_number,
    }

    merge_overlay(template_path, output_path, overlay_data)

    save_next_number(counter_file, current_number + 1)

    messagebox.showinfo("Success", f"PDF generated and saved to:\n{output_path}")
