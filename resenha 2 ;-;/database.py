import sqlite3

DB_NAME = "mission.db"

def create_database():

    conn = sqlite3.connect("mission.db")

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS telemetry(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        temperature REAL,
        energy REAL,
        communication REAL,
        module_status TEXT
    )
    """)

    conn.commit()
    conn.close()


def save_telemetry(
        temperature,
        energy,
        communication,
        module_status):

    conn = sqlite3.connect("mission.db")

    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO telemetry(
        temperature,
        energy,
        communication,
        module_status
    )
    VALUES (?, ?, ?, ?)
    """,
    (
        temperature,
        energy,
        communication,
        module_status
    ))

    conn.commit()
    conn.close()


def get_last_records(limit=20):

    conn = sqlite3.connect("mission.db")

    cursor = conn.cursor()

    cursor.execute(f"""
    SELECT *
    FROM telemetry
    ORDER BY id DESC
    LIMIT {limit}
    """)

    data = cursor.fetchall()

    conn.close()

    return data