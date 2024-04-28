import logging

def setup_logging(level=logging.INFO, log_file=None):
    """
    Sets up the logging configuration for the application.

    Args:
        level (int): Logging level, e.g., logging.INFO, logging.DEBUG.
        log_file (str, optional): Path to a log file where logs should be written.

    """
    log_format = "%(asctime)s - %(levelname)s - %(message)s"
    if log_file:
        # Configure logging to write to a specified log file and the console
        logging.basicConfig(level=level,
                            format=log_format,
                            handlers=[
                                logging.FileHandler(log_file),
                                logging.StreamHandler()
                            ])
    else:
        # Configure logging to write to the console
        logging.basicConfig(level=level, format=log_format)

