# Python Decorators for Database Operations

This project demonstrates how to use Python decorators to enhance database operations using SQLite. Each task simulates real-world use cases like logging, connection management, transactions, retries, and caching.

## Requirements
- Python 3.8 or higher
- SQLite3
- `users.db` database with a `users` table

## Tasks

### 0. Logging Database Queries
- File: `0-log_queries.py`
- Logs SQL queries before executing them.

### 1. Handle Database Connections
- File: `1-with_db_connection.py`
- Automatically manages opening and closing of the database connection.

### 2. Transaction Management
- File: `2-transactional.py`
- Wraps function execution in a transaction (commit or rollback).

### 3. Retry on Failure
- File: `3-retry_on_failure.py`
- Retries failed database operations a set number of times with delay.

### 4. Cache Query Results
- File: `4-cache_query.py`
- Caches results of database queries to avoid redundant calls.

## Setup
Ensure you have a SQLite database named `users.db` with a `users` table:
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL
);
```

## Run
Run each script independently:
```bash
python3 0-log_queries.py
python3 1-with_db_connection.py
...
```

## Author
Your Name - ALX Backend Python Track