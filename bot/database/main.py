import logging
import os

import asyncpg
from asyncpg import Connection, Record
from aiogram.types import User

from bot.config import load_config

CFG = load_config()

logger = logging.getLogger(__name__)

async def create_database():
    connection = None
    try:
        connection = await asyncpg.connect(
            database=CFG.db.database,
            user=CFG.db.user,
            password=CFG.db.password,
            host=CFG.db.host,
            port=CFG.db.port
        )

        create_db_command = open(os.path.join('bot', 'database', 'create_db.sql'), 'r', encoding='utf-8').read()
        await connection.execute(create_db_command)
        logger.debug("Tables has been created")

    except Exception as ex:
        logger.error(ex)

    finally:
        if connection:
            await connection.close()

    return connection

class Database:
    EXISTS_USER = "SELECT EXISTS(SELECT id FROM Users WHERE id = $1)"
    ADD_NEW_USER = "INSERT INTO Users(id, username, first_name, last_name) VALUES ($1, $2, $3, $4) ON CONFLICT DO NOTHING RETURNING сonfirm"
    ADD_NEW_USER_REFERRAL = "INSERT INTO Users(id, username, first_name, last_name, referral) VALUES ($1, $2, $3, $4, $5) ON CONFLICT DO NOTHING RETURNING id"

    def __init__(self, connection):
        self.connection: Connection = connection

    async def user_exists(self, id: int):
        command = self.EXISTS_USER
        return await self.connection.fetchval(command, id)

    async def add_new_user(self, referral: int=None):
        user = User.get_current()
        chat_id = user.id
        username = user.username
        first_name = user.first_name
        last_name = user.last_name
        args = chat_id, username, first_name, last_name
        if referral:
            args += (referral,)
            command = self.ADD_NEW_USER_REFERRAL
        else:
            command = self.ADD_NEW_USER
        record_id = await self.connection.fetchval(command, *args)
        return record_id

