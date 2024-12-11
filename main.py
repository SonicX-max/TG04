import asyncio
import ssl
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import TOKEN

# Ensure SSL is loaded
try:
    ssl.create_default_context()
except Exception as e:
    print("SSL module is not available. Please ensure it is correctly installed.", e)

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Команда /start
@dp.message(Command("start"))
async def start(message: Message):
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="Привет"), types.KeyboardButton(text="Пока")]
        ],
        resize_keyboard=True
    )
    await message.answer(f"Привет, {message.from_user.first_name}! Я бот.", reply_markup=keyboard)

# Обработка кнопок "Привет" и "Пока"
@dp.message(lambda msg: msg.text == "Привет")
async def handle_hello(message: Message):
    await message.answer(f"Привет, {message.from_user.first_name}!")

@dp.message(lambda msg: msg.text == "Пока")
async def handle_goodbye(message: Message):
    await message.answer(f"До свидания, {message.from_user.first_name}!")

# Команда /links
@dp.message(Command("links"))
async def links(message: Message):
    print("Команда /links вызвана")
    keyboard = InlineKeyboardBuilder()
    keyboard.add(types.InlineKeyboardButton(text="Новости", url="https://news.ycombinator.com"))
    keyboard.add(types.InlineKeyboardButton(text="Музыка", url="https://open.spotify.com"))
    keyboard.add(types.InlineKeyboardButton(text="Видео", url="https://www.youtube.com"))
    await message.answer("Выберите ссылку:", reply_markup=keyboard.as_markup())

# Команда /dynamic
@dp.message(Command("dynamic"))
async def dynamic(message: Message):
    print("Команда /dynamic вызвана")
    keyboard = InlineKeyboardBuilder()
    keyboard.add(types.InlineKeyboardButton(text="Показать больше", callback_data="show_more"))
    await message.answer("Динамическое меню:", reply_markup=keyboard.as_markup())

# Обработка динамических кнопок
@dp.callback_query()
async def handle_dynamic(callback: CallbackQuery):
    print(f"Получен callback: {callback.data}")
    if callback.data == "show_more":
        keyboard = InlineKeyboardBuilder()
        keyboard.add(types.InlineKeyboardButton(text="Опция 1", callback_data="option_1"))
        keyboard.add(types.InlineKeyboardButton(text="Опция 2", callback_data="option_2"))
        await callback.message.edit_text("Выберите опцию:", reply_markup=keyboard.as_markup())
    elif callback.data == "option_1":
        await callback.message.answer("Вы выбрали Опция 1")
    elif callback.data == "option_2":
        await callback.message.answer("Вы выбрали Опция 2")

# Установка команд в меню
async def set_commands():
    commands = [
        types.BotCommand(command="start", description="Приветственное сообщение"),
        types.BotCommand(command="links", description="Показать ссылки"),
        types.BotCommand(command="dynamic", description="Динамическое меню")
    ]
    await bot.set_my_commands(commands)

# Главная функция
async def main():
    print("Запуск бота...")
    await set_commands()
    print("Установка команд...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())