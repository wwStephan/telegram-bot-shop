from contextlib import suppress

from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters import Text, Command
from aiogram.utils.exceptions import MessageNotModified

from config import admin_id, manager
from sql_lite import add_id, user_id, product, list_add, list_take_orders, list_take
from keyboard import keyboard, keyboard1, keyboard2, keyboard3, keyboard5, keyboard7

from main import dp, bot

user_data = dict()


@dp.message_handler(Command('start'))
async def start_info(message: Message):
    """"   Обработчик запуска бота """
    await message.answer(text='Привет, я Doner Master bot.🥙\n'
                              'Чтобы сделать заказ, воспользуйтесь кнопками внизу чата. \n')
    await message.answer(text='Bot начал работу! 👋', reply_markup=keyboard)
    global info
    info = list()
    print(message.chat.id)
    await add_id(message.chat.id)
    info.append(message.chat.id)


@dp.message_handler(Text(equals=['Помощь📒']))
async def get_help(message: Message):
    """"   Обработчик Кнопки помощь """
    await message.answer(
        text='Мы работаем круглосуточно ⏰ ,для уточнения заказа вы можете обратиться по номеру:+7 (3822) 33‒10‒00\n'
             'Также для заказа вы можете воспользоватся нашим мобильным приложением:Doner Master\n')


@dp.message_handler(Text(equals=['Сделать заказ🍴']))
async def get_place_list(message: Message):
    """"   Обработчик Кнопки заказа """
    await message.answer(text='Где хотите сделать заказ?🍴\n')
    await message.answer(text='Адреса точек👇', reply_markup=keyboard1)


@dp.callback_query_handler(text_contains='buy_')
async def get_products_category(call: CallbackQuery):
    """"   Обработчик меню """
    await call.answer(cache_time=2)
    t = call['data']
    place = t[t.find('Т'):]
    info.append(place)
    await call.message.answer(f'Вы выбрали точку 🎉{place}\n', reply_markup=keyboard5)
    await call.message.answer(f'Продукты и категории👇\n', reply_markup=keyboard2)
    await call.message.edit_reply_markup(reply_markup=None)


@dp.message_handler(Text(equals=['Меню📕']))
async def get_products_type(message: Message):
    """"   Обработчик кнопки меню """
    global ph
    try:
        ph.clear()
        d.clear()
    except:
        pass
    await message.answer(f'Точка:{info[1]} \n', reply_markup=keyboard5)
    await message.answer('Продукты и категории👇\n', reply_markup=keyboard2)


@dp.callback_query_handler(text_contains='Cancel')
async def cancel(call: CallbackQuery):
    """"   Обработчик отмены """
    await call.answer('Отмена', show_alert=True)
    await call.message.edit_reply_markup(reply_markup=None)


@dp.callback_query_handler(text_contains='_buy', state=None)
async def get_product(call: CallbackQuery):
    """"   Обработчик выбора товара """
    global ph, d
    ph = list()
    d = list()
    await call.answer(cache_time=5)
    t = call['data']
    product_name = t[t.find('p') + 1:]
    m = await product(f'{product_name}')
    c = 0
    for i in range(int(len(m) / 4)):
        try:
            keyboard6 = InlineKeyboardMarkup()
            keyboard6.add(InlineKeyboardButton('Купить', callback_data=f"100{c}"))
            await call.message.answer_photo(open(f'img/{m[c]}', 'rb'))
            await call.message.answer(f'🍴{m[c + 1]}\n')
            await call.message.answer(f'{m[c + 2]}\n'
                                      f'Цена:{m[c + 3]}₽\n', reply_markup=keyboard6)
            d.append(m[c + 1])
            ph.append(m[c])
            ph.append(m[c + 3])
            c += 4
        except FileNotFoundError:
            pass
    await call.message.edit_reply_markup(reply_markup=None)


