import logging


def get_logging():
    return logging.basicConfig(level=logging.WARNING,
                    filename='Logs/Logs.log',
                    format="%(asctime)s - %(module)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s",
                    datefmt='%H:%M:%S',)
