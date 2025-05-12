import sqlite3
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

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
            male INTEGER,
            female INTEGER,       
            date_of_birth TEXT,
            classroom_date TEXT,
            online_date TEXT,
            road_rule INTEGER,
            road_sign INTEGER,
            school_name TEXT,
            tdlr TEXT,
            educator_number TEXT,
            date_issued TEXT,
            driver_ed INTEGER,
            private_school INTEGER,
            duplicate INTEGER,
            public_school INTEGER,
            service_center INTEGER,
            college INTEGER,
            at_dps INTEGER,
            vision_exam INTEGER,
            generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def get_connection():
    return sqlite3.connect(DB_NAME)

def save_submission(data, conn=None, cursor=None):
    internal = False
    if conn is None or cursor is None:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        internal = True

    # Get current Central Time (DST-aware)
    central_now = datetime.now(ZoneInfo("America/Chicago")).replace(tzinfo=None)

    cursor.execute("""
        INSERT INTO submissions (
            control_number, first_name, last_name, middle_name, date_of_birth,
            classroom_date, online_date, road_rule, road_sign, school_name, 
            tdlr, educator_number, date_issued, male, female,
            driver_ed, private_school, duplicate, public_school,
            service_center, college, at_dps, vision_exam, generated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data["control_number"], data["first_name"], data["last_name"], data["middle_name"], data["date_of_birth"],
        data["classroom_date"], data["online_date"], data["road_rule"], data["road_sign"], data["school_name"],
        data["tdlr"], data["educator_number"], data["date_issued"], data["male"], data["female"],
        data["driver_ed"], data["private_school"], data["duplicate"], data["public_school"],
        data["service_center"], data["college"], data["at_dps"], data["vision_exam"],
        central_now.isoformat()
    ))

    if internal:
        conn.commit()
        conn.close()

def get_all_submissions():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, control_number, first_name, last_name, middle_name,
               date_of_birth, classroom_date, online_date, road_rule, road_sign,
               school_name, tdlr, educator_number, date_issued, generated_at
        FROM submissions
        ORDER BY datetime(generated_at) DESC
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_today_submissions():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    today = datetime.now().date()
    tomorrow = today + timedelta(days=1)

    cursor.execute("""
        SELECT id, control_number, first_name, last_name, middle_name,
               date_of_birth, classroom_date, online_date, road_rule, road_sign,
               school_name, tdlr, educator_number, date_issued, generated_at
        FROM submissions
        WHERE generated_at >= ? AND generated_at < ?
        ORDER BY datetime(generated_at) DESC
    """, (today.isoformat(), tomorrow.isoformat()))

    rows = cursor.fetchall()
    conn.close()
    return rows

def is_control_number_exists(control_number):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM submissions WHERE control_number = ?", (control_number,))
    exists = cursor.fetchone()[0] > 0
    conn.close()
    return exists

def get_latest_number():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT control_number FROM submissions")
    rows = cursor.fetchall()
    conn.close()

    max_number = 0
    for row in rows:
        cn = row[0]
        try:
            num = int(cn.split()[1])
            max_number = max(max_number, num)
        except (IndexError, ValueError):
            continue  # skip malformed control numbers

    return max_number

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

    query = """SELECT id, control_number, first_name, last_name, middle_name,
               date_of_birth, classroom_date, online_date, road_rule, road_sign,
               school_name, tdlr, educator_number, date_issued, generated_at 
               FROM submissions WHERE 1=1"""
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
