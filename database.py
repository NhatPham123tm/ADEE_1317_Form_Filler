import sqlite3

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
        data["first_name"], data["last_name"], data["middle_name"], data["date_of_birth"],
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
