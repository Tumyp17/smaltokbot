import random
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram import Router, F, types
from twilio.rest import Client
from app.database import db_users
from app.filters import userstate
from app.bot_data.botreply import text_messages  # , config
from app.keyboards.inline import inline_changes, inline_cancel
from app.keyboards.inline.inline_help import add_help_inline
from app.functions import timeout_func
from app.functions.remove_inline_func import remove_inline

router = Router()


class NameSurnameTel(StatesGroup):
    choosing_whatto_change = State()
    entering_name = State()
    entering_surname = State()
    entering_tel = State()
    entered_code = State()


@router.callback_query(F.data == 'cancel')
async def cmd_cancel(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    builder = add_help_inline()
    await callback.message.edit_text(text_messages['cancel'] + text_messages['help'],
                                     reply_markup=builder.as_markup(resize_keyboard=True))


@router.callback_query(F.data == 'changes', userstate.HasUserIDFilter())
async def cmd_change(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text_messages['changes_question'],
                                     reply_markup=inline_changes.builder.as_markup(resize_keyboard=True))
    await state.set_state(NameSurnameTel.choosing_whatto_change)
    await timeout_func.timeout_callback(NameSurnameTel.choosing_whatto_change, state, callback)


@router.callback_query(F.data, NameSurnameTel.choosing_whatto_change)
async def changes_chosen(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(chosen_datato_change=callback.data)
    user_data = await state.get_data()
    chosen_datato_change = user_data['chosen_datato_change']
    if chosen_datato_change == 'firstname':
        await state.set_state(NameSurnameTel.entering_name)
        await callback.message.edit_text(text_messages['name_request'], reply_markup=inline_cancel.builder.as_markup())
        await timeout_func.timeout_callback(NameSurnameTel.entering_name, state, callback)
    elif chosen_datato_change == 'lastname':
        await state.set_state(NameSurnameTel.entering_surname)
        await callback.message.edit_text(text_messages['surname_request'], reply_markup=inline_cancel.builder.as_markup())
        await timeout_func.timeout_callback(NameSurnameTel.entering_surname, state, callback)
    elif chosen_datato_change == 'tel':
        await callback.message.edit_text(text_messages['change_tel'], reply_markup=inline_cancel.builder.as_markup())
        await state.set_state(NameSurnameTel.entering_tel)
        await timeout_func.timeout_callback(NameSurnameTel.entering_tel, state, callback)
    else:
        builder = add_help_inline()
        await callback.message.edit_text(text_messages['cancel'],
                                         reply_markup=builder.as_markup(resize_keyboard=True))


@router.message(F.text, NameSurnameTel.entering_name)
async def change_name(message: Message, state: FSMContext):
    await state.update_data(entered_name=message.text)
    user_data = await state.get_data()
    entered_name = str(user_data['entered_name'])
    db_users.db.users.update_one({'user_id': message.from_user.id}, {"$set": {'first_name': entered_name}})
    builder = add_help_inline()
    await message.answer(text_messages['profile_updated'], reply_markup=builder.as_markup(resize_keyboard=True))
    await remove_inline(message.message_id, message.from_user.id)
    await state.clear()


@router.message(F.text, NameSurnameTel.entering_surname)
async def change_surname(message: Message, state: FSMContext):
    await state.update_data(entered_surname=message.text)
    user_data = await state.get_data()
    entered_surname = str(user_data['entered_surname'])
    db_users.db.users.update_one({'user_id': message.from_user.id}, {"$set": {'last_name': entered_surname}})
    builder = add_help_inline()
    await message.answer(text_messages['profile_updated'], reply_markup=builder.as_markup(resize_keyboard=True))
    await remove_inline(message.message_id, message.from_user.id)
    await state.clear()


@router.message(F.text, NameSurnameTel.entering_tel)
async def change_tel(message: Message, state: FSMContext):
    await state.update_data(entered_tel=message.text)
    user_data = await state.get_data()
    entered_tel = str(user_data['entered_tel'])
    if entered_tel.isdigit() and len(entered_tel) > 10:
        await state.set_state(NameSurnameTel.entered_code)
        ver_code = str(random.randint(1000, 9999))
        db_users.db.users.update_one({'user_id': message.from_user.id}, {"$set": {'code': ver_code}})
        await remove_inline(message.message_id, message.from_user.id)
        from config_reader import config
        Client(config.sid.get_secret_value(),
               config.token.get_secret_value()).messages.create(from_='+17697570497',
                                                                body=ver_code, to='+' + message.text)
        await message.answer(text_messages['sms_code'], reply_markup=inline_cancel.builder.as_markup())
        await message.answer('TESTMODE__SMS_CODE_IS: ' + ver_code)
        await timeout_func.timeout_message(NameSurnameTel.entered_code, state, message)
    else:
        await state.clear()
        builder = add_help_inline()
        await message.answer('Вы ввели некорректный номер телефона, для повторной попытки нажмите Изменить данные',
                             reply_markup=builder.as_markup(resize_keyboard=True))


@router.message(F.text, NameSurnameTel.entered_code)
async def check_code(message: Message, state: FSMContext):
    await state.update_data(entered_code=message.text)
    user_data = await state.get_data()
    entered_code = str(user_data['entered_code'])
    entered_tel = user_data['entered_tel']
    ver_code = db_users.get_code(message.from_user.id)
    if entered_code == ver_code:
        db_users.db.users.update_one({'user_id': message.from_user.id}, {"$set": {'tel': entered_tel}})
        builder = add_help_inline()
        await message.answer('Ваш номер телефона изменен на: ' + entered_tel,
                             reply_markup=builder.as_markup(resize_keyboard=True))
        await state.clear()
    else:
        builder = add_help_inline()
        await message.answer('Вы ввели неверный код, для повторной попытки нажмите Изменить данные',
                             reply_markup=builder.as_markup(resize_keyboard=True))
        await state.clear()