@dp.callback_query_handler(text_contains='100')
async def how_many_product(call: CallbackQuery):
    """"   Обработчик выбора количества товара """
    global info
    s = call['data'].replace('100', '')
    k = d[int(int(s) / 4)]
    p = ph[int(int(s) / 2)]
    t = ph[int(int(s) / 2) + 1]
    info.append(k)
    info.append(t)
    await call.message.answer_photo(open(f'img/{p}', 'rb'))
    await call.message.answer(f"{k}\n"
                              f"Цена: {t}₽\n")
    await call.message.answer("Укажите количество: 1", reply_markup=keyboard3)
    await call.message.edit_reply_markup(reply_markup=None)


@dp.callback_query_handler(Text(startswith="num_"))
async def callbacks_num(call: CallbackQuery):
    """"   Обработчик изменения количества товара """
    user_value = user_data.get(call.from_user.id, 1)
    action = call.data.split("_")[1]
    if action == "incr":
        user_data[call.from_user.id] = user_value + 1
        await update_num_text(call.message, user_value + 1)
    elif action == "decr":
        user_data[call.from_user.id] = user_value - 1
        if user_data[call.from_user.id] < 1:
            user_data[call.from_user.id] = 1
        await update_num_text(call.message, user_value - 1)
    elif action == "finish":
        await call.message.edit_text(f"Итого: {user_value}")
        info.append(user_value)
        user_data[info[0]] = 1
    await call.answer()


async def update_num_text(message: Message, new_value: int):
    """"   Функция обнавления сообщения """
    with suppress(MessageNotModified):
        if new_value < 1:
            new_value = 1
        await message.edit_text(f"Укажите количество: {new_value}", reply_markup=keyboard3)


@dp.message_handler(Text(equals=['Корзина🛒']))
async def basket(message: Message):
    """"   Функция отображения корзины """
    global info, v
    if len(info[2:]) % 3 != 0 or type(info[-2]) != int:
        info = await basket_cleaning(info)
    if len(info) < 5:
        await message.answer('Ваша корзина пуста', reply_markup=keyboard5)
    else:
        v = list()
        keyboard9 = InlineKeyboardMarkup()
        l = await message.answer(f'🛒🛒🛒🛒🛒🛒🛒🛒🛒🛒🛒🛒🛒🛒🛒🛒\n'
                                 f'Вы выбрали точку 🎉{info[1]}\n'
                                 'Ваша корзина:\n')
        v.append(l.message_id)
        t = info[2:]
        c = 0
        k = 0
        for i in range(int(len(t) / 3)):
            keyboard9.add(InlineKeyboardButton(f'{i + 1} ) {t[c]}', callback_data=f"300{i}"))
            keyboard9.add(InlineKeyboardButton(f'-', callback_data=f"201{i}"),
                          InlineKeyboardButton(f'Убрать товар', callback_data=f"204{i}"),
                          InlineKeyboardButton(f'+', callback_data=f"203{i}"))
            l = await message.answer(f'🔹 {t[c]} 1 — {t[c + 1]}\n'
                                     f'└ {t[c + 2]} x {t[c + 1]}={t[c + 2] * t[c + 1]}₽ \n', reply_markup=keyboard7)
            v.append(l.message_id)
            k += t[c + 2] * t[c + 1]
            c += 3
        keyboard9.add(InlineKeyboardButton('Отчистить корзину', callback_data=f"300"))
        l = await message.answer(f'Итог: 🎉{k}₽\n', reply_markup=keyboard9)
        v.append(l.message_id)


@dp.callback_query_handler(text_contains='20')
async def basket_product_edit(call: CallbackQuery):
    """"   Обработчик редактирования количества товара в корзине    """
    s = str(call['data'].replace('20', ''))
    if int(s[0]) == 1:
        info[(3 * int(s[1]) + 1) + 3] = info[(3 * int(s[1]) + 1) + 3] - 1
        if int(info[(3 * int(s[1]) + 1) + 3]) == 0:
            info.pop((3 * int(s[1]) + 1) + 1)
            info.pop((3 * int(s[1]) + 1) + 1)
            info.pop((3 * int(s[1]) + 1) + 1)
    if int(s[0]) == 4:
        info.pop((3 * int(s[1]) + 1) + 1)
        info.pop((3 * int(s[1]) + 1) + 1)
        info.pop((3 * int(s[1]) + 1) + 1)
    if int(s[0]) == 3:
        info[(3 * int(s[1]) + 1) + 3] = info[(3 * int(s[1]) + 1) + 3] + 1
    for i in v:
        await bot.delete_message(info[0], i)
    await basket(message=call.message)


