#!/usr/bin/env python3
""" Filtered Logger Script """

import re
import logging


def filter_datum(fields, redaction, message, separator):
    """Filter datum to obfuscate field"""
    res = message
    for field in fields:
        regex = str(field) + r'=\s*([^' + str(separator) + r']*)'
        res = re.sub(regex, str(field) + '=' + redaction, res)
    return res


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        res = filter_datum(self.fields, '***', re.sub(r';', '; ',
                           record.getMessage()), ';')
        log = logging.LogRecord("my_logger", logging.INFO, None, None,
                                res, None, None)
        return super().format(log)
