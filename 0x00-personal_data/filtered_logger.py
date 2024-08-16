#!/usr/bin/env python3
"""Uses regex to obfuscate a message"""
import csv
import logging
import os
import re
from typing import List
import mysql.connector


def csv_processor(filename):
    """reads csv to extract the headers"""
    headers = ""
    with open(filename, 'r', encoding="utf-8") as file:
        line = csv.reader(file)
        headers = next(line)
    return headers[:5]


# get headers from
PII_FIELDS = tuple(csv_processor("user_data.csv"))


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    Connects to secure database and read users table

    Returns:
        - mysql.connector.connection.MySQLConnection:
        Connection object to the MySQL database
    """
    user = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    database = os.getenv("PERSONAL_DATA_DB_NAME")

    # create a database connection object
    conn = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
        )
    return conn
    """
    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    # Execute a query
    cursor.execute("SELECT * FROM users")

    # Fetch the results
    results = cursor.fetchall()

    # Process the results
    for row in results:
        print(row)

    # Close the cursor and connection
    cursor.close()
    conn.close()
    """


def get_logger() -> logging.Logger:
    """
    Returns a configured logger named "user_data" for logging user data.
    """
    # create a logger object
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    StreamHandler = logging.StreamHandler()
    StreamHandler.setFormatter(RedactingFormatter(PII_FIELDS))

    logger.addHandler(StreamHandler)

    return logger


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
