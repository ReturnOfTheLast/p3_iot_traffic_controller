#!/usr/bin/env python3
# https://github.com/ReturnOfTheLast/p3_iot_traffic_controller

from logging import (
    Logger,
    FileHandler,
    StreamHandler,
    Formatter,
    getLogger,
    INFO
)
import sys


def get_logger(name: str) -> Logger:
    """Get preconfigured logger

    Args:
        name (str): Name of the logger to get

    Returns:
        Logger: The logger
    """
    logger = getLogger(name)
    logger.setLevel(INFO)

    log_format = "{name:<35s} {levelname:>8s}: {message}"

    log_file_handler = FileHandler('log_file.log')
    log_file_format = "{asctime:<25s}" + log_format
    log_file_formatter = Formatter(log_file_format, style="{")
    log_file_handler.setFormatter(log_file_formatter)

    log_term_handler = StreamHandler(sys.stdout)
    log_term_formatter = Formatter(log_format, style="{")
    log_term_handler.setFormatter(log_term_formatter)

    logger.addHandler(log_file_handler)
    logger.addHandler(log_term_handler)

    return logger
