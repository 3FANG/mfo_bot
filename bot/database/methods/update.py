from sqlite3 import Connection
from loguru import logger

def insert_query(connection: Connection, query: str, values: tuple):
    cursor = connection.cursor()
    try:
        cursor.execute(query, values)
        connection.commit()
    except Exception as ex:
        logger.error(ex)

def update_query(connection: Connection, query: str):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
    except Exception as ex:
        logger.error(ex)
