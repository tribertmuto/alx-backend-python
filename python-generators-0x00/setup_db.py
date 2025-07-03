import sqlite3

# Connect and create table
conn = sqlite3.connect("users.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS user_data (
    user_id TEXT,
    name TEXT,
    email TEXT,
    age INTEGER
)
""")

# Sample data
sample_users = [
    ("00234e50-34eb-4ce2-94ec-26e3fa749796", "Dan Altenwerth Jr.", "Molly59@gmail.com", 67),
    ("006bfede-724d-4cdd-a2a6-59700f40d0da", "Glenda Wisozk", "Miriam21@gmail.com", 119),
    ("006e1f7f-90c2-45ad-8c1d-1275d594cc88", "Daniel Fahey IV", "Delia.Lesch11@hotmail.com", 49),
    ("00cc08cc-62f4-4da1-b8e4-f5d9ef5dbbd4", "Alma Bechtelar", "Shelly_Balistreri22@hotmail.com", 102),
    ("01187f09-72be-4924-8a2d-150645dcadad", "Jonathon Jones", "Jody.Quigley-Ziemann33@yahoo.com", 116)
]

cursor.executemany("INSERT INTO user_data VALUES (?, ?, ?, ?)", sample_users)

conn.commit()
conn.close()
