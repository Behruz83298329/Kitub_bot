from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from aiogram.dispatcher.filters.state import State, StatesGroup
import os
from buttons import menu, tahrir_menu, tasdiq_menu,cancel_search_button,cancel_book_search_button
from database import init_db, save_book, get_user_books, set_privacy, search_books_by_author ,search_books_by_book_name, update_book_name, update_book_author, delete_book_by_name

API_TOKEN = "7569490442:AAGQjt43yD7NX2k3WG_oM2N7TC679mHmBFo"

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

os.makedirs("files", exist_ok=True)
init_db()

class BookStates(StatesGroup):
    waiting_for_book_name = State()
    waiting_for_author_name = State()
    waiting_for_search_query = State()
    waiting_for_edit_choice = State()
    waiting_for_book_to_edit = State()
    waiting_for_new_book_name = State()
    waiting_for_new_author_name = State()
    waiting_for_book_to_delete = State()
    waiting_for_delete_confirm = State()
    waiting_for_search_by_book_name=State()

@dp.message_handler(commands=["start"])
async def start_handler(message: Message):
    await message.answer("Assalomu alaykum! Kitob botiga xush kelibsiz.", reply_markup=menu)

@dp.message_handler(text="Kitob qo`shish")
async def start_save(message: Message):
    await message.answer("Iltimos, kitob faylini yuboring.")

@dp.message_handler(content_types=types.ContentType.DOCUMENT)
async def handle_document(message: Message, state: FSMContext):
    user_id = message.from_user.id
    document = message.document
    file_name = document.file_name
    file_id = message.document.file_id
    await message.answer_document(file_id)

    file_info = await bot.get_file(document.file_id)
    file_path = file_info.file_path
    save_path = f"files/{file_name}"

    await bot.download_file(file_path, save_path)
    await state.update_data(file_name=file_name)
    await message.answer("Kitob nomini kiriting:")
    await BookStates.waiting_for_book_name.set()

@dp.message_handler(state=BookStates.waiting_for_book_name)
async def handle_book_name(message: Message, state: FSMContext):
    await state.update_data(book_name=message.text)
    await message.answer("Muallif ismini kiriting:")
    await BookStates.waiting_for_author_name.set()

@dp.message_handler(state=BookStates.waiting_for_author_name)
async def handle_author_name(message: Message, state: FSMContext):
 data = await state.get_data()
 save_book(message.from_user.id, data['file_name'], data['book_name'], message.text, message.from_user.id )
 await message.answer("Kitob muvaffaqiyatli saqlandi!", reply_markup=menu)
 await state.finish() 


@dp.message_handler(text="Kitoblarim")
async def show_user_books(message: Message):
    books = get_user_books(message.from_user.id)
    if not books:
        await message.answer("Sizda kitob yo‘q.")
        return

    for file_name, book_name, author_name in books:
        path = f"files/{file_name}"
        if os.path.exists(path):
            with open(path, 'rb') as doc:
                await message.answer_document(doc, caption=f"Nomi: {book_name}\nMuallif: {author_name}")
        else:
            await message.answer(f"{book_name} (muallif: {author_name}) — Fayl topilmadi")

@dp.message_handler(text="Maxfiylik")
async def make_private(message: Message):
    set_privacy(message.from_user.id, 1)
    await message.answer("Maxfiylik yoqildi.")

@dp.message_handler(text="Maxfiylikdan chiqish")
async def make_public(message: Message):
    set_privacy(message.from_user.id, 0)
    await message.answer("Maxfiylikdan chiqildi.")

@dp.message_handler(text="Kitob izlash muallif orqali")
async def search_books(message: Message):
    await message.answer("Muallif ismini kiriting:")
    await BookStates.waiting_for_search_query.set()
@dp.message_handler(state=BookStates.waiting_for_search_query)
async def handle_search(message: Message, state: FSMContext):

 books = search_books_by_author(message.text)
 if not books:
  await message.answer("Kitob topilmadi.",reply_markup=cancel_search_button)
 else: 
   for file_name, book_name,author_name in books:
    path = f"files/{file_name}"
    if os.path.exists(path):
        with open(path, 'rb') as doc:
            await message.answer_document(doc, caption=f"Muallif: {author_name}\nNomi: {book_name}")
    else:
                await message.answer(f"{book_name} — Fayl topilmadi")
    await state.finish()

 @dp.callback_query_handler(lambda c: c.data == 'cancel_search', state='*')
 async def cancel_search_handler (callback_query:types.CallbackQuery,state:FSMContext):
  await state.finish()
  await bot.send_message(callback_query.from_user.id,"Qidiruv bekor qilindi.",reply_markup=menu)

