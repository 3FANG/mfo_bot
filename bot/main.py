import asyncio
import logging

from aiogram import Dispatcher, Bot
from asyncpg import Pool
from asyncpg import create_pool

from bot.middleware import DBMidlleware, PaymentMidlleware
from bot.config.config import load_config, Config
from bot.database import create_database
from bot.handlers import user, other

logger = logging.getLogger(__name__)

async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s '
               u'[%(asctime)s] - %(name)s - %(message)s',
        )
    logger.info('Bot started...')
    config: Config = load_config()

    await create_database()

    bot: Bot = Bot(token=(config.tg_bot.token))
    dp: Dispatcher = Dispatcher()
    pool: Pool = await create_pool(
        user=config.db.user,
        password=config.db.password,
        database=config.db.database,
        host=config.db.host,
        port=config.db.port
    )

    dp.include_router(user.router)
    dp.include_router(other.router)

    dp.middleware.setup(DBMidlleware(pool))
    dp.middleware.setup(PaymentMidlleware(config.ym.token, config.ym.account_number, config.ym.redirect_uri))

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await bot.close()

def start_bot():
    try:
        asyncio.run(main())
    except Exception as ex:
        logger.error(ex)
