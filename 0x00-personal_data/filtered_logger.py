#!/usr/bin/env python3
"""Uses regex to obfuscate a message"""
import re
import csv
from typing import List
import logging


def csv_processor(filename):
    """reads csv to extract the headers"""
    headers = ""
    with open(filename, 'r', encoding="utf-8") as file:
        line = csv.reader(file)
        headers = next(line)
    return headers[:5]


# get headers from
PII_FIELDS = csv_processor("user_data.csv")


def get_logger() -> logging.Logger:
    """
    Returns a configured logger named "user_data" for logging user data.
    """
    # create a logger object
    user_data = logging.Logger(__name__)
    user_data.level = logging.INFO
    user_data.propagate = False

    StreamHandler = logging.StreamHandler()
    StreamHandler.setFormatter(RedactingFormatter(PII_FIELDS))

    user_data.addHandler(StreamHandler)

    return user_data


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """Replace sensitive information in the message with redaction string."""
    # re.sub(pattern, repl, string, count=0, flags=0)
    for field in fields:
        pattern = rf'{field}=[^{separator}]*'
        message = re.sub(pattern, f'{field}={redaction}', message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """format the string output"""
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.getMessage(), self.SEPARATOR)
        # print(super().format(record).replace(record.msg, msg))
        return super().format(record)
