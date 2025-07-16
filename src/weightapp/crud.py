
# gripper_ranker/app/crud.py
import sqlite3
from src.weightapp.models import DB_PATH

def save_gripper_data(name, parameters: dict):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute("INSERT INTO grippers (name) VALUES (?)", (name,))
    gripper_id = c.lastrowid
    
    for param_name, value in parameters.items():
        c.execute("INSERT INTO parameters (gripper_id, name, value) VALUES (?, ?, ?)",
                  (gripper_id, param_name, value))
    
    conn.commit()
    conn.close()
    return gripper_id
