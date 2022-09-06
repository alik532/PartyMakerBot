from create_bot import dp
from aiogram.utils import executor
from handlers import view, edit
from data_base.sqlite_db import sql_start
import schedule
from make_request import do_req
import time

async def on_startup(_):
    print('Bot Online')
    sql_start()

view.register_handlers_view(dp)
edit.register_handlers_edit(dp)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)