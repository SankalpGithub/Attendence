from datetime import datetime, timedelta
import pytz
    

# Get the current date and time
def daytime():

    # Get the current time in UTC
    utc_time = datetime.utcnow()

    # Define the Indian Standard Time (IST) timezone
    ist_timezone = pytz.timezone('Asia/Kolkata')

    # Convert the UTC time to IST
    ist_time = utc_time + timedelta(hours=5, minutes=30)
    ist_time = ist_timezone.localize(ist_time)

    # Extract the date, time, and day of the week
    ist_date = str(ist_time.date())
    ist_time_of_day = str(ist_time.strftime('%I:%M %p'))
    ist_day = str(ist_time.strftime('%A'))  # %A gives the full weekday name

    # Format the IST time as a string
    ist_time_str = ist_time.strftime('%Y-%m-%d %H:%M:%S')

    daytime = {
        "date": ist_date,
        "day": ist_day,
        "time": ist_time_of_day
    }
    
    return daytime
