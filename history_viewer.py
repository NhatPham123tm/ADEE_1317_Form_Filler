from tkinter import ttk
import database
import tkinter as tk
from tkinter import messagebox
import back_end
from datetime import datetime
def treeview_sort_column(tv, col, reverse):
    data_list = [(tv.set(k, col), k) for k in tv.get_children('')]

    # Try to convert to int or date for proper sorting
    def try_convert(val):
        try:
            return int(val)
        except ValueError:
            try:
                return datetime.strptime(val, "%m/%d/%Y")
            except:
                return val.lower()

    data_list.sort(key=lambda t: try_convert(t[0]), reverse=reverse)

    for index, (val, k) in enumerate(data_list):
        tv.move(k, '', index)

    # Reverse sort next time
    tv.heading(col, command=lambda: treeview_sort_column(tv, col, not reverse))
    
def launch_history_viewer(history_frame):
    records = database.get_all_submissions()
    today_records = database.get_today_submissions()

    columns = (
        "ID", "Control Number", "First Name", "Last Name", "Middle Name", "DOB", "Classroom Date",
        "Online Date", "Road Rule", "Road Sign", "School", "TDLR", "Educator No",
        "Issued Date", "Generated At"
    )

    # Create Notebook
    notebook = ttk.Notebook(history_frame)
    notebook.grid(row=0, column=0, sticky="nsew")

    # --- Tab 1: Today's Submissions ---
    tab_today = ttk.Frame(notebook)
    notebook.add(tab_today, text="Today's Submissions")

    today_tree = ttk.Treeview(tab_today, columns=columns, show='headings')
    for col in columns:
        today_tree.heading(col, text=col, command=lambda _col=col: treeview_sort_column(today_tree, _col, False))
        today_tree.column(col, anchor="center", width=100)
    for row in today_records:
        today_tree.insert("", "end", values=row)
    today_tree.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    today_scroll_y = ttk.Scrollbar(tab_today, orient="vertical", command=today_tree.yview)
    today_tree.configure(yscrollcommand=today_scroll_y.set)
    today_scroll_y.grid(row=0, column=1, sticky="ns", pady=10)

    tab_today.grid_rowconfigure(0, weight=1)
    tab_today.grid_columnconfigure(0, weight=1)

    # --- Tab 2: All Submissions with Search ---
    tab_all = ttk.Frame(notebook)
    notebook.add(tab_all, text="All Submissions")

    name_var = tk.StringVar()
    month_var = tk.StringVar()
    year_var = tk.StringVar()

    search_frame = ttk.Frame(tab_all)
    search_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=(5, 0))

    ttk.Label(search_frame, text="Name:").grid(row=0, column=0, padx=5)
    ttk.Entry(search_frame, textvariable=name_var, width=20).grid(row=0, column=1, padx=5)
    ttk.Label(search_frame, text="Month (MM):").grid(row=0, column=2, padx=5)
    ttk.Entry(search_frame, textvariable=month_var, width=10).grid(row=0, column=3, padx=5)
    ttk.Label(search_frame, text="Year (YYYY):").grid(row=0, column=4, padx=5)
    ttk.Entry(search_frame, textvariable=year_var, width=10).grid(row=0, column=5, padx=5)

    def perform_search():
        name = name_var.get().strip()
        month = month_var.get().strip()
        year = year_var.get().strip()
        filtered = database.search_submissions(name_query=name, month_query=month, year_query=year)
        for row in tree.get_children():
            tree.delete(row)
        for row in filtered:
            tree.insert("", "end", values=row)

    ttk.Button(search_frame, text="Search", style="Accent.TButton", command=perform_search).grid(row=0, column=6, padx=10)

    tree = ttk.Treeview(tab_all, columns=columns, show='headings')
    for col in columns:
        tree.heading(col, text=col, command=lambda _col=col: treeview_sort_column(tree, _col, False))
        tree.column(col, anchor="center", width=100)
    for row in records:
        tree.insert("", "end", values=row)
    tree.grid(row=1, column=0, sticky="nsew", padx=(10, 0), pady=(5, 5))

    scroll_y = ttk.Scrollbar(tab_all, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scroll_y.set)
    scroll_y.grid(row=1, column=1, sticky="ns", pady=10)

    def print_selected_from_active_tab():
        active_tab = notebook.index(notebook.select())

        selected_tree = today_tree if active_tab == 0 else tree
        selected = selected_tree.focus()

        if not selected:
            messagebox.showwarning("No selection", "Please select a record first.")
            return

        form_id = selected_tree.item(selected, "values")[0]
        try:
            back_end.generate_pdf_by_id(form_id)
            messagebox.showinfo("PDF Generated", f"PDF generated for ID {form_id}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # Global print button (below the tabs)
    print_global_btn = ttk.Button(history_frame, text="Print Selected Record", command=print_selected_from_active_tab)
    print_global_btn.grid(row=1, column=0, sticky="ew", padx=10, pady=(5, 10))

    def update_button_style(event=None):
        active_tab = notebook.index(notebook.select())
        selected_tree = today_tree if active_tab == 0 else tree
        print_global_btn.configure(style="Accent.TButton" if selected_tree.selection() else "")

    tree.bind("<<TreeviewSelect>>", update_button_style)
    today_tree.bind("<<TreeviewSelect>>", update_button_style)
    notebook.bind("<<NotebookTabChanged>>", update_button_style)

    def print_all_records_to_pdf():
        active_tab = notebook.index(notebook.select())
        selected_tree = today_tree if active_tab == 0 else tree

        all_data = [selected_tree.item(row)["values"] for row in selected_tree.get_children()]
        if not all_data:
            messagebox.showwarning("No Data", "No rows to print.")
            return

        try:
            file_path = back_end.export_records_to_pdf(all_data)
            messagebox.showinfo("PDF Created", f"All records exported to:\n{file_path}")
            import webbrowser
            webbrowser.open(file_path)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate record PDF:\n{e}")

    print_combined_btn = ttk.Button(history_frame, text="Export Tab Records to PDF", style="Accent.TButton", command=print_all_records_to_pdf)
    print_combined_btn.grid(row=3, column=0, sticky="ew", padx=10, pady=(0, 10))

    # Configure grid weights
    for i in [0, 1, 2]:
        tab_all.grid_rowconfigure(i, weight=1)
    tab_all.grid_columnconfigure(0, weight=1)

    history_frame.grid_rowconfigure(0, weight=1)
    history_frame.grid_columnconfigure(0, weight=1)

