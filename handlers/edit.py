from email import message
from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext, Dispatcher
from data_base import sqlite_db
from keyboards.add import cancel_kb
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher.filters import Text

class FSMEdit(StatesGroup):
    name = State()
    relation = State()
    birthday = State()
    priority = State()

async def add_new(message: types.Message):
    await FSMEdit.name.set()
    await message.answer('Введи имя человека...', reply_markup=cancel_kb)

async def cancel_adding(message: types.Message, state: FSMEdit):
    curr_state = await state.get_state()
    if curr_state is None:
        return None
    else:
        await state.finish()
        await message.answer('Cancelled')

async def enter_name(message: types.Message, state: FSMEdit):
    async with state.proxy() as data:
        data['name'] = message.text
    await FSMEdit.next()
    await message.answer('Кем он к тебе относится?', reply_markup=cancel_kb)

async def enter_relation(message: types.Message, state: FSMEdit):
    async with state.proxy() as data:
        data['relation'] = message.text
    await FSMEdit.next()
    await message.answer('Какого числа его день рождения?', reply_markup=cancel_kb)

async def enter_birthday(message: types.Message, state: FSMEdit):
    async with state.proxy() as data:
        data['birthday'] = message.text
    await FSMEdit.next()
    await message.answer('Поставь ему приоритет от 1 до 3:', reply_markup=cancel_kb)

async def enter_priority(message: types.Message, state: FSMEdit):
    async with state.proxy() as data:
        data['priority'] = message.text
    await sqlite_db.sql_add_command(state)
    await state.finish()

async def person_to_delete(callback_query: types.CallbackQuery):
    await sqlite_db.sql_delete_command(callback_query.data.replace('del ', ''))
    await callback_query.answer('DELETED')

async def delete_person(message: types.Message):
    people = await sqlite_db.read2()
    for person in people:
        await message.answer(f'Имя: {person[0]}\nДень рождения: {person[2]}',\
             reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(text='Delete', callback_data=f'del {person[0]}')))

def register_handlers_edit(dp: Dispatcher):
    dp.register_message_handler(add_new, commands='add')
    dp.register_message_handler(cancel_adding, commands='Отменить', state="*")
    dp.register_message_handler(enter_name, state=FSMEdit.name)
    dp.register_message_handler(enter_relation, state=FSMEdit.relation)
    dp.register_message_handler(enter_birthday, state=FSMEdit.birthday)
    dp.register_message_handler(enter_priority, state=FSMEdit.priority)
    dp.register_callback_query_handler(person_to_delete, Text(startswith='del'))
    dp.register_message_handler(delete_person, commands='delete')