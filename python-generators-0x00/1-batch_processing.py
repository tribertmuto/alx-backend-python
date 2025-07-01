def streamusersinbatches(batchsize):
    """
    Generator function that yields batches of users from in-memory data
    Each batch contains exactly batchsize users (except possibly the last one)
    Raises ValueError if batchsize is invalid
    """
    if not isinstance(batchsize, int) or batchsize <= 0:
        raise ValueError("batchsize must be a positive integer")

    # In-memory user data simulating a data source
    all_users = [
        {'user_id': '001', 'name': 'Alice', 'email': 'alice@example.com', 'age': 23},
        {'user_id': '002', 'name': 'Bob', 'email': 'bob@example.com', 'age': 30},
        {'user_id': '003', 'name': 'Charlie', 'email': 'charlie@example.com', 'age': 26},
        {'user_id': '004', 'name': 'Diana', 'email': 'diana@example.com', 'age': 24},
        {'user_id': '005', 'name': 'Eve', 'email': 'eve@example.com', 'age': 40},
    ]

    current_batch = []
    for user in all_users:
        current_batch.append(user)
        if len(current_batch) == batchsize:
            yield current_batch
            current_batch = []
    
    # Yield any remaining users in partial batch
    if current_batch:
        yield current_batch


def batch_processing(batchsize):
    """
    Processes user batches and yields individual users over age 25
    Raises ValueError if batchsize is invalid
    """
    if not isinstance(batchsize, int) or batchsize <= 0:
        raise ValueError("batchsize must be a positive integer")

    for batch in streamusersinbatches(batchsize):
        for user in batch:
            if user['age'] > 25:
                yield user


# Example usage
if __name__ == "__main__":
    # Process in batches of 2 and print users over 25
    for user in batch_processing(2):
        print(f"Matched user: {user['name']} (age: {user['age']})")
