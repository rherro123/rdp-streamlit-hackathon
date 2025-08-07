import logging
import logging.config

from config import config

log = logging.getLogger(config.LOGGER_NAME)


def logging_config() -> None:
    """
    Configure logging
    """
    # initialize logging from config
    logging.config.fileConfig(config.LOGGING_CONFIG_FILE)
    log = logging.getLogger(config.LOGGER_NAME)
    root_handler = log.handlers[0]
    log_level = config.LOG_LEVEL if config.LOG_LEVEL else logging.INFO
    log.setLevel(log_level)
    root_handler.setLevel(log_level)

