from tkinter import ttk
import database
import tkinter as tk
from tkinter import messagebox
import back_end

def launch_history_viewer(history_frame):
    def perform_search():
        name = name_var.get().strip()
        month = month_var.get().strip()
        year = year_var.get().strip()
        filtered = database.search_submissions(name_query=name, month_query=month, year_query=year)

        # Clear current table
        for row in tree.get_children():
            tree.delete(row)

        for row in filtered:
            tree.insert("", "end", values=row)

    records = database.get_all_submissions()

    columns = (
        "ID", "Control Number", "First Name", "Last Name", "Middle Name", "DOB", "Classroom Date",
        "Online Date", "Road Rule", "Road Sign", "School", "TDLR", "Educator No",
        "Issued Date", "Generated At"
    )

    # Search Bar Frame
    search_frame = ttk.Frame(history_frame)
    search_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=(5, 0))

    name_var = tk.StringVar()
    month_var = tk.StringVar()
    year_var = tk.StringVar()

    ttk.Label(search_frame, text="Name:").grid(row=0, column=0, padx=5)
    name_entry = ttk.Entry(search_frame, textvariable=name_var, width=20)
    name_entry.grid(row=0, column=1, padx=5)

    ttk.Label(search_frame, text="Month (MM):").grid(row=0, column=2, padx=5)
    month_entry = ttk.Entry(search_frame, textvariable=month_var, width=10)
    month_entry.grid(row=0, column=3, padx=5)

    ttk.Label(search_frame, text="Year (YYYY):").grid(row=0, column=4, padx=5)
    year_entry = ttk.Entry(search_frame,textvariable=year_var, width=10)
    year_entry.grid(row=0, column=5, padx=5)

    search_button = ttk.Button(search_frame, text="Search", style="Accent.TButton", command=perform_search)
    search_button.grid(row=0, column=6, padx=10)

    # Treeview 
    tree = ttk.Treeview(history_frame, columns=columns, show='headings')

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=100)

    for row in records:
        tree.insert("", "end", values=row)

    scrollbar = ttk.Scrollbar(history_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)

    h_scroll = ttk.Scrollbar(history_frame, orient="horizontal", command=tree.xview)
    tree.configure(xscrollcommand=h_scroll.set)

    tree.grid(row=1, column=0, sticky="nsew", padx=(10, 0), pady=(5, 5))
    scrollbar.grid(row=1, column=1, sticky="ns", pady=10)
    h_scroll.grid(row=2, column=0, columnspan=2, sticky="ew", padx=10)

    history_frame.grid_rowconfigure(1, weight=1)
    history_frame.grid_columnconfigure(0, weight=1)

    def print_selected_pdf():
        selected = tree.focus()
        if not selected:
            messagebox.showwarning("No selection", "Please select a record first.")
            return

        selected_values = tree.item(selected, "values")
        form_id = selected_values[0]  # Assuming first column is ID

        try:
            # Call your backend PDF function
            back_end.generate_pdf_by_id(form_id)
            messagebox.showinfo("PDF Generated", f"PDF generated for ID {form_id}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not generate PDF: {e}")
    
    print_btn = ttk.Button(history_frame, text="Print PDF for Selected", command=print_selected_pdf)
    print_btn.grid(row=3, column=0, columnspan=2, sticky="ew", padx=10, pady=(5, 10))
