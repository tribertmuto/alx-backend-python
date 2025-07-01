#!/usr/bin/python3
import sqlite3

def stream_users():
    conn = sqlite3.connect('user_data.db')
    conn.row_factory = sqlite3.Row  # This allows accessing columns by name
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_data")
    for row in cursor:
        yield dict(row)
    cursor.close()
    conn.close()