@dp.callback_query_handler(text_contains='300')
async def basket_product_delete(call: CallbackQuery):
    """"   Обработчик удаления товаров из корзины    """
    global info
    info = info[0:2]
    await basket(message=call.message)


@dp.message_handler(Text(equals=['Оформить заказ✅']))
async def send_manager(message: Message):
    """"   Функция отправки сообщения для администратора о заказе   """
    global info
    await bot.send_message(manager, info)
    await list_add(info)
    info = info[:2]
    await message.answer('Cпасибо за заказ!'
                         'Для уточнения заказа вы можете обратиться по номеру:+7 (3822) 33‒10‒00', reply_markup=None)


@dp.message_handler(Text(equals=['Мои заказы📜']))
async def orders_list(message: Message):
    """"   Функция для показа заказов пользователя   """
    l = await list_take_orders(info[0])
    keyboard4 = InlineKeyboardMarkup()
    n = 0
    for i in l:
        i = i[:4] + '-' + i[4:6] + '-' + i[6:8] + ' ' + i[8:10] + ':' + i[10:12]
        keyboard4.add(InlineKeyboardButton(f'Заказ от {i}', callback_data=f"40t{n}"))
        n += 1
    await message.answer('Ваши заказы', reply_markup=keyboard4)


@dp.callback_query_handler(text_contains='40t')
async def take_order(call: CallbackQuery):
    """"   Функция для добавления в карзину выбранного заказа   """
    global info
    s = str(call['data'].replace('40t', ''))
    l = await list_take_orders(info[0])
    date = l[int(s)]
    info = await list_take(date, info[0])
    q = info[:2]
    t = info[2]
    t = t.split()
    for i in range(0, len(t), 3):
        t[i + 1] = int(t[i + 1])
        t[i + 2] = int(t[i + 2])
    info = q + t
    await call.message.edit_reply_markup(reply_markup=None)
    await basket(message=call.message)


# send section
@dp.message_handler(Command('sendall'))
async def send_all(message: Message):
    """"   Функция рассылки   """
    if message.chat.id == int(admin_id):
        list_user_id = await user_id()
        for i in list_user_id:
            try:
                await bot.send_message(i, message.text[message.text.find(' '):])
            except:
                pass
        await message.answer('Done')
    else:
        await message.answer('Error')


@dp.message_handler(Command('sendallwp'))
async def send_allwp(message: Message):
    """"   Функция рассылки с фото   """
    if message.chat.id == int(admin_id):
        list_user_id = await user_id()
        for i in list_user_id:
            try:
                await bot.send_photo(i, open('photo.jpg', 'rb'), message.text[message.text.find(' '):])
            except:
                pass
        await message.answer('Done')
    else:
        await message.answer('Error')


async def basket_cleaning(list1):
    """"   Функция отчистки козрзины при выборе позиции не до конца   """
    if len(list1[2:]) % 3 == 0 and type(list1[-2]) == int:
        return list1
    t = list1[2:]
    k = list1[:2]
    for i in range(len(list1)):
        try:
            if type(t[int((i + 1) * 3) - 1]) == str:
                t.pop(i * 3)
                t.pop(i * 3)
                break
        except IndexError:
            t.pop(i * 3)
            t.pop(i * 3)
            break
    list1 = k + t
    if len(list1[2:]) % 3 == 0 and type(list1[-2]) == int:
        return list1
    else:
        return basket_cleaning(list1)


@dp.message_handler(Text(equals=['shopingbasket']))
async def info_admin(message: Message):
    """ Функция информации для администратора """
    print(info, type(info))


@dp.message_handler()
async def NLO(message: Message):
    """"   Обработчик неопознанного события    """
    await message.answer('Я ещё молодой бот,я не могу решать такие сложные задачи.\n'
                         ' Но я обязательно над ней подумаю!\n🤔🤔🤔🤔')
