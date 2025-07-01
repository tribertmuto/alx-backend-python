def stream_user_ages():
    # Example data source - replace with actual data streaming logic
    user_ages = [25, 30, 22, 40, 28, 35]
    for age in user_ages:
        yield age

def calculate_average_age():
    total_age = 0
    count = 0
    for age in stream_user_ages():
        total_age += age
        count += 1
    average_age = total_age / count if count > 0 else 0
    print(f"Average age of users: {average_age}")

calculate_average_age()
