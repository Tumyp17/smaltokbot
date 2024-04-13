from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

# Creats a buttons layout for general cancel button

builder = InlineKeyboardBuilder()


builder.add(types.InlineKeyboardButton(
        text='❌ Cancel',
        callback_data='cancel')
    )
builder.adjust(2)
