import requests
from config import weather_token, tg_token
from aiogram import Bot, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

storage = MemoryStorage()
bot = Bot(token=tg_token)
dp = Dispatcher(bot, storage=storage)

kb_weather = KeyboardButton('/Погода')
kb = ReplyKeyboardMarkup(resize_keyboard=True)
kb.add(kb_weather)


class FSMAdmin(StatesGroup):
    lat = State()
    lon = State()




@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply ('Приветствую!', reply_markup=kb)

@dp.message_handler(commands='Погода', state=None)
async def weather(message: types.Message):
    await FSMAdmin.next()
    await message.answer('Введите широту')

@dp.message_handler(state=FSMAdmin.lat)
async def get_lat(message: types.Message, state:FSMContext):
    async with state.proxy() as data:
        data['lat'] = (message.text)
        await FSMAdmin.next()
        await message.reply('Введите долготу')

@dp.message_handler(state=FSMAdmin.lon)
async def get_lon (message: types.Message, state:FSMContext):
    async with state.proxy() as data:
        data['lon'] = (message.text)
    async with state.proxy() as data:
        m1 = data['lat']
        m2 = data['lon']

        emodji = {
            'Clear': 'Ясно \U00002600',
            'Clouds': 'Облачно \U00002601',
            'Rain': 'Дождь \U00002614',
            'Drizzle': 'Дождь \U00002614',
            'Thunderstorm': 'Гроза \U000026A1',
            'Snow': 'Снег \U0001F328',
            'Mist': 'Туман \U0001F32B'
        }

        try:

            r = requests.get(
                f'https://api.openweathermap.org/data/2.5/weather?lat={m1}&lon={m2}&appid={weather_token}&units=metric')
            data = r.json()

            temp = data['main']['temp']
            humidity = data['main']['humidity']
            descriptions = data['weather'][0]['main']
            if descriptions in emodji:
                wd = emodji[descriptions]
            else:
                wd = 'Посмотри в окно'
            wind = data['wind']['speed']
            clouds = data['clouds']['all']
            lat = data['coord']['lat']
            lon = data['coord']['lon']

            await message.answer(
                f'Погодные улосвия на сегодня, по координатам: {lat} {lon} \nТемпература: {temp}C° {wd} \n'
                f'Влажность: {humidity}%\nСкорость ветра: {wind} м/c \nОблачность: {clouds}%')
        except:

            await message.answer('Данные введены не верно')

    await state.finish()



if __name__ == '__main__':
    executor.start_polling(dp)
