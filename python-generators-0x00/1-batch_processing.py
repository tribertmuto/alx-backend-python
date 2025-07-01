def stream_users_in_batches(batchsize):
    """
    Yield batches of users of size batchsize from an in-memory data list.
    Raises ValueError if batchsize is invalid.
    """
    if not isinstance(batchsize, int) or batchsize <= 0:
        raise ValueError("batchsize must be a positive integer")

    user_data = [
        {'user_id': '001', 'name': 'Alice', 'email': 'alice@example.com', 'age': 23},
        {'user_id': '002', 'name': 'Bob', 'email': 'bob@example.com', 'age': 30},
        {'user_id': '003', 'name': 'Charlie', 'email': 'charlie@example.com', 'age': 26},
        {'user_id': '004', 'name': 'Diana', 'email': 'diana@example.com', 'age': 24},
        {'user_id': '005', 'name': 'Eve', 'email': 'eve@example.com', 'age': 40},
        # Add more users if needed
    ]

    batch = []
    for user in user_data:
        batch.append(user)
        if len(batch) == batchsize:
            yield batch
            batch = []
    if batch:
        yield batch


def batch_processing(batchsize):
    """
    Process each batch from stream_users_in_batches.
    Yield individual users over the age of 25.
    Raises ValueError if batchsize is invalid.
    """
    if not isinstance(batchsize, int) or batchsize <= 0:
        raise ValueError("batchsize must be a positive integer")

    for batch in stream_users_in_batches(batchsize):
        for user in batch:
            if user['age'] > 25:
                yield user


# Example usage
if __name__ == "__main__":
    for user in batch_processing(2):
        print(user)
