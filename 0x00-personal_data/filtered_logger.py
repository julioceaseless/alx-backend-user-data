#!/usr/bin/env python3
"""Uses regex to obfuscate a message"""
import re
from typing import List


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """Replace sensitive information in the message with redaction string."""
    # re.sub(pattern, repl, string, count=0, flags=0)
    for field in fields:
        pattern = rf'{field}=[^{separator}]*'
        message = re.sub(pattern, f'{field}={redaction}', message)
    return message
