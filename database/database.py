import sqlite3
import os
import datetime

# Path to SQLite database file inside data/ directory
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "women_safety.db")

def get_connection():
    """Returns a connection object to the SQLite database."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Allows accessing columns by column name
    return conn

def initialize_database():
    """
    Creates the 'alerts' and 'gender_stats' tables if they do not already exist.
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            alert_type TEXT NOT NULL,
            severity TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            location TEXT NOT NULL,
            male_count INTEGER DEFAULT 0,
            female_count INTEGER DEFAULT 0,
            description TEXT
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS gender_stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            source_name TEXT NOT NULL,
            male_count INTEGER DEFAULT 0,
            female_count INTEGER DEFAULT 0,
            total_count INTEGER DEFAULT 0
        );
    """)
    
    conn.commit()
    conn.close()

def save_alert(alert_type, severity, timestamp, location, male_count, female_count, description):
    """
    Saves a single safety alert to the SQLite database.
    """
    initialize_database()
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO alerts (alert_type, severity, timestamp, location, male_count, female_count, description)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (alert_type, severity, timestamp, location, male_count, female_count, description))
    
    conn.commit()
    alert_id = cursor.lastrowid
    conn.close()
    return alert_id

def get_all_alerts():
    """
    Retrieves all recorded alerts from the database ordered by newest first.
    Returns a list of dictionaries.
    """
    initialize_database()
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM alerts ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]

def get_alert_count():
    """
    Returns the total number of safety alerts recorded in the database.
    """
    initialize_database()
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM alerts")
    count = cursor.fetchone()[0]
    conn.close()
    
    return count

def get_alerts_by_location(location):
    """
    Retrieves recorded safety alerts filtered by camera/location name.
    """
    initialize_database()
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM alerts WHERE location = ? ORDER BY id DESC", (location,))
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]

# --- GENDER STATISTICS FUNCTIONS ---

def save_gender_stat(source_name, male_count, female_count):
    """
    Saves scene gender detection counts to the database.
    """
    initialize_database()
    conn = get_connection()
    cursor = conn.cursor()

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    total_count = male_count + female_count

    cursor.execute("""
        INSERT INTO gender_stats (timestamp, source_name, male_count, female_count, total_count)
        VALUES (?, ?, ?, ?, ?)
    """, (timestamp, source_name, male_count, female_count, total_count))

    conn.commit()
    stat_id = cursor.lastrowid
    conn.close()
    return stat_id

def get_aggregate_gender_stats():
    """
    Computes overall aggregated gender statistics across all analyzed scenes.
    """
    initialize_database()
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT SUM(male_count), SUM(female_count), SUM(total_count) FROM gender_stats")
    result = cursor.fetchone()
    conn.close()

    males = result[0] if result[0] is not None else 0
    females = result[1] if result[1] is not None else 0
    total = result[2] if result[2] is not None else 0

    male_pct = (males / total * 100.0) if total > 0 else 0.0
    female_pct = (females / total * 100.0) if total > 0 else 0.0

    return {
        "total": total,
        "male": males,
        "female": females,
        "male_pct": male_pct,
        "female_pct": female_pct
    }

def get_latest_gender_stat():
    """
    Returns the most recent scene gender detection record.
    """
    initialize_database()
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM gender_stats ORDER BY id DESC LIMIT 1")
    row = cursor.fetchone()
    conn.close()

    return dict(row) if row else None
