import asyncio
from app.keyboards.inline.inline_help import add_help_inline
from app.bot_data.botreply import text_messages
from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.types import Message


async def timeout_callback(current_state, state: FSMContext, callback: types.CallbackQuery):
    await asyncio.sleep(30)
    if await state.get_state() == current_state:
        await state.clear()
        await callback.message.edit_text(text_messages['inactivity_cancel'] + text_messages['restart'])


async def timeout_message(current_state, state: FSMContext, message: Message):
    await asyncio.sleep(30)
    if await state.get_state() == current_state:
        await state.clear()
        builder = add_help_inline()
        reply = text_messages['inactivity_cancel'] + text_messages['help']
        await message.answer(reply, reply_markup=builder.as_markup(resize_keyboard=True))
