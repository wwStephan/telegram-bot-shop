from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Сделать заказ🍴'),
        ],
        [
            KeyboardButton(text='Помощь📒'),
            KeyboardButton(text='Мои заказы📜')
        ]
    ],
    resize_keyboard=True
)


cb = CallbackData('buy', 'id', 'name')
keyboard2 = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='ХИТЫ_ПРОДАЖ🔥', callback_data='_buy:0:pХИТЫ_ПРОДАЖ')
        ],
        [
            InlineKeyboardButton(text='КОМБО', callback_data='_buy:1:pКОМБО')
        ],
        [
            InlineKeyboardButton(text='шаурма_300гр🌯', callback_data='_buy:2:pшаурма_300гр')
        ],
        [
            InlineKeyboardButton(text='шаурма_400гр🌯', callback_data='_buy:3:pшаурма_400гр')
        ],
        [
            InlineKeyboardButton(text='шаурма_500гр🌯', callback_data='_buy:4:pшаурма_500гр')
        ],
        [
            InlineKeyboardButton(text='ГОРЯЧИЕ_БЛЮДА🍚', callback_data='_buy:5:pГОРЯЧИЕ_БЛЮДА')
        ],
        [
            InlineKeyboardButton(text='САЛАТЫ🥗', callback_data='_buy:6:pСАЛАТЫ')
        ],
        [
            InlineKeyboardButton(text='БЛИНЧИКИ🥞', callback_data='_buy:7:pБЛИНЧИКИ')
        ],
        [
            InlineKeyboardButton(text='ВЫПЕЧКА🥧', callback_data='_buy:8:pВЫПЕЧКА')
        ],
        [
            InlineKeyboardButton(text='НАПИТКИ🥤', callback_data='_buy:9:pНАПИТКИ')
        ],
        [
            InlineKeyboardButton(text='СОУСЫ / ДОБАВКИ🥩', callback_data='_buy:10:pСОУСЫДОБАВКИ')
        ],
        [
            InlineKeyboardButton(text='Cancel🚫', callback_data='Cancel')
        ]
    ]
)

keyboard1 = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Усова, 11а', callback_data='buy_:0:Томск_Усова, 11а')
    ],
    [
        InlineKeyboardButton(text='Cоветская, 80', callback_data='buy_:1:Томск_Cоветская, 80')
    ],
    [
        InlineKeyboardButton(text='Иркутский тракт, 61/7', callback_data='buy_:2:Томск_Иркутский тракт, 61/7')
    ],
    [
        InlineKeyboardButton(text='проспект Ленина, 54Б', callback_data='buy_:3:Томск_проспект Ленина, 54Б')
    ],
    [
        InlineKeyboardButton(text='проспект Ленина, 41', callback_data='buy_:4:Томск_проспект Ленина, 41')
    ],
    [
        InlineKeyboardButton(text='проспект Фрунзе, 92Б', callback_data='buy_:5:Томск_проспект Фрунзе, 92Б')
    ],
    [
        InlineKeyboardButton(text='проспект Фрунзе, 102а', callback_data='buy_:6:Томск_проспект Фрунзе, 102а')
    ],
    [
        InlineKeyboardButton(text='79 Гвардейской Дивизии, 12/5',
                             callback_data='buy_:7:Томск_79 Гвардейской Дивизии, 12/5')
    ],
    [
        InlineKeyboardButton(text='Иркутский тракт, 54/1', callback_data='buy_:8:Томск_Иркутский тракт, 54/1')
    ],
    [
        InlineKeyboardButton(text='Cancel', callback_data='Cancel')
    ]
]
)

keyboard3 = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="-1", callback_data="num_decr"),
        InlineKeyboardButton(text="+1", callback_data="num_incr"),
    ],
    [
        InlineKeyboardButton(text="Добавить в корзину", callback_data="num_finish")
    ]
]
)


keyboard5 = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Меню📕'),
            KeyboardButton(text='Корзина🛒'),
        ],
        [
            KeyboardButton(text='Помощь📒'),
            KeyboardButton(text='Мои заказы📜')
        ],
    ],
    resize_keyboard=True
)

keyboard7 = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Меню📕'),
        ],
        [
            KeyboardButton(text='Оформить заказ✅'),
        ],
    ],
    resize_keyboard=True
)

