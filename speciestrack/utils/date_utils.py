import datetime


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

    return date_map