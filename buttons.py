from aiogram.types import ReplyKeyboardMarkup, KeyboardButton,InlineKeyboardMarkup,InlineKeyboardButton

menu = ReplyKeyboardMarkup(resize_keyboard=True)
menu.add(
    KeyboardButton("Kitob qo`shish"),
    KeyboardButton("Kitoblarim")
)
menu.add(
    KeyboardButton("Kitob izlash"),
    KeyboardButton("Maxfiylik"),
    KeyboardButton("Maxfiylikdan chiqish")
)
menu.add(
    KeyboardButton("Kitobni tahrirlash")
)

tahrir_menu = ReplyKeyboardMarkup(resize_keyboard=True)
tahrir_menu.add(
    KeyboardButton("Nomini tahrirlash"),
    KeyboardButton("Muallifni tahrirlash"),
    KeyboardButton("Kitobni o‘chirish")
)
tahrir_menu.add(KeyboardButton("Bekor qilish"))

tasdiq_menu = ReplyKeyboardMarkup(resize_keyboard=True)
tasdiq_menu.add(
    KeyboardButton("Ha"),
    KeyboardButton("Yo‘q")
)
cancel_search_button = InlineKeyboardMarkup(row_width=1)
cancel_search_button.add(InlineKeyboardButton("Qidiruvni bekor qilish",
callback_data="cancel_search")
)