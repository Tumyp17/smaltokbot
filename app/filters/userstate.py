from typing import Union, Dict, Any
from aiogram.filters import BaseFilter
from aiogram.types import Message
from app.database.db_users import get_current_state, db
from aiogram.fsm.context import FSMContext

us = db.users


class HasUserIDFilter(BaseFilter):
    async def __call__(self, message: Message) -> Union[bool, Dict[str, Any]]:
        if (us.find_one({'user_id': message.from_user.id}) is not None
                and get_current_state(message.from_user.id) == 'verified'):
            return True
        else:
            return False


class NoUserIDFilter(BaseFilter):
    async def __call__(self, message: Message) -> Union[bool, Dict[str, Any]]:
        if us.find_one({'user_id': message.from_user.id}) is None:
            return True
        elif get_current_state(message.from_user.id) == 'null':
            return True
        else:
            return False


class ChangeNumFilter(BaseFilter):
    async def __call__(self, message: Message) -> Union[bool, Dict[str, Any]]:
        user_id = message.from_user.id
        if us.find_one({'user_id': user_id}) is None or get_current_state(user_id) == 'new_num':
            return True
        else:
            return False


class NoStateFilter(BaseFilter):
    async def __call__(self, message: Message, state: FSMContext) -> Union[bool, Dict[str, Any]]:
        if await state.get_state() is None:
            return True
        else:
            return False
