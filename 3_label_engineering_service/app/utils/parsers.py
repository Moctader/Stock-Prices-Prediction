from datetime import datetime
from app.core.logging import logger


def parse_float(value):
    try:
        return float(value)
    except (ValueError, TypeError):
        logger.error(f"Failed to parse float: {value}")
        return None


def parse_int(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        logger.error(f"Failed to parse int: {value}")
        return None


def parse_date(value):
    try:
        return datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
    except (ValueError, TypeError):
        logger.error(f"Failed to parse date: {value}")
        return None
