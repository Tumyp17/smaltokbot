import aiogram
from aiogram import exceptions
from config_reader import config
from aiogram import Bot

bot = Bot(token=config.bot_token.get_secret_value())


async def remove_inline(message_id, chat_id):
    i = message_id - 3
    while i <= message_id:
        try:
            await bot.edit_message_reply_markup(chat_id, i, reply_markup=None)
        except aiogram.exceptions.TelegramBadRequest:
            i += 1
