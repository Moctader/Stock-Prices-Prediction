from datetime import datetime
from app.core.logging import logger


def parse_float(value, default=0.0):
    try:
        return float(value)
    except (ValueError, TypeError):
        logger.error(f"Failed to parse float: {value}")
        return default


def parse_int(value, default=0):
    try:
        return int(value)
    except (ValueError, TypeError):
        logger.error(f"Failed to parse int: {value}")
        return default


def parse_date(value):
    try:
        return datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
    except (ValueError, TypeError):
        logger.error(f"Failed to parse date: {value}")
        return None
