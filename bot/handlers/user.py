from aiogram import Dispatcher, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, CommandObject, Text

from bot.database import Database
from bot.lexicon import RU_LEXICON
from bot.keyboards import agree_button

router = Router()

@router.message(CommandStart())
async def command_start_process(message: Message, db: Database, command: CommandObject):
    is_confirm = await db.user_exists(command.args if command.args.isdigit() else None)
    if not is_confirm:
        await message.answer(text=RU_LEXICON['rules'], reply_markup=agree_button)
    else:
        await message.answer(text='Доделать')
         
@router.callback_query(Text(text='agree'))
async def callback_agree_process(callback: CallbackQuery, db: Database):
    pass