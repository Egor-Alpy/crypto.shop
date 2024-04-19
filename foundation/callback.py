# IMPORT ----- IMPORT ----- IMPORT ----- IMPORT ----- IMPORT ----- IMPORT ----- IMPORT ----- IMPORT ----- IMPORT ----- I
import datetime

from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from data_project.data_base import *

from bot_creation import *
from aiogram import types

from data_project.text import MSG

from foundation.keyboards import get_softs_inlinekeyboard
from state_groups import *

from web3 import Web3
from web3.types import HexStr

# отмена покупки
@dp.callback_query_handler(lambda call: call.data.startswith('cancel_purchase'),
                           state=PaymentStatesGroup.all_states + ClientStatesGroup.all_states + PartnerStatesGroup.all_states)
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
                                text=MSG['RUS']['SOFT_MENU'],
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
        data['description_message_id'] = callback.message.message_id
    await bot.edit_message_reply_markup(message_id=callback.message.message_id, chat_id=callback.message.chat.id,
                                        reply_markup=None)
    await bot.send_message(chat_id=callback.message.chat.id,
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
        data['price_promo'] = str(float(data['soft_price']) - 0)
        data['promo_discount'] = 0
    name = data['soft_name']
    price_with_promo = float(data['soft_price']) - 0
    await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                                text=f"<b><u>Название софта:</u> {name}</b>\n"
                                     f"<b><u>Цена софта:</u> {price_with_promo} USDT</b>\n"
                                     f"<b><u>Скидка промокода:</u> {0} USDT\n</b>"
                                     f"",
                                reply_markup=receipt_markup, parse_mode='html')


# добавление промокода пользователя в базу данных
@dp.message_handler(content_types=['text'], state=PaymentStatesGroup.promo)
async def add_promo(message: types.Message, state: FSMContext):
    valid_promos = data_base.select_promos()
    if message.text in valid_promos:
        promo_discount = data_base.select_promo_discount(message.text)
        await PaymentStatesGroup.receipt.set()
        async with state.proxy() as data:
            data['soft_promo'] = message.text
            data['price_promo'] = str(float(data['soft_price']) - promo_discount)
            data['promo_discount'] = promo_discount
        receipt_markup = InlineKeyboardMarkup()
        b1 = InlineKeyboardButton('Перейти к покупке', callback_data='go_to_purchase')
        b2 = InlineKeyboardButton('🔴Отменить покупку🔴', callback_data='cancel_purchase')
        receipt_markup.add(b1).add(b2)
        await bot.edit_message_reply_markup(chat_id=message.chat.id, message_id=message.message_id - 1,
                                            reply_markup=None)
        price_with_promo = float(data['soft_price']) - promo_discount
        await bot.send_message(chat_id=message.chat.id,
                               text=f"<b><u>Название софта:</u> {data['soft_name']}</b>\n"
                                    f"<b><u>Цена софта:</u> {price_with_promo} USDT</b>\n"
                                    f"<b><u>Скидка промокода:</u> {promo_discount} USDT\n</b>"
                                    f"",
                               reply_markup=receipt_markup, parse_mode='html')
    else:
        promocode_check_markup = InlineKeyboardMarkup()
        b1 = InlineKeyboardButton('Пропустить', callback_data='skip_promo')
        b2 = InlineKeyboardButton('🔴Отменить покупку🔴', callback_data='cancel_purchase')
        promocode_check_markup.add(b1).add(b2)
        await bot.edit_message_reply_markup(chat_id=message.chat.id, message_id=message.message_id - 1,
                                            reply_markup=None)
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
    price_with_promo = float(data['soft_price']) - data['promo_discount']
    await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                                text=f"Отправьте {price_with_promo} USDT по адресу: XXXXXXXXXXXXXXXXXXXXX. После отправьте "
                                     f"сообщение с хэшом транзакзции для подтверждения",
                                reply_markup=transaction_markup)


