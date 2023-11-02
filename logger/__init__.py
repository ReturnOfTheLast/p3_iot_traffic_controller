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
from singleton import Singleton


class CustomFormatter(Formatter):
    def __init__(self, time=False):
        lformat: str = "{asctime:<25s} {name:<35s} {levelname:>8s}: {message}"
        Formatter.__init__(self, lformat, style="{")


class DebugFileHandler(FileHandler, metaclass=Singleton):
    def __init__(self):
        FileHandler.__init__(self, "debug.log")
        self.setFormatter(CustomFormatter(time=True))
        self.setLevel(DEBUG)


class InfoFileHandler(FileHandler, metaclass=Singleton):
    def __init__(self):
        FileHandler.__init__(self, "info.log")
        self.setFormatter(CustomFormatter(time=True))
        self.setLevel(INFO)


class ConsoleHandler(StreamHandler, metaclass=Singleton):
    def __init__(self):
        StreamHandler.__init__(self, sys.stdout)
        self.setFormatter(CustomFormatter())
        self.setLevel(INFO)


def get_logger(name: str) -> Logger:
    """Get preconfigured logger

    Args:
        name (str): Name of the logger to get

    Returns:
        Logger: The logger
    """
    logger: Logger = getLogger(name)
    logger.setLevel(DEBUG)

    logger.addHandler(DebugFileHandler())
    logger.addHandler(InfoFileHandler())
    logger.addHandler(ConsoleHandler())

    return logger
