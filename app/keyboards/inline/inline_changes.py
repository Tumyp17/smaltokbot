from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

builder = InlineKeyboardBuilder()


builder.add(types.InlineKeyboardButton(
        text='\U0001F1F3 Name',
        callback_data='firstname')
    )
builder.add(types.InlineKeyboardButton(
        text='\U0001F1F8 Surname',
        callback_data='lastname')
    )
builder.add(types.InlineKeyboardButton(
        text='\U0001F4DE Telephone',
        callback_data='tel')
    )
builder.add(types.InlineKeyboardButton(
        text='❌ Cancel',
        callback_data='cancel')
    )
builder.adjust(2)