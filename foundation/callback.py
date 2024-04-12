# IMPORT ----- IMPORT ----- IMPORT ----- IMPORT ----- IMPORT ----- IMPORT ----- IMPORT ----- IMPORT ----- IMPORT ----- I
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot_creation import *
from aiogram import types
from data_project.config import valid_promos

from foundation.keyboards import get_softs_inlinekeyboard
from state_groups import *


# отмена покупки
@dp.callback_query_handler(lambda call: call.data.startswith('cancel_purchase'), state=PaymentStatesGroup.all_states + ClientStatesGroup.all_states + PartnerStatesGroup.all_states)
async def cancel_purchase(callback: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await bot.edit_message_reply_markup(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                                        reply_markup=None)
    await bot.send_message(chat_id=callback.message.chat.id,
                           text="*Покупка была отменена, нажмите на /menu, чтобы вызвать меню*",
                           parse_mode='markdown')
    await callback.answer()


# создание меню софтов
@dp.callback_query_handler(lambda call: call.data.startswith('SOFT'))
async def chosen_soft(callback: types.CallbackQuery):
    # клавиатура подробное описание софта / начало покупки
    b1 = InlineKeyboardButton('Купить', callback_data='buy_request')
    b2 = InlineKeyboardButton('🔺 Назад', callback_data='back_to_soft_menu')
    soft_consideration_markup = InlineKeyboardMarkup()
    soft_consideration_markup.add(b1, b2)

    data_list = data_base.select_software_info(callback.data[4:])[0]
    await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                                text=f'<b><u>Название</u>:</b> {data_list[0]}\n\n<b><u>Описание</u>:</b> {data_list[1]}\n\n<b><u>Цена</u>:</b> {data_list[2]} USDT',
                                parse_mode='html', reply_markup=soft_consideration_markup)


# возвращение в меню софтов
@dp.callback_query_handler(lambda call: call.data.startswith('back_to_soft_menu'))
async def back_from_description_menu(callback: types.CallbackQuery):
    await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                                text='*Выберите софт, чтобы узнать более подробную информацию о нем!*',
                                parse_mode='markdown', reply_markup=get_softs_inlinekeyboard())


# запрос на покупку
@dp.callback_query_handler(lambda call: call.data.startswith('buy_request'))
async def buy_callback(callback: types.CallbackQuery, state: FSMContext):
    await PaymentStatesGroup.promo.set()
    promocode_check_markup = InlineKeyboardMarkup()
    b1 = InlineKeyboardButton('Пропустить', callback_data='skip_promo')
    b2 = InlineKeyboardButton('🔴Отменить покупку🔴', callback_data='cancel_purchase')
    promocode_check_markup.add(b1).add(b2)

    soft_name = callback.message.text.split('\n')[0][10::]
    soft_price = callback.message.text.split('\n')[-1].split()[1]

    async with state.proxy() as data:
        data['soft_name'] = soft_name
        data['soft_price'] = soft_price

    await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                                text='Введите промокод или нажмите "Пропустить"',
                                reply_markup=promocode_check_markup)


# пропустить шаг: промокод
@dp.callback_query_handler(lambda call: call.data.startswith('skip_promo'), state=PaymentStatesGroup.promo)
async def skip_promo(callback: types.CallbackQuery, state: FSMContext):
    await PaymentStatesGroup.receipt.set()
    receipt_markup = InlineKeyboardMarkup()
    b1 = InlineKeyboardButton('Перейти к покупке', callback_data='go_to_purchase')
    b2 = InlineKeyboardButton('🔴Отменить покупку🔴', callback_data='cancel_purchase')
    receipt_markup.add(b1).add(b2)
    async with state.proxy() as data:
        data['soft_promo'] = '-'
    name = data['soft_name']
    price = data[
        'soft_price']  # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                                text=f"<b><u>Название софта:</u> {data['soft_name']}</b>\n"
                                         f"<b><u>Цена софта:</u> {data['soft_price']} USDT</b>\n"
                                         f"<b><u>Скидка промокода:</u> {valid_promos[data['soft_promo']]} USDT\n</b>"
                                         f"",
                                reply_markup=receipt_markup, parse_mode='html')


