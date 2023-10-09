#!/usr/bin/env python3
# https://github.com/ReturnOfTheLast/p3_iot_traffic_controller

import logging
import sys


def get_module_logger(mod_name):
    logger = logging.getLogger(mod_name)
    logger.setLevel(logging.INFO)

    log_format = "{name:<20s} {levelname:>8s}: {message}"

    log_file_handler = logging.FileHandler('log_file.log')
    log_file_format = "{asctime:<25s}" + log_format
    log_file_formatter = logging.Formatter(log_file_format, style="{")
    log_file_handler.setFormatter(log_file_formatter)

    log_term_handler = logging.StreamHandler(sys.stdout)
    log_term_formatter = logging.Formatter(log_format, style="{")
    log_term_handler.setFormatter(log_term_formatter)

    logger.addHandler(log_file_handler)
    logger.addHandler(log_term_handler)

    return logger