# транзакция подтверждена
@dp.message_handler(state=PaymentStatesGroup.transaction)
async def transaction_check(message: types.Message, state: FSMContext):
    flag = False

    async with state.proxy() as data:
        pass

    chat_id = message.chat.id

    tx_hash = HexStr(message.text)  # '0xd3a08bbe68b8949ea43a76b5720914dcdaebc2b47b69d006af976aa84d5c9752'
    con_web3 = Web3(provider=Web3.HTTPProvider(endpoint_uri='https://rpc.ankr.com/eth'))

    USDT_CONTRACT_ADRESS = '0xdAC17F958D2ee523a2206206994597C13D831ec7'
    RECEIVER = '' # const

    tx_data = con_web3.eth.wait_for_transaction_receipt(transaction_hash=tx_hash, timeout=1000)

    tx_exists = tx_data['status']
    tx_contract = tx_data['to']  # адрес контракта\получателя?
    tx_receiver = tx_data['logs']['????']  # как вытащить получателя
    tx_coin_qty = tx_data['logs']['?????']  # как вытащить кол-во монет

    if tx_contract != USDT_CONTRACT_ADRESS:
        bot.send_message(chat_id=chat_id, text='Некорректный адрес смарт-контракта')

    elif tx_receiver != RECEIVER:
        bot.send_message(chat_id=chat_id, text='Неверно указан адрес получателя')

    elif tx_coin_qty < data['price_promo']:
        bot.send_message(chat_id=chat_id, text='Вы перевели недостаточное кол-во средств')

    elif tx_exists != 1:
        bot.send_message(chat_id=chat_id, text='Ошибка транзакции')

    elif tx_hash in data_base:
        bot.send_message(chat_id=chat_id, text='Ошибка транзакции, хэш-транзакции уже есть в базе данных')

    else:
        flag = True

    if flag:
        await PaymentStatesGroup.github_request.set()
        async with state.proxy() as data:
            data['transaction_hash'] = message.text
            data['status'] = tx_exists
        await bot.edit_message_reply_markup(chat_id=message.chat.id, message_id=message.message_id - 1,
                                            reply_markup=None)
        await bot.send_message(chat_id=message.chat.id,
                               text="*Транзакция была успешно подтверждена, пришлите свой гитхаб для выдачи доступа к софту.*",
                               parse_mode='markdown')
        promo = data['soft_promo']
        if data['soft_promo'] != '-':
            promo_quantity_left = data_base.select_promo_quantity(promo)
            if promo_quantity_left <= 1:
                data_base.del_promo(promo)
            else:
                data_base.edit_promo_quantity_minus_one(promo, promo_quantity_left)

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
                                    "Чтобы посмотреть другие софты нажмите на /menu.*",
                               parse_mode='markdown')

        refer_code = data_base.select_refer_code(user_id=message.from_user.id)[0]

        time = datetime.datetime.now()
        github = data['github']
        soft_name = data['soft_name']
        soft_price = data['soft_price']
        promo = data['soft_promo']
        discount = data['promo_discount']
        purchased = data['price_promo']
        transaction_hash = data['transaction_hash']
        username = message.from_user.username
        user_id = message.from_user.id
        status = '' # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1111

        data_base.add_purchase(user_id=user_id, username=username,
                               user_github=github, soft_name=soft_name, soft_price=soft_price,
                               promo=promo, discount=discount,
                               purchased=purchased, transaction_hash=transaction_hash, refer_code=refer_code,
                               status=status, data_time=time)

        await bot.send_message(chat_id='868320310', text=f"*🟢БЫЛА СОВЕРШЕНА ПОКУПКА🟢\nСофт: {data['soft_name']}\n"
                                                         f"Итоговая цена: {purchased} USDT\n"
                                                         f"Промо: {promo}\n"
                                                         f"Скидка промокода: {discount} USDT\n"
                                                         f"Реферал id: {refer_code}\n"
                                                         f"USERNAME покупателя: {username}\n"
                                                         f"Хэш-транзакции: {transaction_hash}\n"
                                                         f"Github: {data['github']}\n*", parse_mode='markdown')

        await state.finish()
    else:
        pass
