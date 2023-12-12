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
from abc import ABC
from singleton import Singleton


class CustomFormatter(Formatter):
    lformat: str = "[{threadName:^13s}] {name:<25s} {levelname:>8s}: {message}"

    def __init__(self, prefix: str = None, suffix: str = None):
        if type(prefix) is str:
            self.lformat = prefix + self.lformat

        if type(suffix) is str:
            self.lformat = self.lformat + suffix

        Formatter.__init__(self, self.lformat, style="{")


class CustomFileFormatter(CustomFormatter):
    def __init__(self):
        prefix: str = "{asctime:<25s} "
        CustomFormatter.__init__(self, prefix=prefix)


class DebugFileHandler(FileHandler, metaclass=Singleton):
    def __init__(self):
        FileHandler.__init__(self, "debug.log")
        self.setFormatter(CustomFileFormatter())
        self.setLevel(DEBUG)


class InfoFileHandler(FileHandler, metaclass=Singleton):
    def __init__(self):
        FileHandler.__init__(self, "info.log")
        self.setFormatter(CustomFileFormatter())
        self.setLevel(INFO)


class ConsoleHandler(StreamHandler, metaclass=Singleton):
    def __init__(self):
        StreamHandler.__init__(self, sys.stdout)
        self.setFormatter(CustomFormatter())
        self.setLevel(INFO)


class LoggingObject(ABC):
    """Describes an element that can log
    """

    _logger = None

    @property
    def logger(self):
        if not self._logger:
            self._logger: Logger = getLogger(
                f"{self.__module__}.{self.__class__.__qualname__}"
            )
            self._logger.setLevel(DEBUG)
            self._logger.addHandler(DebugFileHandler())
            self._logger.addHandler(InfoFileHandler())
            self._logger.addHandler(ConsoleHandler())
        return self._logger
