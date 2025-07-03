# 1-batch_processing.py
import json

def stream_users_in_batches(batch_size):
    """Generator that yields users in batches without database queries."""
    # Simulated user data (this would typically come from a database or file)
    users = [
        {"user_id": "00234e50-34eb-4ce2-94ec-26e3fa749796", "name": "Dan Altenwerth Jr.", "email": "Molly59@gmail.com", "age": 67},
        {"user_id": "006bfede-724d-4cdd-a2a6-59700f40d0da", "name": "Glenda Wisozk", "email": "Miriam21@gmail.com", "age": 119},
        {"user_id": "006e1f7f-90c2-45ad-8c1d-1275d594cc88", "name": "Daniel Fahey IV", "email": "Delia.Lesch11@hotmail.com", "age": 49},
        {"user_id": "00cc08cc-62f4-4da1-b8e4-f5d9ef5dbbd4", "name": "Alma Bechtelar", "email": "Shelly_Balistreri22@hotmail.com", "age": 102},
        {"user_id": "01187f09-72be-4924-8a2d-150645dcadad", "name": "Jonathon Jones", "email": "Jody.Quigley-Ziemann33@yahoo.com", "age": 116},
        # Add more test data as needed
    ]
    
    # First loop - yields batches
    for i in range(0, len(users), batch_size):
        yield users[i:i + batch_size]

def batch_processing(batch_size):
    """Process batches and filter users over age 25."""
    # Second loop - processes batches
    for batch in stream_users_in_batches(batch_size):
        # Third loop - filters users
        for user in batch:
            if user["age"] > 25:
                yield json.dumps(user)  # Use yield instead of print

# Example usage (this part would be in your 2-main.py)
if __name__ == "__main__":
    import sys
    try:
        for user in batch_processing(50):
            print(user)
    except BrokenPipeError:
        sys.stderr.close()
