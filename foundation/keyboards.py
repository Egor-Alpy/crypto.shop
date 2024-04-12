# IMPORT ----- IMPORT ----- IMPORT ----- IMPORT ----- IMPORT ----- IMPORT ----- IMPORT ----- IMPORT ----- IMPORT ----- I
from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from data_project.data_base import *
from data_project.data_base import *
from bot_creation import *
from data_project.text import MSG


# Кнопка отмены машины состояния
cancel_markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
b1 = KeyboardButton('/cancel')
cancel_markup.add(b1)


# клавиатура софтов
def get_softs_inlinekeyboard():
    with sq.connect(db_name) as con:
        cur = con.cursor()
        cur.execute("SELECT name FROM software")
        rows = cur.fetchall()
        softs_markup = InlineKeyboardMarkup()
        for i in range(len(rows)):
            softs_markup.add(InlineKeyboardButton(rows[i][0], callback_data='SOFT' + rows[i][0]))
        softs_markup.add(InlineKeyboardButton('🔺 Назад', callback_data='menu_request'))
        return softs_markup


# Клавиатура удаление софтов
def get_softs_inlinekeyboard_4delete():
    with sq.connect(db_name) as con:
        cur = con.cursor()
        cur.execute("SELECT name FROM software")
        rows = cur.fetchall()
        softs_markup = InlineKeyboardMarkup()
        for i in range(len(rows)):
            softs_markup.add(InlineKeyboardButton(rows[i][0], callback_data='DELETE_SOFT' + rows[i][0]))
        return softs_markup


@dp.callback_query_handler(lambda call: call.data.startswith('DELETE_SOFT'))
async def software_list_menu(callback: types.CallbackQuery):
    data_base.delsoft(callback.data[11:])
    await callback.message.edit_reply_markup(reply_markup=get_softs_inlinekeyboard_4delete())


# Клавиатура удаление партнёров
def get_partners_inlinekeyboard_4delete():
    with sq.connect(db_name) as con:
        cur = con.cursor()
        cur.execute("SELECT user_id, name, promocode, discount, quantity FROM partners")
        rows = cur.fetchall()
        partners_markup = InlineKeyboardMarkup()
        for i in range(len(rows)):
            partners_markup.add(InlineKeyboardButton(f"name: {rows[i][1]}|id: {rows[i][0]}|promo: {rows[i][2]}"
                                                     f"|disc: {rows[i][3]}USDT|qty: {rows[i][4]}",
                                                     callback_data='DELETE_PARTNER' + str(rows[i][0])))
        return partners_markup


@dp.callback_query_handler(lambda call: call.data.startswith('DELETE_PARTNER'))
async def admin_info_keyboard(callback: types.CallbackQuery):
    data_base.delpartner(callback.data[14:])
    await callback.message.edit_reply_markup(reply_markup=get_partners_inlinekeyboard_4delete())
