def stream_users_in_batches(batch_size):
    """
    Simulate streaming users from a data source, yielding lists of users in batches.
    Each user is a dict with keys: 'user_id', 'name', 'email', 'age'
    """
    # Simulated user data source - replace with real data fetching
    users = [
        {'user_id': '001', 'name': 'Alice', 'email': 'alice@example.com', 'age': 23},
        {'user_id': '002', 'name': 'Bob', 'email': 'bob@example.com', 'age': 30},
        {'user_id': '003', 'name': 'Charlie', 'email': 'charlie@example.com', 'age': 26},
        {'user_id': '004', 'name': 'Diana', 'email': 'diana@example.com', 'age': 24},
        {'user_id': '005', 'name': 'Eve', 'email': 'eve@example.com', 'age': 40},
        # Add as many as you want or fetch from real DB
    ]

    batch = []
    for user in users:
        batch.append(user)
        if len(batch) == batch_size:
            yield batch
            batch = []
    if batch:
        yield batch


def batch_processing(batch_size):
    """
    Process each batch from stream_users_in_batches.
    For each user in batch, if age > 25 yield that user dict.
    """
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user['age'] > 25:
                yield user
