from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder


def add_help_inline():
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
            text='\U0001F4AC Services',
            callback_data='request')
        )
    builder.add(types.InlineKeyboardButton(
            text='\U0001F4B0 Balance',
            callback_data='balance')
        )
    builder.add(types.InlineKeyboardButton(
            text='\U0001F464 Profile',
            callback_data='profile')
        )
    builder.add(types.InlineKeyboardButton(
            text='\U0001F4E9 Support',
            callback_data='support')
        )
    builder.adjust(2)
    return builder


def remove_help_inline():
    builder = InlineKeyboardBuilder()
    return builder
