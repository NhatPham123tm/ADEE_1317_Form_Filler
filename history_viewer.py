from tkinter import ttk

import database

def launch_history_viewer(history_frame):
    records = database.get_all_submissions()

    columns = (
        "ID", "First Name", "Last Name", "Middle Name", "DOB", "Classroom Date",
        "Online Date", "Road Rule", "Road Sign", "School", "TDLR", "Educator No",
        "Issued Date", "Generated At"
    )

    # Treeview
    tree = ttk.Treeview(history_frame, columns=columns, show='headings')

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=100)

    for row in records:
        tree.insert("", "end", values=row)

    # Scrollbar
    scrollbar = ttk.Scrollbar(history_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    h_scroll = ttk.Scrollbar(history_frame, orient="horizontal", command=tree.xview)
    tree.configure(xscrollcommand=h_scroll.set)
    h_scroll.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10)
    history_frame.grid_rowconfigure(1, weight=0)

    # Layout using grid
    tree.grid(row=0, column=0, sticky="nsew", padx=(10, 0), pady=10)
    scrollbar.grid(row=0, column=1, sticky="ns", pady=10)

    # Configure frame grid weights so the table expands properly
    history_frame.grid_rowconfigure(0, weight=1)
    history_frame.grid_columnconfigure(0, weight=1)