# добавление промокода пользователя в базу данных
@dp.message_handler(content_types=['text'], state=PaymentStatesGroup.promo)
async def add_promo(message: types.Message, state: FSMContext):
    if message.text in valid_promos:
        await PaymentStatesGroup.receipt.set()
        async with state.proxy() as data:
            data['soft_promo'] = message.text
        receipt_markup = InlineKeyboardMarkup()
        b1 = InlineKeyboardButton('Перейти к покупке', callback_data='go_to_purchase')
        b2 = InlineKeyboardButton('🔴Отменить покупку🔴', callback_data='cancel_purchase')
        receipt_markup.add(b1).add(b2)
        await bot.edit_message_reply_markup(chat_id=message.chat.id, message_id=message.message_id - 1, reply_markup=None)
        await bot.send_message(chat_id=message.chat.id,
                                    text=f"<b><u>Название софта:</u> {data['soft_name']}</b>\n"
                                         f"<b><u>Цена софта:</u> {data['soft_price']} USDT</b>\n"
                                         f"<b><u>Скидка промокода:</u> {valid_promos[data['soft_promo']]} USDT\n</b>"
                                         f"",
                                    reply_markup=receipt_markup, parse_mode='html')
    else:
        promocode_check_markup = InlineKeyboardMarkup()
        b1 = InlineKeyboardButton('Пропустить', callback_data='skip_promo')
        b2 = InlineKeyboardButton('🔴Отменить покупку🔴', callback_data='cancel_purchase')
        promocode_check_markup.add(b1).add(b2)
        await bot.edit_message_reply_markup(chat_id=message.chat.id, message_id=message.message_id-1, reply_markup=None)
        await bot.send_message(chat_id=message.chat.id,
                                    text='<b>❗️Промокод недействителен, попробуйте ввести другой или нажмите "Пропустить"❗️</b>',
                                    parse_mode='html', reply_markup=promocode_check_markup)


# подтверждение транзакции
@dp.callback_query_handler(state=PaymentStatesGroup.receipt)
async def skip_promo(callback: types.CallbackQuery, state: FSMContext):
    await PaymentStatesGroup.transaction.set()
    transaction_markup = InlineKeyboardMarkup()
    b1 = InlineKeyboardButton('🔴Отменить покупку🔴', callback_data='cancel_purchase')
    transaction_markup.add(b1)
    async with state.proxy() as data:
        pass
    name = data['soft_name']
    price = data['soft_price'] # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                                text=f"Отправьте {price} USDT по адресу: XXXXXXXXXXXXXXXXXXXXX. После отправьте "
                                     f"сообщение с хэшом транзакзции для подтверждения",
                                reply_markup=transaction_markup)


# транзакция подтверждена
@dp.message_handler(state=PaymentStatesGroup.transaction)
async def transaction_check(message: types.Message, state: FSMContext):
    if True:
        await PaymentStatesGroup.github_request.set()
        async with state.proxy() as data:
            data['transaction_hash'] = message.text
        await bot.edit_message_reply_markup(chat_id=message.chat.id, message_id=message.message_id - 1,
                                            reply_markup=None)
        await bot.send_message(chat_id=message.chat.id,
                               text="*Транзакция была успешно подтверждена, пришлите свой гитхаб для выдачи доступа к софту.*",
                               parse_mode='markdown')
    else:
        pass


# закрытие покупки
@dp.message_handler(state=PaymentStatesGroup.github_request)
async def transaction_check(message: types.Message, state: FSMContext):
    if True:
        async with state.proxy() as data:
            data['github'] = message.text
        await bot.send_message(chat_id=message.chat.id,
                               text="*Доступ к софту будет предоставлен в ближайшее время, спасибо за покупку!\n"
                                    "\n"
                                    "Чтобы вы хотите посмотреть другие софты нажмите на /menu.*",
                               parse_mode='markdown')

        await bot.send_message(chat_id='868320310', text=f"*🟢БЫЛА СОВЕРШЕНА ПОКУПКА🟢\nСофт: {data['soft_name']}\n"
                                                         f"Цена: {data['soft_price']} USDT\n"
                                                         f"Скидка промокода: {valid_promos[data['soft_promo']]} USDT   Промо: {data['soft_promo']}\n"
                                                         f"Реферал: {'-'}\n"
                                                         f"Ник покупателя: {message.from_user.first_name} {message.from_user.last_name}\n"
                                                         f"Хэш-транзакции: {data['transaction_hash']}\n"
                                                         f"Github: {data['github']}\n*", parse_mode='markdown')

        await state.finish()
    else:
        pass