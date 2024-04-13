import asyncio
from aiogram import types


# This function deletes a bot message. Used for timeout requests.
async def delete_message(message: types.Message, sleep_time: int = 0):
    await asyncio.sleep(sleep_time)
    await message.delete()
