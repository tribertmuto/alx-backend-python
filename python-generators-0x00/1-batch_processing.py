def stream_users_in_batches(batch_size):
    """
    Yield batches of users of size batch_size from a data iterable.
    Raises ValueError if batch_size is invalid.
    """

    if not isinstance(batch_size, int) or batch_size <= 0:
        raise ValueError("batch_size must be a positive integer")

    user_data = [
        {'user_id': '001', 'name': 'Alice', 'email': 'alice@example.com', 'age': 23},
        {'user_id': '002', 'name': 'Bob', 'email': 'bob@example.com', 'age': 30},
        {'user_id': '003', 'name': 'Charlie', 'email': 'charlie@example.com', 'age': 26},
        {'user_id': '004', 'name': 'Diana', 'email': 'diana@example.com', 'age': 24},
        {'user_id': '005', 'name': 'Eve', 'email': 'eve@example.com', 'age': 40},
        # ... add more if needed
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
    Process each batch yielded by stream_users_in_batches.
    Yield individual users over the age of 25.
    Raises ValueError if batch_size is invalid.
    """

    if not isinstance(batch_size, int) or batch_size <= 0:
        raise ValueError("batch_size must be a positive integer")

    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user['age'] > 25:
                yield user
