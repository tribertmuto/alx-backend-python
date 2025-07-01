def streamusersinbatches(batchsize):
    """
    Generator function that yields batches of users from in-memory data
    Each batch contains exactly batchsize users (except possibly the last one)
    Raises ValueError if batchsize is invalid
    """
    if not isinstance(batchsize, int) or batchsize <= 0:
        raise ValueError("batchsize must be a positive integer")

    # In-memory user data
    users = [
        {'user_id': '001', 'name': 'Alice', 'email': 'alice@example.com', 'age': 23},
        {'user_id': '002', 'name': 'Bob', 'email': 'bob@example.com', 'age': 30},
        {'user_id': '003', 'name': 'Charlie', 'email': 'charlie@example.com', 'age': 26},
        {'user_id': '004', 'name': 'Diana', 'email': 'diana@example.com', 'age': 24},
        {'user_id': '005', 'name': 'Eve', 'email': 'eve@example.com', 'age': 40},
    ]

    current_batch = []
    for user in users:
        current_batch.append(user)
        if len(current_batch) == batchsize:
            yield current_batch
            current_batch = []
    
    if current_batch:
        yield current_batch


def batch_processing(batchsize):
    """
    Processes user batches from streamusersinbatches()
    Yields individual users over age 25
    """
    if not isinstance(batchsize, int) or batchsize <= 0:
        raise ValueError("batchsize must be a positive integer")

    for batch in streamusersinbatches(batchsize):
        for user in batch:
            if user['age'] > 25:
                yield user


if __name__ == "__main__":
    # Example usage with batch size of 2
    for result in batch_processing(2):
        print(result)
