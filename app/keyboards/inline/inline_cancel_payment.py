from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder


# Creats a buttons layout for payment cancelation


builder = InlineKeyboardBuilder()


builder.add(types.InlineKeyboardButton(
        text='❌ Cancel',
        callback_data='cancel_payment')
    )
builder.adjust(2)
