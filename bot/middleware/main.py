from aiogram import BaseMiddleware
from asyncpg import Pool

from bot.database import Database

class DBMidlleware(BaseMiddleware):
    def __init__(self, pool):
        super().__init__()
        self.pool: Pool = pool

    async def on_pre_process_message(self, obj, data, *args):
        connection = await self.pool.acquire()
        data["connection"] = connection
        data["db"] = Database(connection)

    async def on_pre_process_callback_query(self, obj, data, *args):
        connection = await self.pool.acquire()
        data["connection"] = connection
        data["db"] = Database(connection)

    async def on_post_process_message(self, obj, data_from_handler, data, *args):
        del data["db"]
        connection = data.get("connection")
        if connection:
            # check the documentation of your pool implementation
            # for proper way of releasing connection
            await self.pool.release(connection)

    async def on_post_process_callback_query(self, obj, data_from_handler, data, *args):
        del data["db"]
        connection = data.get("connection")
        if connection:
            # check the documentation of your pool implementation
            # for proper way of releasing connection
            await self.pool.release(connection)

class PaymentMidlleware(BaseMiddleware):
    def __init__(self, yoomoney_token: str, yoomoney_account_number: str, redirect_uri: str):
        super().__init__()
        self.yoomoney_token = yoomoney_token
        self.yoomoney_account_number = yoomoney_account_number
        self.redirect_uri = redirect_uri

    async def on_pre_process_message(self, obj, data, *args):
        data['yoomoney_token'] = self.yoomoney_token
        data['yoomoney_account_number'] = self.yoomoney_account_number
        data['redirect_uri'] = self.redirect_uri

    async def on_pre_process_callback_query(self, obj, data, *args):
        data['yoomoney_token'] = self.yoomoney_token
        data['yoomoney_account_number'] = self.yoomoney_account_number
        data['redirect_uri'] = self.redirect_uri
