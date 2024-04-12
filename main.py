# ================================================================
# MAIN ----- MAIN ----- MAIN ----- MAIN ----- MAIN ----- MAIN ----
# ================================================================

# IMPORT ----- IMPORT ----- IMPORT ----- IMPORT ----- IMPORT -----

from bot_creation import *
from aiogram import executor

from foundation.unifier import *


# ON_STARTUP ----- ON_STARTUP ----- ON_STARTUP ----- ON_STARTUP ---
async def on_startup(_):
    print('==================\n [BOT IS RUNNING]\n==================')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
