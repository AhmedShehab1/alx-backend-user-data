#!/usr/bin/env python3
"""
filtered_logger
"""
import re
import logging
from typing import List
import os


def filter_datum(
    fields: List[str], redaction: str, message: str, separator: str
) -> str:
    """
    Uses regex to obfuscate PII fields
    Args:
        fields (List[str]): fields to search for and obfuscate
        redaction (str): string used as obfuscation
        message (str): message to be obfuscated
        separator (str): delimeter between fields

    Returns:
        str: New Obfuscated Message
    """
    for field in fields:
        pattern = f"{field}=.*?(?={separator})"
        message = re.sub(pattern, f"{field}={redaction}", message)
    return message


class RedactingFormatter(logging.Formatter):
    """
    Redacting Formatter Class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        RedactingFormatter Constructor
        Args:
            fields (List[str]): PII Fields
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        formats record msg
        Args:
            record (logging.LogRecord): logged record

        Returns:
            str: Formatted Message
        """
        record.msg = filter_datum(
            self.fields, self.REDACTION, record.msg, self.SEPARATOR
        )
        return super(RedactingFormatter, self).format(record)


def get_db():
    """
    Uses ENV VAR To connect to a mysql db
    Returns:
        connector object
    """
    conn = mysql.connector.connect(
        host=os.getenv("PERSONAL_DATA_DB_HOST", "localhost"),
        user=os.getenv("PERSONAL_DATA_DB_USERNAME", "root"),
        password=os.getenv("PERSONAL_DATA_DB_PASSWORD", ""),
        database=os.getenv("PERSONAL_DATA_DB_NAME"),
    )
    return conn
