import logging


def get_logger(name, log_level):
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    _consolehandler = logging.StreamHandler()
    _consolehandler.setFormatter(logging.Formatter(
        "%(asctime)s [%(levelname)s] [%(name)s] - %(message)s"))
    logger.addHandler(_consolehandler)
    return logger
