from aiogram import BaseMiddleware
from app.database import db_updates
from aiogram.types import Message
from typing import Callable, Dict, Any, Awaitable
from datetime import datetime


class UpdatesMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        db_updates.add_update(event)
        seconds = db_updates.get_seconds(event.from_user.id, event.message_id)
        current_seconds = (datetime.now() - datetime(1, 1, 1, 0, 0)).total_seconds()
        seconds_range = int(float(current_seconds - seconds))
        if not seconds:
            pass
        elif seconds_range >= 2:
            return await handler(event, data)
        else:
            pass