@dp.message_handler(text="Kitob izlash nomi orqali")
async def search_books(message: Message):
    await message.answer("kitobni nomini kiriting:")
    await BookStates.waiting_for_search_by_book_name.set()
    print("SOrovdan oldingi sorov")
@dp.message_handler(state=BookStates.waiting_for_search_by_book_name)
async def handle_search(message: Message, state: FSMContext):
    print("Bu yer ishlasa ")
    books = search_books_by_book_name(message.text)
    print(books)

    if not books:
        print("Bu yerda kitop topilmasa ishlaydi")
        await message.answer("Kitob topilmadi.",reply_markup=cancel_search_button)
    else: 
        print(books)
    for file_name, book_name,author_name in books:
        path = f"files/{file_name}"
        if os.path.exists(path):
            with open(path, 'rb') as doc:
                await message.answer_document(doc, caption=f"Muallif: {author_name}\nNomi: {book_name}")
        else:
            await message.answer(f"{book_name} — Fayl topilmadi")
        await state.finish()

@dp.callback_query_handler(lambda c: c.data == 'cancel_book_search', state='*')
async def cancel_book_search_handler (callback_query:types.CallbackQuery,state:FSMContext):
  await state.finish()
  await bot.send_message(callback_query.from_user.id,"Qidiruv bekor qilindi.",reply_markup=menu)

@dp.message_handler(text="Kitobni tahrirlash")
async def edit_book_start(message: Message):
    await message.answer("Tahrirlash turini tanlang:", reply_markup=tahrir_menu)
    await BookStates.waiting_for_edit_choice.set()

@dp.message_handler(state=BookStates.waiting_for_edit_choice)
async def choose_edit_type(message: Message, state: FSMContext):
    choice = message.text
    await state.update_data(edit_choice=choice)

    if choice in ["Nomini tahrirlash", "Muallifni tahrirlash"]:
        await message.answer("Tahrir qilinadigan kitob nomini kiriting:")
        await BookStates.waiting_for_book_to_edit.set()
    elif choice == "Kitobni o‘chirish":
        await message.answer("O‘chirmoqchi bo‘lgan kitob nomini kiriting:")
        await BookStates.waiting_for_book_to_delete.set()
    else:
        await message.answer("Bekor qilindi.", reply_markup=menu)
        await state.finish()

@dp.message_handler(state=BookStates.waiting_for_book_to_edit)
async def ask_new_value(message: Message, state: FSMContext):
    await state.update_data(book_to_edit=message.text)
    data = await state.get_data()

    if data['edit_choice'] == "Nomini tahrirlash":
        await message.answer("Yangi nomni kiriting:")
        await BookStates.waiting_for_new_book_name.set()
    elif data['edit_choice'] == "Muallifni tahrirlash":
        await message.answer("Yangi muallif ismini kiriting:")
        await BookStates.waiting_for_new_author_name.set()

@dp.message_handler(state=BookStates.waiting_for_new_book_name)
async def update_name(message: Message, state: FSMContext):
    data = await state.get_data()
    update_book_name(data['book_to_edit'], message.text)
    await message.answer("Kitob nomi yangilandi.", reply_markup=menu)
    await state.finish()

@dp.message_handler(state=BookStates.waiting_for_new_author_name)
async def update_author(message: Message, state: FSMContext):
    data = await state.get_data()
    update_book_author(data['book_to_edit'], message.text)
    await message.answer("Muallif ismi yangilandi.", reply_markup=menu)
    await state.finish()

@dp.message_handler(state=BookStates.waiting_for_book_to_delete)
async def ask_confirm(message: Message, state: FSMContext):
    await state.update_data(book_to_delete=message.text)
    await message.answer("Rostan ham o‘chirmoqchimisiz?",reply_markup=tasdiq_menu)
    await BookStates.waiting_for_delete_confirm.set()

@dp.message_handler(state=BookStates.waiting_for_delete_confirm)
async def confirm_delete(message: Message, state: FSMContext):
    data = await state.get_data()
    if message.text.lower() == "ha":
     delete_book_by_name(data.get('book_to_delete'), message.from_user.id)
     await message.answer("Kitob o‘chirildi.", reply_markup=menu)
     await state.finish()
     return
    else:
     await message.answer("Kitob o‘chirilmagan.", reply_markup=menu)
     await state.finish()

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)