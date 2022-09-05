import sqlite3 as sq
from time import time
from create_bot import Bot
import datetime

def sql_start():
    global base, cur
    base = sq.connect('people.db')
    cur = base.cursor()

    if base:
        print('Data base connected')
    else:
        print('DATABASE NOT WORKING')

    base.execute('CREATE TABLE IF NOT EXISTS people (name TEXT PRIMARY KEY, relation TEXT, birthday TEXT, priority TEXT)')
    base.commit()

async def sql_add_command(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO people VALUES (?, ?, ?, ?)', tuple(data.values()))
        base.commit()

async def sql_read(message):
    for ret in cur.execute('SELECT * FROM people').fetchall():
        await message.answer(f'Имя: {ret[0]}\nОтносится к тебе как: {ret[1]}\nДень рождения: {ret[2]}\nПриоритет: {ret[3]}')

async def read2():
    return cur.execute('SELECT * FROM people').fetchall()

async def sql_delete_command(name):
    cur.execute('DELETE FROM people WHERE name == ?', (name, ))
    base.commit()

async def get_closest_bd():
    list = {}
    for person in cur.execute('SELECT * FROM people').fetchall():
        bd = str(person[2]).split('.')
        delta = None
        if (datetime.datetime(year=datetime.date.today().year, month=int(bd[1]), day=int(bd[0])) - datetime.datetime.now()).days < 0:
            delta = datetime.datetime(year=datetime.date.today().year+1, month=int(bd[1]), day=int(bd[0])) - datetime.datetime.now()
        else:
            delta = datetime.datetime(year=datetime.date.today().year, month=int(bd[1]), day=int(bd[0])) - datetime.datetime.now()
        list[str(person[0])] = delta.days
    return min(list, key=list.get), min(list.values())

async def get_all_bd():
    list = []
    people = await read2()
    for person in people:
        bd = str(person[2]).split('.')
        delta = None
        if (datetime.datetime(year=datetime.date.today().year, month=int(bd[1]), day=int(bd[0])) - datetime.datetime.now()).days < 0:
            delta = datetime.datetime(year=datetime.date.today().year+1, month=int(bd[1]), day=int(bd[0])) - datetime.datetime.now()
        else:
            delta = datetime.datetime(year=datetime.date.today().year, month=int(bd[1]), day=int(bd[0])) - datetime.datetime.now()
        list.append([person[0], person[1], delta.days])
    return list