from aiogram import Router
from app.bot_data import botreply
from aiogram.types import Message
from app.filters import userstate

router = Router()
router.message.filter(userstate.NoUserIDFilter())


@router.message()
async def cmd_start(message: Message):
    await message.answer(botreply.text_messages['not_reg'])
