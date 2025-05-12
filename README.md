# ADEE_1317_Form_Filler
Desktop app which help filling and managing ADEE_1317 form

icon download from https://www.flaticon.com/free-icons/corgi | Corgi icons created by Iconriver - Flaticon
theme from  https://github.com/rdbende/Azure-ttk-theme

# ADEE 1317 Form Auto Generator

This is a desktop application that helps educators fill and generate ADEE-1317 Texas Adult Driver Education Certificate PDFs. It includes a searchable submission history, automatic control number tracking, validation, and PDF export.

## Features

- Fill out student information in a user-friendly GUI.
- Automatically generate and save PDF certificates.
- Prevents duplicate control numbers with warnings.
- Automatically tracks submission timestamps in Central Time (CT).
- Search and filter submission history by name and date.
- Export selected or all records to a summary PDF.
- Tabbed interface for today's submissions and full history.
- Data stored in a local SQLite database (`submissions.db`).

## File Structure  
.
├── Front_end.py                # Main GUI launcher
├── back_end.py                 # PDF generation, utility functions
├── database.py                 # SQLite DB setup and logic
├── Template/
│   └── ADEE-1317-texas-adult-driver-education-certificate-template.pdf
├── theme/
│   ├── azure.tcl
│   ├── midnight.json
│   └── light/                 # Optional image assets or additional styles
├── counter.txt                # Tracks current control number
└── output/                    # Stores generated PDFs (organized by date)

## Usage  
- Unzip the release zip into your folder choice which include Template folder and exe file  
- Run the exe  