from datetime import datetime


def get_date_json():
    """
    Get the current date as a JSON-compatible dictionary.

    Returns:
        dict: A dictionary containing day, month, and year as strings
    """
    now = datetime.now()
    return {"day": str(now.day), "month": str(now.month), "year": str(now.year)}
