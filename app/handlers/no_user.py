from aiogram import Router
from app.bot_data import botreply
from aiogram.types import Message
from app.filters import userstate

router = Router()
router.message.filter(userstate.NoUserIDFilter())  # filters in any not registred user


# Reacts to any update from a not registred user
@router.message()
async def cmd_start(message: Message):
    await message.answer(botreply.text_messages['not_reg'])
