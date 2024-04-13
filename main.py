import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config_reader import config
from app.middlewares.add_update import UpdatesMiddleware
# from app.middlewares.add_update_callback import UpdatesMiddlewareCallback
from app.handlers import common, topup, reg, no_user, changes, request


# A main file that is used to initialize dispatcher, add routers and middlwars. This file is used for starting this bot.
# main.py should be accessed only from the current directory. Otherwise, it will send an error (due to the pydotenv).


# Enabling logging
async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    # Initialazing dispacher
    dp = Dispatcher(storage=MemoryStorage())
    # Getting a bot token. Bot initializing.
    bot = Bot(token=config.bot_token.get_secret_value())

    # Updates middlware initializing
    dp.message.outer_middleware(UpdatesMiddleware())
    #   dp.message.outer_middleware(UpdatesMiddlewareCallback())

    # Initializing routers
    dp.include_router(common.router)
    dp.include_router(topup.router)
    dp.include_router(reg.router)
    dp.include_router(no_user.router)
    dp.include_router(changes.router)
    dp.include_router(request.router)

    # Starting bot polling proccess
    await dp.start_polling(bot, skip_updates=False)


# Checks if the file name is main and runs the main functions. Code starts here.
if __name__ == "__main__":
    asyncio.run(main())
