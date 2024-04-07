import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config_reader import config
from app.middlewares.add_update import UpdatesMiddleware
# from app.middlewares.add_update_callback import UpdatesMiddlewareCallback
from app.handlers import common, topup, reg, no_user, changes, request


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    dp = Dispatcher(storage=MemoryStorage())
    bot = Bot(token=config.bot_token.get_secret_value())

    dp.message.outer_middleware(UpdatesMiddleware())
    #   dp.message.outer_middleware(UpdatesMiddlewareCallback())

    dp.include_router(common.router)
    dp.include_router(topup.router)
    dp.include_router(reg.router)
    dp.include_router(no_user.router)
    dp.include_router(changes.router)
    dp.include_router(request.router)

    await dp.start_polling(bot, skip_updates=False)


if __name__ == "__main__":
    asyncio.run(main())
