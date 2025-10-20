#!/usr/bin/env python3
""" Filtered Logger Script """

import re
import logging
import os
import mysql.connector

PII_FIELDS = (
    'name',
    'email',
    'phone',
    'ssn',
    'password'
)


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


def get_logger() -> logging.Logger:
    """ Return a logger """
    streamHandler = logging.StreamHandler()
    streamHandler.setStream(RedactingFormatter(PII_FIELDS))
    logger = logging.getLogger("user_data")
    logger.propagate = False
    logger.addHandler(streamHandler)
    logger.setLevel(logging.INFO)
    return logger


def get_db():
    """ Return a db connection """
    db_username = os.environ["PERSONAL_DATA_DB_USERNAME"]
    db_pass = os.environ["PERSONAL_DATA_DB_PASSWORD"]
    db_host = os.environ["PERSONAL_DATA_DB_HOST"]
    db_name = os.environ["PERSONAL_DATA_DB_NAME"]
    config = {
        'user': db_username,
        'password': db_pass,
        'host': db_host,
        'database': db_name,
    }

    try:
        cnx = mysql.connector.connect(**config)
        return cnx
    except mysql.connector.Error as err:
        if err.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cnx.close()
