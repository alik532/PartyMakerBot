from aiogram import types
from aiogram.dispatcher import Dispatcher
from create_bot import dp
from data_base import sqlite_db
from data_base.sqlite_db import sql_read, get_all_bd
from time import sleep
from make_request import do_req
import schedule
from threading import Thread

async def show_people(message: types.Message):
    await sql_read(message)

async def show_closest_birthday(message: types.Message):
    birthday = await sqlite_db.get_closest_bd()
    await message.answer(f'{birthday[0]}: {birthday[1]} days left')

async def show_all_birthdays(message: types.Message):
    people = await get_all_bd()
    for person in people:
        await message.answer(f'{person[0]}({person[1]}): {person[2]} days left')

async def get_notif(message: types.Message):
    do_req()

def schedule_checker():
    while True:
        schedule.run_pending()
        sleep(1)

schedule.every().wednesday.at("23:10").do(do_req())


def register_handlers_view(dp: Dispatcher):
    dp.register_message_handler(get_notif, commands='notif')
    dp.register_message_handler(show_all_birthdays, commands='all_bd')
    dp.register_message_handler(show_people, commands='people')
    dp.register_message_handler(show_closest_birthday, commands='closest_bd')

