from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

# Creats a buttons layout for profile callback

builder = InlineKeyboardBuilder()

builder.add(types.InlineKeyboardButton(
        text='\U0001F519 Back',
        callback_data='help')
    )
builder.add(types.InlineKeyboardButton(
        text='\U0001F4DD Changе',
        callback_data='changes')
    )
builder.adjust(1)
