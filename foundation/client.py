# IMPORT ----- IMPORT ----- IMPORT ----- IMPORT ----- IMPORT ----- IMPORT ----- IMPORT ----- IMPORT ----- IMPORT ----- I
from aiogram import types
from bot_creation import *

from foundation.keyboards import get_softs_inlinekeyboard
from data_project.data_base import *
from data_project.text import *

import web3
# ======================================================================================================================
# MAIN FUNCTIONS ----- MAIN FUNCTIONS MAIN FUNCTIONS ----- MAIN FUNCTIONS MAIN FUNCTIONS ----- MAIN FUNCTIONS MAIN FUNCT
# ======================================================================================================================


# START ----- START ----- START ----- START ----- START ----- START ----- START ----- START ----- START ----- START ----
@dp.message_handler(commands=['start'])
async def start_func(message: types.Message):
    await message.answer(MSG['RUS']['START'], parse_mode='markdown')
    data_base.adduser(user_id=message.from_user.id, name=message.from_user.username, message=message)


# MENU ----- MENU ----- MENU ----- MENU ----- MENU ----- MENU ----- MENU ----- MENU ----- MENU ----- MENU ----- MENU ---
@dp.message_handler(commands=['menu'])
async def menu_func(message: types.Message):
    # LANG = get_lang()
    await get_menu(user_id=message.from_user.id)


async def get_menu(message_id=None, user_id=None, LANG='rus'):
    menu_markup = InlineKeyboardMarkup()
    b1 = InlineKeyboardButton('Софты', callback_data='soft_menu')
    b2 = InlineKeyboardButton('Канал', url='https://t.me/AT_industries')
    menu_markup.add(b1, b2)
    if message_id is None:
        await bot.send_message(chat_id=user_id, text=MSG['RUS']['MENU'], reply_markup=menu_markup,
                               parse_mode='markdown')
    else:
        await bot.edit_message_text(
            chat_id=user_id, message_id=message_id, text=MSG['RUS']['MENU'],
            reply_markup=menu_markup, parse_mode='markdown'
        )


# SOFT MENU ----- SOFT MENU ----- SOFT MENU ----- SOFT MENU ----- SOFT MENU ----- SOFT MENU ----- SOFT MENU ----- SOFT M
@dp.callback_query_handler(lambda call: call.data.startswith('soft_menu'))
async def menu_soft_func(callback: types.CallbackQuery):
    await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                                text=MSG['RUS']['SOFT_MENU'],
                                reply_markup=get_softs_inlinekeyboard(), parse_mode='markdown')


@dp.callback_query_handler(lambda call: call.data.startswith('menu_request'))
async def menu_soft_func(callback: types.CallbackQuery):
    await get_menu(message_id=callback.message.message_id, user_id=callback.message.chat.id)


# PURCHASE CHECK ----- PURCHASE CHECK ----- PURCHASE CHECK ----- PURCHASE CHECK ----- PURCHASE CHECK ----- PURCHASE CHEC
'''@dp.message_handler(commands=['pur'])
async def pur(messagee: types.Message):
    from web3 import Web3
    from web3.types import HexStr
    contract_adress_usdt = '0xdAC17F958D2ee523a2206206994597C13D831ec7'
    tx_hash = '0xd3a08bbe68b8949ea43a76b5720914dcdaebc2b47b69d006af976aa84d5c9752'
    con_web3 = Web3(provider=Web3.HTTPProvider(endpoint_uri='https://rpc.ankr.com/eth'))
    tx_hash = HexStr(tx_hash)
    tx_data = con_web3.eth.wait_for_transaction_receipt(transaction_hash=tx_hash, timeout=1000)
    tx_exists = tx_data['status']
    tx_contract = tx_data['to']
    tx_receiver = '' # !? !? !? !? !? !? !? !? !? !? !? !
    tx_coins_qty = tx_data['logs']

    await bot.send_message(messagee.chat.id, data)
    await bot.send_message(messagee.chat.id, data['status'])


'''

