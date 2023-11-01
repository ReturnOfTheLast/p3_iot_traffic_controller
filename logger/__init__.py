#!/usr/bin/env python3
# https://github.com/ReturnOfTheLast/p3_iot_traffic_controller

from logging import (
    Logger,
    FileHandler,
    StreamHandler,
    Formatter,
    getLogger,
    INFO,
    DEBUG
)
import sys
from os import environ


def get_logger(name: str) -> Logger:
    """Get preconfigured logger

    Args:
        name (str): Name of the logger to get

    Returns:
        Logger: The logger
    """
    logger: Logger = getLogger(name)
    logger.setLevel(DEBUG if environ.get("DEBUG") else INFO)

    log_format: str = "{name:<35s} {levelname:>8s}: {message}"

    log_file_handler: FileHandler = FileHandler('log_file.log')
    log_file_format: str = "{asctime:<25s}" + log_format
    log_file_formatter: Formatter = Formatter(log_file_format, style="{")
    log_file_handler.setFormatter(log_file_formatter)

    log_term_handler: StreamHandler = StreamHandler(sys.stdout)
    log_term_formatter: Formatter = Formatter(log_format, style="{")
    log_term_handler.setFormatter(log_term_formatter)

    logger.addHandler(log_file_handler)
    logger.addHandler(log_term_handler)

    return logger
