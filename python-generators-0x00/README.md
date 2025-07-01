# alx-backend-python
# ALX Prodev MySQL Seeder

This Python script (`seed.py`) sets up a MySQL database named `ALX_prodev` and populates it with user data from a CSV file.

## Features

- Connects to MySQL server.
- Creates the database `ALX_prodev` if it doesn't exist.
- Creates a `user_data` table with fields:
  - `user_id` (Primary Key, UUID)
  - `name` (VARCHAR, NOT NULL)
  - `email` (VARCHAR, NOT NULL)
  - `age` (DECIMAL, NOT NULL)
- Reads user data from `user_data.csv` and inserts records, skipping duplicates based on email.
