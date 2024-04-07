from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

builder = InlineKeyboardBuilder()


builder.add(types.InlineKeyboardButton(
        text='Help',
        callback_data='help')
    )
builder.add(types.InlineKeyboardButton(
        text='Top Up',
        callback_data='topup')
    )
builder.add(types.InlineKeyboardButton(
        text='Balance',
        callback_data='balance')
    )
builder.add(types.InlineKeyboardButton(
        text='Request',
        callback_data='request')
    )
builder.add(types.InlineKeyboardButton(
        text='Your profile',
        callback_data='profile')
    )
builder.add(types.InlineKeyboardButton(
        text='Change data',
        callback_data='changes')
    )
builder.add(types.InlineKeyboardButton(
        text='Support',
        callback_data='support')
    )
builder.adjust(2)
