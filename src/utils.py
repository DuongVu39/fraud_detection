import logging

def logging_wrapper(level, path):
    """Producing log message

    :param level: Logging level. Default=3. 1-5 scale determining the logging messages to save.
                 5 is only CRITICAL, 1 is all message
    :param path:  Default=logs/{scipt_name}_{unix_time}.log
                Path to the desired location to store logs

    :return: Log message
    """

    # Determine desired logging level
    level = int(str(level) + "0")

    # Create a logging instance
    logger = logging.getLogger()
    logger.setLevel(level)

    # Setup logging file
    logger_handler = logging.FileHandler(path)
    logger_handler.setLevel(level)

    # Formatting
    logger_formatter = logging.Formatter("%(name)s - %(levelname)s - %(message)s")

    # Put them together
    logger_handler.setFormatter(logger_formatter)

    logger.addHandler(logger_handler)
    logger.info("Logging successfully configured.")

    return logger
