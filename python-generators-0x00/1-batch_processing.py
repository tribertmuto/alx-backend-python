def stream_users_in_batches(batch_size):
    """
    Simulate fetching user data in batches from a Python iterable (no SQL).
    Yield batches (lists) of user dicts.
    """

    # Example user data source — replace with your actual data iterable
    user_data = [
        {'user_id': '001', 'name': 'Alice', 'email': 'alice@example.com', 'age': 23},
        {'user_id': '002', 'name': 'Bob', 'email': 'bob@example.com', 'age': 30},
        {'user_id': '003', 'name': 'Charlie', 'email': 'charlie@example.com', 'age': 26},
        {'user_id': '004', 'name': 'Diana', 'email': 'diana@example.com', 'age': 24},
        {'user_id': '005', 'name': 'Eve', 'email': 'eve@example.com', 'age': 40},
        # Add more as needed
    ]

    batch = []
    for user in user_data:
        batch.append(user)
        if len(batch) == batch_size:
            yield batch
            batch = []
    if batch:
        yield batch


def batch_processing(batch_size):
    """
    Process batches of users fetched by stream_users_in_batches.
    Yield users who are older than 25 years.
    """

    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user['age'] > 25:
                yield user
