from aiogram.filters.command import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram import Router, F, types
from app.database import db_users
from app.bot_data import botreply
from app.keyboards.inline.inline_help import add_help_inline
from app.filters import userstate
from app.functions import timeout_func
from app.functions.remove_inline_func import remove_inline
from config_reader import config
from app.bot_data.botreply import text_messages


# This file is used for balance topup

router = Router()
router.message.filter(userstate.HasUserIDFilter())  # checks if user is registred


# Creates an Aiogram Machine State class for multistep proccess
class TopUp(StatesGroup):
    choosing_topup_amount = State()
    succesful_payment = State()


# Handles /cancel command
@router.message(Command('cancel'))
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await remove_inline(message.message_id, message.from_user.id)
    builder = add_help_inline()
    await message.answer('Action canceled', reply_markup=builder.as_markup(resize_keyboard=True))


# Handles users request to cancel paymen (cancel_payment callback)
@router.callback_query(F.data == 'cancel_payment')
async def cmd_cancel(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.delete()


# Handles topup callback. Asks for the amount that user wnats to topup.
@router.callback_query(F.data == 'topup')
async def cmd_topup(callback: types.CallbackQuery, state: FSMContext):
    from app.keyboards.inline.inline_cancel import builder
    await callback.message.edit_text(text_messages["topup_summ"], reply_markup=builder.as_markup(resize_keyboard=True))
    await state.set_state(TopUp.choosing_topup_amount)
    await timeout_func.timeout_callback(TopUp.choosing_topup_amount, state, callback)


# Handles the entered topup summ. Checks if amount is correct and sends a payment api link.
@router.message(TopUp.choosing_topup_amount)
async def topup_entered(message: Message, state: FSMContext):
    await remove_inline(message.message_id, message.from_user.id)
    await state.update_data(chosen_summ=message.text)
    user_data = await state.get_data()
    chosen_summ = user_data['chosen_summ']
    if chosen_summ is not None and chosen_summ.isdigit() and chosen_summ[0] != '0' and int(chosen_summ) >= 100:
        from aiogram import Bot
        bot = Bot(token=config.bot_token.get_secret_value())
        amount_topup = int(chosen_summ) * 100
        price = types.LabeledPrice(label="Balance topup", amount=amount_topup)
        from app.keyboards.inline.inline_cancel_payment import builder
        await message.answer("THIS IS A TEST PAYMENT. TEST CARD DETAILS: 1111 1111 1111 1026 12/22 000")
        await bot.send_invoice(message.chat.id,
                               title="Balance topup",
                               description="Your balance topup",
                               provider_token=config.payment_token.get_secret_value(),
                               currency="rub",
                               photo_width=416,
                               photo_height=234,
                               photo_size=416,
                               is_flexible=False,
                               prices=[price],
                               start_parameter="one-month-subscription",
                               payload="test-invoice-payload")
    else:
        builder = add_help_inline()
        await message.answer(botreply.text_messages['wrong_typo_balance'],
                             reply_markup=builder.as_markup(resize_keyboard=True))
        await state.clear()


# Checks if payment has been completed
@router.pre_checkout_query(lambda query: True)
async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery, state: FSMContext):
    from aiogram import Bot
    bot = Bot(token=config.bot_token.get_secret_value())
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)
    await state.set_state(TopUp.succesful_payment)


# If payment was successful sends a related message
@router.message(TopUp.succesful_payment)
async def successful_payment(message: types.Message, state: FSMContext):
    new_balance = int(db_users.get_balance(message.from_user.id)) + message.successful_payment.total_amount // 100
    db_users.topup(message.from_user.id, new_balance)
    reply = botreply.text_messages['topup'] + '\nBalance: ' + str(new_balance)
    builder = add_help_inline()
    await message.answer(f"Payment in the amount of {message.successful_payment.total_amount // 100} "
                         f"{message.successful_payment.currency} is successful")
    await message.answer(reply, reply_markup=builder.as_markup(resize_keyboard=True))
    await state.clear()
