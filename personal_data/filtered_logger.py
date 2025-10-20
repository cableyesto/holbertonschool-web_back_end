#!/usr/bin/env python3
""" Filtered Logger Script """

import re


def filter_datum(fields, redaction, message, separator):
    """Filter datum to obfuscate field"""
    res = message
    for field in fields:
        regex = str(field) + r'=\s*([^' + str(separator) + r']*)'
        res = re.sub(regex, str(field) + '=' + redaction, res)
    return res
