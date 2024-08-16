#!/usr/bin/env python3
"""Uses regex to obfuscate a message"""
import re
import csv
from typing import List
import logging


# Assuming user_data.csv has headers in the first row
PII_FIELDS = []
def process_csv(filename):
  """
  Extracts PII fields from the first row of the CSV file.
  """
  with open(filename, "r") as csvfile:
    reader = csv.reader(csvfile)
    headers = next(reader)
    # make PII_FIELDS global
    global PII_FIELDS
    PII_FIELDS = headers[:5]

def get_logger() -> logging.Logger:
  """
  Returns a configured logger named "user_data" for logging user data.
  """
  user_data = logging.Logger(__name__, level=logging.INFO)
  
  # Don't propagate messages to parent loggers
  user_data.propagate = False 

  # Process CSV to determine PII fields (call only once)
  process_csv("user_data.csv")

  # Create StreamHandler with RedactingFormatter
  handler = logging.StreamHandler()
  formatter = RedactingFormatter(PII_FIELDS)
  handler.setFormatter(formatter.format(formatter))
  user_data.addHandler(handler)

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
        """Format string output"""
        # Filter message using filter_datum (assuming it's defined elsewhere)
        record.msg = filter_datum(self.fields, self.REDACTION, record.msg,
                                  self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)
