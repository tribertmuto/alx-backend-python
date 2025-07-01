def check_for_sql_keywords(filename):
    with open(filename, 'r') as file:
        code = file.read().lower()
        if 'select' in code or 'from user_data' in code:
            return False
    return True

if __name__ == "__main__":
    file_ok = check_for_sql_keywords("1-batch_processing.py")
    if file_ok:
        print("No SQL keywords found — file passes the check.")
    else:
        print("SQL keywords found — file fails the check.")
