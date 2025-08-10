#!/usr/bin/python3
import sqlite3

def stream_users():
    """
    Generator function that streams users from the database one by one.
    Yields each user as a dictionary with user_id, name, email, and age.
    """
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT user_id, name, email, age FROM user_data")
        
        while True:
            row = cursor.fetchone()
            if row is None:
                break
            
            user = {
                "user_id": row[0],
                "name": row[1],
                "email": row[2],
                "age": row[3]
            }
            yield user
    
    finally:
        conn.close()

# Make the function directly callable when the module is imported
__all__ = ['stream_users']

# If called as a script, you can test it directly
if __name__ == "__main__":
    for user in stream_users():
        print(user)