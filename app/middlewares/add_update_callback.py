from aiogram import BaseMiddleware
from app.database import db_updates
from aiogram.types import CallbackQuery
from typing import Callable, Dict, Any, Awaitable
from datetime import datetime


# This file is used fot outer middlware that adds all users callback updates to the MongoDB

class UpdatesMiddlewareCallback(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        event: CallbackQuery,
        data: Dict[str, Any]
    ) -> Any:
        db_updates.add_update_callback(event)
        seconds = db_updates.get_seconds(event.from_user.id, event.callback_id)
        current_seconds = (datetime.now() - datetime(1, 1, 1, 0, 0)).total_seconds()
        seconds_range = int(float(current_seconds - seconds))
        if not seconds and seconds_range >= 5:
            return await handler(event, data)
        else:
            pass
