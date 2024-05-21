import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import F

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token="7133138529:AAFVdHFR4vlzWB5tQNMsouG4lLloV5vcy1w")
# Диспетчер
dp = Dispatcher()

# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет! Я был написан студентами группы Б9123-09.03.04.\n\nМеня создавали:\nВласова Валерия Владимировна\nПортнова Лидия Михайловна\nПапчук Елизавета Ибрагимовна\nМельничук Алиса Викторовна\nКозлова Кристина Викторовна\n\nДля просмотра функций отправьте /help")

@dp.message(Command("help"))
async def cmd_start(message: types.Message):
    await message.answer("Для того чтобы узнать информацию по теме Резервное копирование данных необходимо вежливо попросить об этом") 

# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())