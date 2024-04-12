from bot_creation import *
from data_project.config import admin_id
from foundation.client import get_menu
from foundation.keyboards import get_softs_inlinekeyboard_4delete, cancel_markup, get_partners_inlinekeyboard_4delete
from state_groups import *
from data_project.text import *


@dp.message_handler(commands=CANCEL_CMDS, state=PaymentStatesGroup.all_states + ClientStatesGroup.all_states + PartnerStatesGroup.all_states)
async def cancel_commands_admin(message: types.Message, state: FSMContext):
    await state.finish()
    # await bot.send_message(chat_id=message.chat.id, text='машина состояния отменена')
    if message.text == '/delsoft':
        await delete_soft(message)
    if message.text == '/addsoft':
        await add_soft(message)
    if message.text == '/delpartner':
        await delete_partner(message)
    if message.text == '/addpartner':
        await add_partner(message)
    if message.text == '/addsoft':
        await add_soft(message)
    if message.text == '/menu':
        await menu_func(message)
    if message.text == '/start':
        await start_func(message)
    if message.text == '/cancel':
        await bot.send_message(chat_id=message.chat.id, text='машина состояния отменена')


@dp.message_handler(commands=['delsoft'], state=None)
async def delete_soft(message: types.Message):
    if message.from_user.id in admin_id:
        await message.answer(MSG['RUS']['SOFT']['DEL'],
                             parse_mode='markdown',
                             reply_markup=get_softs_inlinekeyboard_4delete())
    else:
        await message.reply(MSG['RUS']['ERROR']['NO_ROOTS'], parse_mode='markdown')


@dp.message_handler(commands=['addsoft'], state=None)
async def add_soft(message: types.Message):
    if message.from_user.id in admin_id:
        await ClientStatesGroup.name.set()
        await message.answer(MSG['RUS']['SOFT']['ADD']['NAME'],
                             parse_mode='markdown',
                             reply_markup=cancel_markup)
    else:
        await message.reply(MSG['RUS']['ERROR']['NO_ROOTS'], parse_mode='markdown')


@dp.message_handler(commands=['delpartner'], state=None)
async def delete_partner(message: types.Message):
    if message.from_user.id in admin_id:
        await message.answer(MSG['RUS']['PARTNER']['DEL'],
                             parse_mode='markdown',
                             reply_markup=get_partners_inlinekeyboard_4delete())
    else:
        await message.reply(MSG['RUS']['ERROR']['NO_ROOTS'], parse_mode='markdown')


@dp.message_handler(commands=['addpartner'])
async def add_partner(message: types.Message):
    if message.from_user.id in admin_id:
        await PartnerStatesGroup.user_id.set()
        await message.answer(MSG['RUS']['PARTNER']['ADD']['ID'],
                             parse_mode='markdown',
                             reply_markup=cancel_markup)
    else:
        await message.reply(MSG['RUS']['ERROR']['NO_ROOTS'], parse_mode='markdown')


@dp.message_handler(commands=['menu'])
async def menu_func(message: types.Message):
    # LANG = get_lang()
    await get_menu(user_id=message.from_user.id)


@dp.message_handler(commands=['start'])
async def start_func(message: types.Message):
    await message.answer(MSG['RUS']['START'], parse_mode='markdown')


