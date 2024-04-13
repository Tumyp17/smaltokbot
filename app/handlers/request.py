import requests
from aiogram import Router, F, types
from aiogram.types import Message
from aiogram.filters.command import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from app.database import db_users
from app.filters import userstate, balance
from app.bot_data.botreply import text_messages
from app.keyboards.inline import inline_request, inline_cancel, inline_balance
from app.keyboards.inline.inline_help import add_help_inline
from app.functions.remove_inline_func import remove_inline


# This file is used for handling users requests.

router = Router()
router.message.filter(userstate.HasUserIDFilter())  # Checking if user is registred


# Creates an Aiogram States Machine class
class RequestType(StatesGroup):
    choosing_request_type = State()
    request_help = State()
    support = State()


# Handles a /cancel command
@router.message(Command('cancel'))
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    builder = add_help_inline()
    await message.answer(text_messages['cancel'], reply_markup=builder.as_markup(resize_keyboard=True))


# Handles a support callback, asks user for additional info for a support team
@router.callback_query(F.data == 'support')
async def cmd_request(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text_messages['support_msg'], reply_markup=inline_cancel.builder.as_markup())
    await state.set_state(RequestType.support)


# Handles an additional info from user and sends a support request to CRM
@router.message(F.text, RequestType.support)
async def send_support(message: Message, state: FSMContext):
    await state.update_data(support_text=message.text.lower())
    bitrix_url = db_users.get_bx_url_assistance(message, 'SUPPORT')
    requests.get(bitrix_url)
    builder = add_help_inline()
    await message.answer(text_messages['successful_request'], reply_markup=builder.as_markup(resize_keyboard=True))
    await remove_inline(message.message_id, message.from_user.id)
    await state.clear()


# Handles a request callback. Condition - user has not enough funds. Sends a related info message to a user.
@router.callback_query(F.data == 'request', balance.NoBalanceFilter())
async def cmd_request_no(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text_messages['no_funds'],
                                     reply_markup=inline_balance.builder.as_markup(resize_keyboard=True))
    await state.clear()


# Handles a request callback. Condition - user has enough funds. Asks user which service he needs.
@router.callback_query(F.data == 'request', balance.BalanceFilter())
async def cmd_request(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text_messages['request_msg'],
                                     reply_markup=inline_request.builder.as_markup(resize_keyboard=True))
    await state.set_state(RequestType.choosing_request_type)


# Handles users request type (translate/assistance callbacks).
# If user has chosen translate - sends a request to CRM
# If user has chosen assistance - asks for an additional information
@router.callback_query(F.data, RequestType.choosing_request_type)
async def send_request(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(chosen_request=callback.data)
    user_data = await state.get_data()
    chosen_request = str(user_data['chosen_request'])
    if chosen_request.lower() == 'translate':
        bitrix_url = db_users.get_bx_url(callback, '!ASSISTANT_TRANSLATION!')
        requests.get(bitrix_url)
        builder = add_help_inline()
        reply = text_messages['successful_request']
        await callback.message.edit_text(reply, reply_markup=builder.as_markup(resize_keyboard=True))
        await state.clear()
    elif chosen_request.lower() == 'assistance':
        from app.keyboards.inline.inline_cancel import builder
        await callback.message.edit_text(text_messages['specify_request'],
                                         reply_markup=builder.as_markup())
        await state.set_state(RequestType.request_help)


# Handles users additional information (assistance callback related) and sends it to the CRM.
@router.message(F.text, RequestType.request_help)
async def help_request(message: Message, state: FSMContext):
    await state.update_data(help_msg=message.text.lower())
    bitrix_url = db_users.get_bx_url_assistance(message, 'HELP')
    requests.get(bitrix_url)
    builder = add_help_inline()
    await message.answer(text_messages['successful_request'], reply_markup=builder.as_markup(resize_keyboard=True))
    await remove_inline(message.message_id, message.from_user.id)
    await state.clear()
