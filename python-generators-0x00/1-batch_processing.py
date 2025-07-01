import sys
from typing import Generator, List, Dict

def stream_users_in_batches(batch_size: int) -> Generator[List[Dict[str, object]], None, None]:
    """Stream users in batches using a generator.
    
    Args:
        batch_size: Number of users per batch
        
    Yields:
        Lists of user dictionaries in batches
    """
    user_data = [
        {'user_id': '00234e50-34eb-4ce2-94ec-26e3fa749796', 'name': 'Dan Altenwerth Jr.', 'email': 'Molly59@gmail.com', 'age': 67},
        {'user_id': '006bfede-724d-4cdd-a2a6-59700f40d0da', 'name': 'Glenda Wisozk', 'email': 'Miriam21@gmail.com', 'age': 119},
        {'user_id': '006e1f7f-90c2-45ad-8c1d-1275d594cc88', 'name': 'Daniel Fahey IV', 'email': 'Delia.Lesch11@hotmail.com', 'age': 49},
        {'user_id': '00cc08cc-62f4-4da1-b8e4-f5d9ef5dbbd4', 'name': 'Alma Bechtelar', 'email': 'Shelly_Balistreri22@hotmail.com', 'age': 102},
        {'user_id': '01187f09-72be-4924-8a2d-150645dcadad', 'name': 'Jonathon Jones', 'email': 'Jody.Quigley-Ziemann33@yahoo.com', 'age': 116},
    ]
    for i in range(0, len(user_data), batch_size):
        yield user_data[i:i + batch_size]

def batch_processing(batch_size: int) -> None:
    """Process batches of users and filter those over age 25.
    
    Args:
        batch_size: Number of users per batch to process
    """
    for batch in stream_users_in_batches(batch_size):
        for user in (u for u in batch if u['age'] > 25):
            try:
                print(user)
            except BrokenPipeError:
                sys.stderr.close()
                break

if __name__ == "__main__":
    batch_processing(50)
