import datetime

# Get the current date and time
def daytime():
    current_datetime = datetime.datetime.now()
    
    # Extract the day, date, and time components
    current_day = current_datetime.strftime("%A")  # Full day name (e.g., "Monday")
    current_date = current_datetime.strftime("%Y-%m-%d")  # Date in yyyy-mm-dd format (e.g., "2023-09-23")
    current_time = current_datetime.strftime("%I:%M %p")  # Time in HH:MM:SS format (e.g., "14:30:00")
    
    daytime = {
        "date": current_date,
        "day": current_day,
        "time": current_time
    }
    
    return daytime
