import logging
import pyodbc

from config.settings import settings

logger = logging.getLogger(__name__)

CONNECTION_STRING = settings.database_connection_string


def get_connection():
    try:
        return pyodbc.connect(CONNECTION_STRING)

    except pyodbc.Error as e:
        logger.exception(
            "Failed to connect to SQL Server",
            extra={
                "error_type": type(e).__name__,
                "error_message": str(e),
                "operation": "database_connect",
            },
        )
        raise