from datetime import datetime
import pytz


def get_time_now(timezone: str or None = None):
    if not timezone:
        return datetime.now()
    tz = pytz.timezone(timezone)
    now = datetime.now(tz)
    return now