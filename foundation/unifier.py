from foundation.cancel_states import *
from foundation.admin import *
from foundation.callback import *
from foundation.client import *


# Последний хэндлер
@dp.message_handler()
async def otherwise_func(message: types.Message):
    await message.answer(MSG['RUS']['OTHERWISE'])
    print(message.text)
