import sqlite3
import json

def stream_users_in_batches(batch_size):
    """
    Fetches rows in batches from the 'user_data' table.
    Yields each batch using SQL with SELECT and FROM user_data.
    """
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    offset = 0
    while True:
        cursor.execute("SELECT user_id, name, email, age FROM user_data LIMIT ? OFFSET ?", (batch_size, offset))
        rows = cursor.fetchall()
        if not rows:
            break
        yield rows  # ✅ yield used, not return
        offset += batch_size

    conn.close()

def batch_processing(batch_size):
    """
    Processes users in batches and yields JSON for users older than 25.
    """
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

if __name__ == "__main__":
    import sys
    try:
        for user in batch_processing(2):  # Change batch size as needed
            print(user)
    except BrokenPipeError:
        sys.stderr.close()
