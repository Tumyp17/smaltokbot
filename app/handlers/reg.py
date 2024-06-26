import random
from aiogram.filters.command import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram import Router, F
# from twilio.rest import Client
from app.filters import userstate
from app.bot_data.botreply import text_messages
from app.keyboards.inline.inline_help import add_help_inline
from app.database import db_users

# This file is used for initial user registration.

router = Router()
router.message.filter(userstate.NoUserIDFilter())


# Creates an Aiogram States Machine state class that is used in multistep registration proccess
class TelCode(StatesGroup):
    entering_tel = State()
    entered_code = State()


# reacts to the cancel command, clears States Machine
@router.message(Command('cancel'))
async def cmd_cancel(message: Message, state: FSMContext):
    db_users.delete_user(message.from_user.id)
    await state.clear()
    await message.answer(text_messages['cancel'])


# Reacts to the /start command and initiates a user registration proccess
@router.message(Command('start'))
async def cmd_start(message: Message, state: FSMContext):
    await message.answer(text_messages['start'])
    await state.set_state(TelCode.entering_tel)


# This handler is entered when users entered his phone number for the first time
# Sends an SMS code to the entered telephone number.
@router.message(F.text, TelCode.entering_tel)
async def enter_tel(message: Message, state: FSMContext):
    await state.update_data(entered_tel=message.text)
    user_data = await state.get_data()
    entered_tel = str(user_data['entered_tel'])
    if entered_tel.isdigit() and len(entered_tel) > 10:
        await state.set_state(TelCode.entered_code)
        await message.answer(text_messages['sms_code'])
        ver_code = str(random.randint(1000, 9999))
        db_users.check_and_add_user(message, ver_code)
#        from config_reader import config
#        Client(config.sid.get_secret_value(),
#               config.token.get_secret_value()).messages.create(from_='+17697570497',
#                                                                body=ver_code, to='+' + message.text)
        await message.answer('TESTMODE__SMS_CODE_IS: ' + ver_code)
        print(ver_code)
    else:
        await message.answer(text_messages['wrong_phone'])
        db_users.delete_user(message.from_user.id)
        await state.clear()


# Handles entered code, checks if it is correct and completes the registration by adding user to database
@router.message(F.text, TelCode.entered_code)
async def check_code(message: Message, state: FSMContext):
    await state.update_data(entered_code=message.text)
    user_data = await state.get_data()
    entered_tel = str(user_data['entered_tel'])
    entered_code = str(user_data['entered_code'])
    ver_code = db_users.get_code(message.from_user.id)
    if entered_code == ver_code:
        await state.clear()
        db_users.db.users.update_one({'user_id': message.from_user.id}, {"$set": {'tel': entered_tel}})
        db_users.db.users.update_one({'user_id': message.from_user.id}, {"$set": {'state': 'verified'}})
        builder = add_help_inline()
        await message.answer(text_messages['successful_reg'], reply_markup=builder.as_markup(resize_keyboard=True))
    else:
        await message.answer(text_messages['wrong_code'])
        db_users.delete_user(message.from_user.id)
        await state.clear()
