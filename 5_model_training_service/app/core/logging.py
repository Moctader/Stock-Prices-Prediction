from app.core.settings import settings
import logging
from graypy import GELFUDPHandler


def setup_logging():
    logging.basicConfig(level=logging.INFO)

    if settings.LOGGER_CONSOLE:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        logging.getLogger().addHandler(console_handler)

    if settings.LOGGER_GRAYLOG:
        graylog_handler = GELFUDPHandler(
            settings.LOGGER_GRAYLOG_HOST, settings.LOGGER_GRAYLOG_PORT)
        logging.getLogger().addHandler(graylog_handler)


logger = logging.getLogger(settings.PROJECT_NAME)
