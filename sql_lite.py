import sqlite3
import datetime
from datetime import datetime, date


async def add_id(id):
    """"  Функция добавления id пользователей для рассылки """
    with sqlite3.connect('users.db') as connect:
        cursor = connect.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS login_id(
            id INTEGER PRIMARY KEY
        )""")
        cursor.execute(f"SELECT id FROM login_id WHERE id={id}")
        data = cursor.fetchone()
        if data is None:
            connect.commit()
            user_id = [id]
            cursor.execute("INSERT INTO login_id VALUES(?);", user_id)
            connect.commit()


async def user_id():
    """"  Функция получения списка id пользователей для рассылки """
    with sqlite3.connect('users.db') as connect:
        cursor = connect.cursor()
        query = "SELECT * FROM login_id"
        cursor.execute(query)
        data = cursor.fetchall()
        m = []
        for i in data:
            i = int(i[0])
            m.append(i)
        return m


async def product(table):
    """"  Функция получения информации о товаре в категории """
    with sqlite3.connect('food_list.db') as connect:
        cursor = connect.cursor()
        query = f'SELECT * FROM {table}'
        cursor.execute(query)
        data = cursor.fetchall()
        m = []
        for i in data:
            structure = i[1]
            price = i[-2]
            photoname = i[-1]
            name = i[0]
            m.extend([photoname, name, structure, price])
        return (m)


async def list_add(list2):
    """"  Функция добавления заказа в бд """
    with sqlite3.connect('basket.db') as connect:
        current_date = str(date.today())
        time = datetime.now().strftime('%H:%M')
        lasttime = current_date + ' ' + time
        lasttime = lasttime.replace('-', '')
        lasttime = lasttime.replace(' ', '')
        lasttime = lasttime.replace(':', '')
        cursor = connect.cursor()
        food = (list2[2:])
        for i in range(int(len(food) / 3)):
            print('tut', food[int(i * 3)])
            food[int(i * 3)] = food[int(i * 3)].replace(' ', '_')
        k = str()
        for i in food:
            k += str(i) + ' '
        cursor.execute(""" CREATE TABLE IF NOT EXISTS order1(id, place, product, time) """)
        place = str(list2[1])
        params = (list2[0], place, k, lasttime)
        cursor.execute("INSERT INTO order1 VALUES (?, ?, ?, ?)", params)
        connect.commit()


async def list_take_orders(id):
    """"  Функция получения списка заказов пользователя """
    with sqlite3.connect('basket.db') as connect:
        cursor = connect.cursor()
        query = f'SELECT * FROM order1 WHERE id={id}'
        cursor.execute(query)
        data = cursor.fetchall()
        m = []
        for i in data:
            time = i[-1]
            m.extend([time])
        return m


async def list_take(data, id):
    """"  Функция получения информации о конкретном заказу пользователя """
    with sqlite3.connect('basket.db') as connect:
        cursor = connect.cursor()
        data.replace(' ', 'T')
        query = f'SELECT * FROM order1 WHERE id={id} and time={data}'
        cursor.execute(query)
        data = cursor.fetchall()
        m = []
        for i in data:
            id = i[0]
            place = i[1]
            product = i[2]
            m.extend([id, place, product])
        return m
