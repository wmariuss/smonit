from datetime import datetime


def time(time_format=None):
    if not time_format:
        time_format = "%Y-%m-%dT%H:%M:%SZ"

    return datetime.utcnow().strftime(time_format)
