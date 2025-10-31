import datetime
import json


def get_date_json():
    # Get the current date
    now = datetime.datetime.now()

    # Get the day of the year
    day_of_year = now.timetuple().tm_yday

    # Create a dictionary (map) with month, day of year, and year
    date_map = {
        "month": now.month,
        "day": day_of_year,  # day of the year
        "year": now.year,
    }

    # Convert the dictionary to a JSON string
    date_json = json.dumps(date_map)

    return date_json
