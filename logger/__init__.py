#!/usr/bin/env python3
# https://github.com/ReturnOfTheLast/p3_iot_traffic_controller

import logging
import sys


def get_module_logger(mod_name):
    logger = logging.getLogger(mod_name)
    logger.setLevel(logging.INFO)

    log_file_handler = logging.FileHandler('log_file.log')
    log_file_format = "%(asctime)s %(name)s %(levelname)s: %(message)s"
    log_file_formatter = logging.Formatter(log_file_format)
    log_file_handler.setFormatter(log_file_formatter)

    log_term_handler = logging.StreamHandler(sys.stdout)
    log_term_format = "%(name)s %(levelname)s: %(message)s"
    log_term_formatter = logging.Formatter(log_term_format)
    log_term_handler.setFormatter(log_term_formatter)

    logger.addHandler(log_file_handler)
    logger.addHandler(log_term_handler)

    return logger
