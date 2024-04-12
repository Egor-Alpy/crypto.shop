# ======================================================================================================================
# BOT CREATION ----- BOT CREATION ----- BOT CREATION ----- BOT CREATION ----- BOT CREATION ----- BOT CREATION ----- BOT
# ======================================================================================================================

# IMPORT ----- IMPORT ----- IMPORT ----- IMPORT ----- IMPORT ----- IMPORT ----- IMPORT ----- IMPORT ----- IMPORT ----- I
from data_project.config import TOKEN
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import data_project.data_base as db


# Создание экземпляра Базы Данных
data_base = db.DataBase()

# Временное хранилище
storage = MemoryStorage()

# Инициализация бота
bot = Bot(TOKEN)
dp = Dispatcher(bot=bot, storage=storage)


