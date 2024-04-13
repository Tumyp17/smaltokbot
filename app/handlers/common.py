from aiogram.filters.command import Command
from aiogram import Bot, Router, F, types
from aiogram.types import Message
from app.database import db_users
from app.keyboards.inline import inline_balance, inline_profile
from app.bot_data.botreply import text_messages
from app.functions.remove_inline_func import remove_inline
from app.keyboards.inline.inline_help import add_help_inline
from app.filters.userstate import NoStateFilter, HasUserIDFilter
from config_reader import config

bot = Bot(token=config.bot_token.get_secret_value())
router = Router()
router.message.filter(HasUserIDFilter())


# A handler that reacts to help callback
@router.callback_query(F.data == 'help')
async def cmd_help(callback: types.CallbackQuery):
    help_inline = add_help_inline()
    await callback.message.edit_text(text_messages['help'], reply_markup=help_inline.as_markup(resize_keyboard=True))


# Reacts to balance callback
@router.callback_query(F.data == 'balance')
async def cmd_balance(callback: types.CallbackQuery):
    balance = str(db_users.get_balance(callback.from_user.id))
    reply = 'Your balance is: ' + balance
    await callback.message.edit_text(reply, reply_markup=inline_balance.builder.as_markup(resize_keyboard=True))


# Reacts to profile callback
@router.callback_query(F.data == 'profile')
async def cmd_profile(callback: types.CallbackQuery):
    reply = ('Your profile\nName - ' + db_users.get_first_name(callback.from_user.id) + '\n'
             'Surname - ' + db_users.get_last_name(callback.from_user.id) + '\n'
             'Telephone - ' + db_users.get_tel(callback.from_user.id) +
             '\n\nThe data above has been received from your Telegram profile,\n or it has been acquired from you')
    await callback.message.edit_text(reply, reply_markup=inline_profile.builder.as_markup(resize_keyboard=True))


@router.message(Command('delete'))
async def cmd_delete(message: Message):
    await db_users.delete_user(message.from_user.id)
    await message.answer("Your profile has been deleted")


# Reacts to /start command
@router.message(F or Command('start'), NoStateFilter())
async def cmd_start(event: Message or types.CallbackQuery):
    await remove_inline(event.message_id, event.from_user.id)
    builder = add_help_inline()
    await event.answer(text_messages['help'], reply_markup=builder.as_markup(resize_keyboard=True))
