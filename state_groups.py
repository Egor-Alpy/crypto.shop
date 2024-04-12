# IMPORT ----- IMPORT ----- IMPORT ----- IMPORT ----- IMPORT ----- IMPORT ----- IMPORT ----- IMPORT ----- IMPORT ----- I
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State


# Add soft state
class ClientStatesGroup(StatesGroup):
    name = State()
    desc = State()
    price = State()


# Add partner state
class PartnerStatesGroup(StatesGroup):
    user_id = State()
    name = State()
    promo = State()
    discount = State()
    quantity = State()


# Add payment state
class PaymentStatesGroup(StatesGroup):
    promo = State()
    receipt = State()
    transaction = State()
    github_request = State()
