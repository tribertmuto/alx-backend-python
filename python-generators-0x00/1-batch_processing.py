import json

def stream_users_in_batches(batch_size):
    """
    Generator that yields users in batches without using return.
    """
    users = [
        {"user_id": "00234e50-34eb-4ce2-94ec-26e3fa749796", "name": "Dan Altenwerth Jr.", "email": "Molly59@gmail.com", "age": 67},
        {"user_id": "006bfede-724d-4cdd-a2a6-59700f40d0da", "name": "Glenda Wisozk", "email": "Miriam21@gmail.com", "age": 119},
        {"user_id": "006e1f7f-90c2-45ad-8c1d-1275d594cc88", "name": "Daniel Fahey IV", "email": "Delia.Lesch11@hotmail.com", "age": 49},
        {"user_id": "00cc08cc-62f4-4da1-b8e4-f5d9ef5dbbd4", "name": "Alma Bechtelar", "email": "Shelly_Balistreri22@hotmail.com", "age": 102},
        {"user_id": "01187f09-72be-4924-8a2d-150645dcadad", "name": "Jonathon Jones", "email": "Jody.Quigley-Ziemann33@yahoo.com", "age": 116}
    ]

    for i in range(0, len(users), batch_size):
        yield users[i:i + batch_size]  # ✅ Using yield, not return

def batch_processing(batch_size):
    """
    Processes each batch and yields JSON strings for users over 25.
    """
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user["age"] > 25:
                yield json.dumps(user)  # ✅ Using yield, not return

if __name__ == "__main__":
    import sys
    try:
        for user_json in batch_processing(2):
            print(user_json)
    except BrokenPipeError:
        sys.stderr.close()
