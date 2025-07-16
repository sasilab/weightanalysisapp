# gripper_ranker/app/models.py
import sqlite3

DB_PATH = "database/gripper.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute("""
    CREATE TABLE IF NOT EXISTS grippers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT
    )
    """)
    
    c.execute("""
    CREATE TABLE IF NOT EXISTS parameters (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        gripper_id INTEGER,
        name TEXT,
        value TEXT,
        FOREIGN KEY (gripper_id) REFERENCES grippers (id)
    )
    """)
    
    conn.commit()
    conn.close()
