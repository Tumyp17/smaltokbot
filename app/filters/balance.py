from typing import Union, Dict, Any

from aiogram.filters import BaseFilter
from aiogram.types import Message
from app.database import db_users


# A filter that returns True or False depending on the users balance
class BalanceFilter(BaseFilter):
    async def __call__(self, message: Message) -> Union[bool, Dict[str, Any]]:
        if int(db_users.get_balance(message.from_user.id)) >= 29:
            return True
        else:
            return False


# Another filter that returns True or False depending on the users balance.
# Second filter is required for different services types (some of them are more expensive than others)
class NoBalanceFilter(BaseFilter):
    async def __call__(self, message: Message) -> Union[bool, Dict[str, Any]]:
        if int(db_users.get_balance(message.from_user.id)) < 30:
            return True
        else:
            return False
