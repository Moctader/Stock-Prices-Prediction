from datetime import datetime


def parse_float(value):
    try:
        return float(value)
    except (ValueError, TypeError):
        return None


def parse_int(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        return None


def parse_date(value):
    try:
        return datetime.strptime(value, "%Y-%m-%d")
    except (ValueError, TypeError):
        return None
