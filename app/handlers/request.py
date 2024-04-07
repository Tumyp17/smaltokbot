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

router = Router()
router.message.filter(userstate.HasUserIDFilter())


class RequestType(StatesGroup):
    choosing_request_type = State()
    request_help = State()
    support = State()


@router.message(Command('cancel'))
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    builder = add_help_inline()
    await message.answer('Действие отменено', reply_markup=builder.as_markup(resize_keyboard=True))


@router.callback_query(F.data == 'support')
async def cmd_request(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text_messages['support_msg'], reply_markup=inline_cancel.builder.as_markup())
    await state.set_state(RequestType.support)


@router.message(F.text, RequestType.support)
async def send_support(message: Message, state: FSMContext):
    await state.update_data(support_text=message.text.lower())
    bitrix_url = db_users.get_bx_url_assistance(message, 'ПОДДЕРЖКА')
    requests.get(bitrix_url)
    builder = add_help_inline()
    await message.answer(text_messages['successful_request'], reply_markup=builder.as_markup(resize_keyboard=True))
    await remove_inline(message.message_id, message.from_user.id)
    await state.clear()


@router.callback_query(F.data == 'request', balance.NoBalanceFilter())
async def cmd_request_no(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text_messages['no_funds'],
                                     reply_markup=inline_balance.builder.as_markup(resize_keyboard=True))
    await state.clear()


@router.callback_query(F.data == 'request', balance.BalanceFilter())
async def cmd_request(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text_messages['request_msg'],
                                     reply_markup=inline_request.builder.as_markup(resize_keyboard=True))
    await state.set_state(RequestType.choosing_request_type)


@router.callback_query(F.data, RequestType.choosing_request_type)
async def send_request(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(chosen_request=callback.data)
    user_data = await state.get_data()
    chosen_request = str(user_data['chosen_request'])
    if chosen_request.lower() == 'translate':
        bitrix_url = db_users.get_bx_url(callback, '!СИНХРОННЫЙ_ПЕРЕВОД!')
        requests.get(bitrix_url)
        builder = add_help_inline()
        reply = text_messages['successful_request']
        await callback.message.edit_text(reply, reply_markup=builder.as_markup(resize_keyboard=True))
        await state.clear()
    elif chosen_request.lower() == 'assistance':
        from app.keyboards.inline.inline_cancel import builder
        await callback.message.edit_text('Уточните, какую задачу необходимо выполнить нашему специалисту.',
                                         reply_markup=builder.as_markup())
        await state.set_state(RequestType.request_help)


@router.message(F.text, RequestType.request_help)
async def help_request(message: Message, state: FSMContext):
    await state.update_data(help_msg=message.text.lower())
    bitrix_url = db_users.get_bx_url_assistance(message, 'ПОМОЩЬ')
    requests.get(bitrix_url)
    builder = add_help_inline()
    await message.answer(text_messages['successful_request'], reply_markup=builder.as_markup(resize_keyboard=True))
    await remove_inline(message.message_id, message.from_user.id)
    await state.clear()
