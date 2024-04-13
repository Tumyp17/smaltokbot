from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

# Creats a buttons layout for topup

builder = InlineKeyboardBuilder()


builder.add(types.InlineKeyboardButton(
        text='\U0001F519 Back',
        callback_data='help')
    )
builder.add(types.InlineKeyboardButton(
        text='\U0001F4B0 Top Up',
        callback_data='topup'))
builder.adjust(2)
