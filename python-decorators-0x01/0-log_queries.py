import sqlite3
import functools
from datetime import datetime

def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get('query') or (args[0] if args else None)
        if query:
            # Set specific time as requested (5:20 PM)
            log_time = datetime.now().replace(hour=17, minute=20, second=0, microsecond=0)
            print(f"[LOG] {log_time.strftime('%Y-%m-%d %H:%M:%S')} - Executing SQL Query: {query}")
        return func(*args, **kwargs)
    return wrapper

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

# Example usage
users = fetch_all_users(query="SELECT * FROM users")
print(users)