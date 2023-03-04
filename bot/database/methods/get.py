from sqlite3 import Connection
from loguru import logger

def select_query(connection: Connection, query: str):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Exception as ex:
        logger.error(ex)
