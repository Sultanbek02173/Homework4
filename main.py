from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
import config 
import logging
import sqlite3
from datetime import datetime


bot = Bot(token = config.token)
dp = Dispatcher(bot)
dp = Dispatcher(bot, storage=MemoryStorage())
print(dp)
storage = MemoryStorage()
print(storage)
logging.basicConfig(level=logging.INFO)

connect = sqlite3.connect('dodo_pizza.db')
cursor = connect.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS users(
    username VARCHAR(255),
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    id_user INTEGER PRIMARY KEY,
    phone_number VARCHAR(15) 
    );
    """)

cursor.execute("""CREATE TABLE IF NOT EXISTS address(
    address_longitude VARCHAR(255),
    address_latitude VARCHAR(255),
    id_user INTEGER
    );
    """)

cursor.execute("""CREATE TABLE IF NOT EXISTS orders(
    title VARCHAR(255),
    address_destination VARCHAR(255),
    date_time_order VARCHAR(255)
    );
    """)    

connect.commit()



@dp.message_handler(commands = 'start')
async def start(message: types.Message):
    cursor = connect.cursor()
    cursor.execute(f"SELECT id_user FROM users WHERE id_user = {message.from_user.id};")
    res = cursor.fetchall()
    if res == []:
        cursor.execute(f"""INSERT INTO users VALUES ('{message.from_user.username}', 
        '{message.from_user.first_name}', '{message.from_user.last_name}', {message.from_user.id}, "0")""")
    connect.commit()

    inline_btn_1 = InlineKeyboardButton('Отправить номер', callback_data='button1')
    inline_btn_2 = InlineKeyboardButton('Отправить локацию', callback_data='button2')
    inline_btn_3 = InlineKeyboardButton('Заказать еду', callback_data='button3')

    inline_kb1 = InlineKeyboardMarkup().add(inline_btn_1, inline_btn_2, inline_btn_3)

    # ilnline_kb = [
    #     [types.InlineKeyboardButton("Отправить номер", callback_data = "user_number", request_contact = True)],
    #     [InlineKeyboardButton("Отправить локацию", callback_data = "user_locat", request_location = True)],
    #     [InlineKeyboardButton("Заказать еду", callback_data = "user_order")]
    # ]
    # Inline_kb = InlineKeyboardMarkup(inline_keyboard = ilnline_kb)

    await message.answer(f"Здраствуйте {message.from_user.full_name}", reply_markup = inline_kb1)

@dp.callback_query_handler(lambda callbak: callbak.data == 'button1')
async def process_callback_button1(callbak: types.CallbackQuery):
    kb = [
        [KeyboardButton("/contact", request_contact=True)]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, one_time_keyboard=True,
    input_field_placeholder="Выберите вариант загрузки")
    # print(callbak)
    await callbak.message.answer(f"Нажата_кнопка_контакта!", reply_markup=keyboard)

@dp.callback_query_handler(lambda callbak: callbak.data == 'button2')
async def process_callback_button1(callbak: types.CallbackQuery):
    kb = [
        [KeyboardButton("/location", request_location=True)]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, one_time_keyboard=True,
    input_field_placeholder="Выберите вариант загрузки")
    await callbak.message.answer(f"Нажата_кнопка_локации!", reply_markup = keyboard)

@dp.message_handler(content_types=types.ContentType.CONTACT)
async def get_contact(msg:types.Message):
    cursor = connect.cursor()
    cursor.execute(f"SELECT phone_number FROM users WHERE id_user = {msg.contact['phone_number']};")
    res = cursor.fetchall()
    # print(res)
    if res == []:
        cursor.execute(f"""UPDATE users SET phone_number = {msg.contact['phone_number']} WHERE phone_number = '0';""")
    connect.commit()
    await msg.reply("Ваш телефон принят")
    # print(msg.contact['phone_number'])

@dp.message_handler(content_types=types.ContentType.LOCATION)
async def get_location(msg:types.Message):
    cursor = connect.cursor()
    longitude = str(msg.location['longitude'])
    latitude = str(msg.location['latitude'])
    cursor.execute(f"SELECT id_user FROM users WHERE id_user = {msg.from_user.id};")
    cursor.execute(f"""INSERT INTO address VALUES ('{longitude}', '{latitude}',
     '{msg.from_user.id}')""")
    connect.commit()
    # print(msg.location['latitude'])
    # print(msg.location['longitude'])
    # await bot.send_location(msg.chat.id, msg.location['latitude'], msg.location['longitude'])
    await msg.answer("Ваша локация принята")

@dp.callback_query_handler(lambda callbak: callbak.data == 'button3')
async def process_callback_button1(callbak: types.CallbackQuery):
    kb = [
        [KeyboardButton("/Calzone")],
        [KeyboardButton("/Pizza_Romana")],
        [KeyboardButton("/Pizza_al_tegamino")]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, one_time_keyboard=True,
    input_field_placeholder="Выберите вариант загрузки")
    await callbak.message.answer(f"Выберите пиццу!", reply_markup = keyboard)

@dp.message_handler(commands = 'Calzone')
async def start(message: types.Message):
    current_datetime = datetime.now()
    current_datetime1 = str(current_datetime)
    await message.answer("Вы заказали пиццу Calzone")
    cursor = connect.cursor()
    cursor.execute(f"SELECT id_user FROM users WHERE id_user = {message.from_user.id};")
    cursor.execute(f"""INSERT INTO orders VALUES ('Calzone', "город Ош", '{current_datetime1}')""")
    connect.commit()

@dp.message_handler(commands = 'Pizza_Romana')
async def start(message: types.Message):
    current_datetime = datetime.now()
    current_datetime1 = str(current_datetime)
    await message.answer("Вы заказали пиццу CalzPizza Romanaone")
    cursor = connect.cursor()
    cursor.execute(f"SELECT id_user FROM users WHERE id_user = {message.from_user.id};")
    cursor.execute(f"""INSERT INTO orders VALUES ('Pizza Romana', "город Ош", '{current_datetime1}')""")
    connect.commit()

@dp.message_handler(commands = 'Pizza_al_tegamino')
async def start(message: types.Message):
    current_datetime = datetime.now()
    current_datetime1 = str(current_datetime)
    await message.answer("Вы заказали пиццу Pizza al tegamino")
    cursor = connect.cursor()
    cursor.execute(f"SELECT id_user FROM users WHERE id_user = {message.from_user.id};")
    cursor.execute(f"""INSERT INTO orders VALUES ('Pizza al tegamino', "город Ош", '{current_datetime1}')""")
    connect.commit()


executor.start_polling(dp)