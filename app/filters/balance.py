from typing import Union, Dict, Any

from aiogram.filters import BaseFilter
from aiogram.types import Message
from app.database import db_users


class BalanceFilter(BaseFilter):
    async def __call__(self, message: Message) -> Union[bool, Dict[str, Any]]:
        if int(db_users.get_balance(message.from_user.id)) >= 29:
            return True
        else:
            return False


class NoBalanceFilter(BaseFilter):
    async def __call__(self, message: Message) -> Union[bool, Dict[str, Any]]:
        if int(db_users.get_balance(message.from_user.id)) < 30:
            return True
        else:
            return False
