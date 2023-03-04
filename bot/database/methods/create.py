from sqlite3 import Connection
from loguru import logger

def create_query(connection: Connection, query: str):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
    except Exception as ex:
        logger.error(ex)
