# IMPORT ----- IMPORT ----- IMPORT ----- IMPORT ----- IMPORT ----- IMPORT ----- IMPORT ----- IMPORT ----- IMPORT ----- I
from aiogram.dispatcher import FSMContext
from aiogram.types import *

from data_project.config import *
from bot_creation import *
from state_groups import *
from utilities import is_number
from data_project.text import *
from foundation.keyboards import *


# ======================================================================================================================
# ADMIN ----- ADMIN ----- ADMIN ----- ADMIN ----- ADMIN ----- ADMIN ----- ADMIN ----- ADMIN ----- ADMIN ----- ADMIN ----
# ======================================================================================================================

# SOFT ----- SOFT ----- SOFT ----- SOFT ----- SOFT ----- SOFT ----- SOFT ----- SOFT ----- SOFT ----- SOFT ----- SOFT ---
# ADD + + + + + + + + ADD + + + + + + + + + ADD + + + + + + + + ADD + + + + + + + + + ADD + + + + + + + + ADD + + + + +
@dp.message_handler(commands=['addsoft'], state=None)
async def add_soft(message: types.Message):
    if message.from_user.id in admin_id:
        await ClientStatesGroup.name.set()
        await message.answer(MSG['RUS']['SOFT']['ADD']['NAME'],
                             parse_mode='markdown',
                             reply_markup=cancel_markup)
    else:
        await message.reply(MSG['RUS']['ERROR']['NO_ROOTS'], parse_mode='markdown')


@dp.message_handler(lambda message: message.text, state=ClientStatesGroup.name)
async def load_softname(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await ClientStatesGroup.next()
    await message.reply(MSG['RUS']['SOFT']['ADD']['DESC'], parse_mode='markdown')


@dp.message_handler(state=ClientStatesGroup.desc)
async def load_desc(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['desc'] = message.text
    await ClientStatesGroup.next()
    await message.reply(MSG['RUS']['SOFT']['ADD']['PRICE'], parse_mode='markdown')


@dp.message_handler(state=ClientStatesGroup.price)
async def load_price(message: types.Message, state: FSMContext):
    if is_number(message.text):
        async with state.proxy() as data:
            data['price'] = message.text
        data_base.addsoft(name=data['name'], desc=data['desc'], price=data['price'])
        await message.reply(MSG['RUS']['DATA_BASE'], parse_mode='markdown')
        await state.finish()
    else:
        await message.reply(MSG['RUS']['ERROR']['INCORRECT_INPUT'], parse_mode='Markdown')


# SOFT ----- SOFT ----- SOFT ----- SOFT ----- SOFT ----- SOFT ----- SOFT ----- SOFT ----- SOFT ----- SOFT ----- SOFT ---
# DEL + + + + + + + + DEL + + + + + + + + + DEL + + + + + + + + DEL + + + + + + + + + DEL + + + + + + + + DEL + + + + +
@dp.message_handler(commands=['delsoft'], state=None)
async def delete_soft(message: types.Message):
    if message.from_user.id in admin_id:
        await message.answer(MSG['RUS']['SOFT']['DEL'],
                             parse_mode='markdown',
                             reply_markup=get_softs_inlinekeyboard_4delete())
    else:
        await message.reply(MSG['RUS']['ERROR']['NO_ROOTS'], parse_mode='markdown')


# PARTNER ----- PARTNER ----- PARTNER ----- PARTNER ----- PARTNER ----- PARTNER ----- PARTNER ----- PARTNER ----- PART
# ADD + + + + + + + + ADD + + + + + + + + + ADD + + + + + + + + ADD + + + + + + + + + ADD + + + + + + + + ADD + + + + +
@dp.message_handler(commands=['addpartner'])
async def add_partner(message: types.Message):
    if message.from_user.id in admin_id:
        await PartnerStatesGroup.user_id.set()
        await message.answer(MSG['RUS']['PARTNER']['ADD']['ID'],
                             parse_mode='markdown',
                             reply_markup=cancel_markup)
    else:
        await message.reply(MSG['RUS']['ERROR']['NO_ROOTS'], parse_mode='markdown')


@dp.message_handler(lambda message: message.text, state=PartnerStatesGroup.user_id)
async def load_userid(message: types.Message, state: FSMContext):
    if is_number(message.text):
        async with state.proxy() as data:
            data['user_id'] = message.text
        await PartnerStatesGroup.name.set()
        await message.reply(MSG['RUS']['PARTNER']['ADD']['NAME'], reply_markup=cancel_markup, parse_mode='markdown')
    else:
        await message.reply(MSG['RUS']['ERROR']['INCORRECT_INPUT'], parse_mode='Markdown')


@dp.message_handler(lambda message: message.text, state=PartnerStatesGroup.name)
async def load_partnername(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await PartnerStatesGroup.promo.set()
    await message.reply(MSG['RUS']['PARTNER']['ADD']['PROMO'], reply_markup=cancel_markup, parse_mode='markdown')


@dp.message_handler(lambda message: message.text, state=PartnerStatesGroup.promo)
async def load_promo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['promocode'] = message.text
    await PartnerStatesGroup.discount.set()
    await message.reply(MSG['RUS']['PARTNER']['ADD']['DISCOUNT'], reply_markup=cancel_markup, parse_mode='markdown')


@dp.message_handler(lambda message: message.text, state=PartnerStatesGroup.discount)
async def load_discount(message: types.Message, state: FSMContext):
    if is_number(message.text):
        async with state.proxy() as data:
            data['discount'] = message.text
        await PartnerStatesGroup.quantity.set()
        await message.reply(MSG['RUS']['PARTNER']['ADD']['QUANTITY'], reply_markup=cancel_markup, parse_mode='markdown')
    else:
        await message.reply(MSG['RUS']['ERROR']['INCORRECT_INPUT'], parse_mode='Markdown')


@dp.message_handler(lambda message: message.text, state=PartnerStatesGroup.quantity)
async def load_quantity(message: types.Message, state: FSMContext):
    if is_number(message.text):
        async with state.proxy() as data:
            data['quantity'] = message.text
        temporary_storage = data['user_id'], data['name'], data['promocode'], data['discount'], data['quantity']
        data_base.addpartner(data['user_id'], data['name'], data['promocode'], data['discount'], data['quantity'])
        await state.finish()
        await message.reply(MSG['RUS']['DATA_BASE'], parse_mode='markdown')
    else:
        await message.reply(MSG['RUS']['ERROR']['INCORRECT_INPUT'], parse_mode='Markdown')


# DELETE * DELETE * DELETE * DELETE * DELETE * DELETE * DELETE * DELETE * DELETE
@dp.message_handler(commands=['delpartner'], state=None)
async def delete_partner(message: types.Message):
    if message.from_user.id in admin_id:
        await message.answer(MSG['RUS']['PARTNER']['DEL'],
                             parse_mode='markdown',
                             reply_markup=get_partners_inlinekeyboard_4delete())
    else:
        await message.reply(MSG['RUS']['ERROR']['NO_ROOTS'], parse_mode='markdown')
