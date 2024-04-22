# IMPORT ----- IMPORT ----- IMPORT ----- IMPORT ----- IMPORT ----- IMPORT ----- IMPORT ----- IMPORT ----- IMPORT ----- I
import datetime

from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from data_project.data_base import *

from bot_creation import *
from aiogram import types

from data_project.text import MSG, RECEIVER, USDT_CONTRACT_ADDRESS

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
                           text='*Введите промокод или нажмите "Пропустить"*',
                           reply_markup=promocode_check_markup, parse_mode='markdown')


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
        data['price_with_promo'] = float(data['soft_price']) - data['promo_discount']
    price_with_promo = float(data['soft_price']) - data['promo_discount']
    await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                                text=f"*Отправьте {price_with_promo} USDT по адресу:\n{RECEIVER}\n\nПосле отправьте "
                                     f"сообщение с хэшом транзакзции для подтверждения.*",
                                reply_markup=transaction_markup, parse_mode='markdown')
    async with state.proxy() as data:
        data['last_message'] = callback.message.message_id


# транзакция подтверждена
#############################################################
from aiogram import types
from aiogram.dispatcher import FSMContext
from web3 import Web3
from web3.types import HexStr
from bot_creation import *
from data_project.data_base import *


@dp.message_handler(state=PaymentStatesGroup.transaction)
async def transaction_check(message: types.Message, state: FSMContext):
    transaction_markup = InlineKeyboardMarkup()
    b1 = InlineKeyboardButton('🔴остановить состояние оплаты🔴', callback_data='cancel_purchase')
    transaction_markup.add(b1)

    try:
        chat_id = message.chat.id

        tx_hash = HexStr(message.text)
        con_web3 = Web3(provider=Web3.HTTPProvider(endpoint_uri='https://rpc.ankr.com/eth'))

        await bot.send_message(chat_id=chat_id, text='⌛️')
        tx_data = con_web3.eth.wait_for_transaction_receipt(transaction_hash=tx_hash, timeout=10)
        tx_status = tx_data['status']  # purchase status
        tx_status_for_db = str(tx_status)
        tx_contract = tx_data['to']  # smart-contract address
        tx_receiver = '0x' + tx_data['logs'][0]['topics'][2].hex()[26:]  # receiver address
        tx_coin_qty = int(tx_data['logs'][0]['data'].hex(), 16) / 10 ** 6  # USDT value
        tx_list_hashes = data_base.select_tx_hashes()  # list of all previous transactions

        async with state.proxy() as data:
            data['purchased'] = tx_coin_qty
            data['emoji_id'] = message.message_id + 1

        status_error = ''

        flag = True

        # check 1: smart-contract address
        if tx_contract != USDT_CONTRACT_ADDRESS:
            status_error += '\n🔸 *Некорректный адрес смарт-контракта*'
            tx_status_for_db += ' incorrect smart-contract address |'
            flag = False

        # check 2: receiver address
        if tx_receiver != tx_receiver:  # RECEIVER:
            status_error += '\n🔸 *Неверно указан адрес получателя*'
            tx_status_for_db += ' incorrect receiver address |'
            flag = False

        # check 3: quantity of purchased coins
        if tx_coin_qty < data['price_with_promo']:
            status_error += '\n🔸 *Вы перевели недостаточное кол-во средств*'
            tx_status_for_db += ' incorrect(low) coin quantity |'
            flag = False

        # check 4: unique transaction
        if tx_hash in tx_list_hashes:
            status_error += '\n🔸 *Ошибка транзакции, хэш-транзакции уже есть в базе данных*'
            tx_status_for_db += ' not unique transaction hash |'
            flag = False

        # check 5: transaction status
        if tx_status != 1:
            status_error += '\n🔸 *Ошибка транзакции*'
            flag = False

        if tx_status and flag:
            await bot.edit_message_text(chat_id=chat_id, message_id=data['emoji_id'], text='✅')
            await PaymentStatesGroup.github_request.set()
            async with state.proxy() as data:
                data['transaction_hash'] = message.text
                data['status'] = tx_status_for_db
            await bot.edit_message_reply_markup(chat_id=message.chat.id, message_id=data['last_message'],
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
            await bot.edit_message_text(chat_id=chat_id, message_id=data['emoji_id'], text='❌')
            await bot.send_message(chat_id=chat_id, text=status_error, reply_markup=transaction_markup, parse_mode='markdown')
            async with state.proxy() as data:
                data['status'] = tx_status_for_db
            refer_code = data_base.select_refer_code(user_id=message.from_user.id)[0]
            time = datetime.datetime.now()
            github = ''
            soft_name = data['soft_name']
            soft_price = data['soft_price']
            promo = data['soft_promo']
            discount = data['promo_discount']
            purchased = data['purchased']
            transaction_hash = message.text
            username = message.from_user.username
            user_id = message.from_user.id
            status = data['status']
            data_base.add_purchase(user_id=user_id, username=username,
                                   user_github=github, soft_name=soft_name, soft_price=soft_price,
                                   promo=promo, discount=discount,
                                   purchased=purchased, transaction_hash=transaction_hash, refer_code=refer_code,
                                   status=status, data_time=time)
    except:
        await bot.edit_message_text(message_id=message.message_id+1, chat_id=message.chat.id, text='🛂')
        await bot.send_message(chat_id=message.chat.id, text='*Ошибка проверки транзакции в блокчейне: транзакция'
                                                             ' была не найдена*', parse_mode='markdown', reply_markup=transaction_markup)

#############################################################


# закрытие покупки
@dp.message_handler(state=PaymentStatesGroup.github_request)
async def transaction_check(message: types.Message, state: FSMContext):

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
        purchased = data['purchased']
        transaction_hash = data['transaction_hash']
        username = message.from_user.username
        user_id = message.from_user.id
        status = data['status']
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