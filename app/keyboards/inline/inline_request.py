from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

# Creats a buttons layout for user request callback

builder = InlineKeyboardBuilder()


builder.add(types.InlineKeyboardButton(
        text='🈳 Translation',
        callback_data='translate')
    )
builder.add(types.InlineKeyboardButton(
        text='💁 Assistant',
        callback_data='assistance')
    )
builder.add(types.InlineKeyboardButton(
        text='❌ Back',
        callback_data='cancel')
    )

builder.adjust(2)
