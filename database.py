import sqlite3
from datetime import datetime
DB_NAME = "submissions.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            control_number TEXT,
            first_name TEXT,
            last_name TEXT,
            middle_name TEXT,
            date_of_birth TEXT,
            classroom_date TEXT,
            online_date TEXT,
            road_rule INTEGER,
            road_sign INTEGER,
            school_name TEXT,
            tdlr TEXT,
            educator_number TEXT,
            date_issued TEXT,
            generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def save_submission(data):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO submissions (
            control_number, first_name, last_name, middle_name, date_of_birth,
            classroom_date, online_date, road_rule, road_sign,
            school_name, tdlr, educator_number, date_issued
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data["control_number"],data["first_name"], data["last_name"], data["middle_name"], data["date_of_birth"],
        data["classroom_date"], data["online_date"], int(data["road_rule"]), int(data["road_sign"]),
        data["school_name"], data["tdlr"], data["educator_number"], data["date_issued"]
    ))
    conn.commit()
    conn.close()

def get_all_submissions():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM submissions
                    GROUP BY DATE(generated_at)
                    ORDER BY DATE(generated_at) DESC """)
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_current_month_submission_count():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Match current month in YYYY-MM format
    current_month = datetime.now().strftime("%Y-%m")
    cursor.execute("""
        SELECT COUNT(*) FROM submissions
        WHERE strftime('%Y-%m', generated_at) = ?
    """, (current_month,))
    count = cursor.fetchone()[0]
    conn.close()
    return count

def search_submissions(name_query="", month_query="", year_query=""):
    conn = sqlite3.connect("submissions.db")
    cursor = conn.cursor()

    query = "SELECT * FROM submissions WHERE 1=1"
    params = []

    if name_query:
        query += " AND (first_name LIKE ? OR last_name LIKE ?)"
        params.extend([f"%{name_query}%", f"%{name_query}%"])

    if month_query:
        query += " AND strftime('%m', generated_at) = ?"
        params.append(month_query.zfill(2))  # Ensure 2-digit format

    if year_query:
        query += " AND strftime('%Y', generated_at) = ?"
        params.append(year_query.zfill(4))  # Ensure 4-digit format
    query += " ORDER BY generated_at DESC"
    cursor.execute(query, tuple(params))
    results = cursor.fetchall()
    conn.close()
    return results
