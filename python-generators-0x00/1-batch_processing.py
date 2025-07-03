import sqlite3
import json

def stream_users_in_batches(batch_size):
    """Generator that yields users in batches using SQL."""
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    
    offset = 0
    while True:
        cursor.execute("SELECT user_id, name, email, age FROM user_data LIMIT ? OFFSET ?", (batch_size, offset))
        rows = cursor.fetchall()
        if not rows:
            break
        yield rows
        offset += batch_size
    
    conn.close()

def batch_processing(batch_size):
    """Process batches and filter users over age 25."""
    for batch in stream_users_in_batches(batch_size):
        for row in batch:
            user = {
                "user_id": row[0],
                "name": row[1],
                "email": row[2],
                "age": row[3]
            }
            if user["age"] > 25:
                yield json.dumps(user)

# Example usage
if __name__ == "__main__":
    import sys
    try:
        for user in batch_processing(50):
            print(user)
    except BrokenPipeError:
        sys.stderr.close()
