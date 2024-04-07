from aiogram.fsm.context import FSMContext
from aiogram import Router, F, types
from app.database import db_users
from app.keyboards.inline.inline_help import add_help_inline
from app.bot_data.botreply import text_messages

router = Router()


@router.callback_query(F.data == 'cancel')
async def cmd_cancel(callback: types.CallbackQuery, state: FSMContext):
    db_users.db.users.update_one({'user_id': callback.from_user.id}, {"$set": {'state': 'verified'}})
    await state.clear()
    builder = add_help_inline()
    await callback.message.edit_text(text_messages['cancel'] + text_messages['help'],
                                     reply_markup=builder.as_markup(resize_keyboard=True))
