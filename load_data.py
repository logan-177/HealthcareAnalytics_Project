import sqlite3
import pandas as pd
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / 'data' / 'healthcare.db'

def load (query = None):
    print (f"Connecting to: {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    if query is None:
        query = "SELECT * FROM patients"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df