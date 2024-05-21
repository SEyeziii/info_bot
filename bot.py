import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram import F

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)

# Объект бота
bot = Bot(token="your token")

# Диспетчер
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Флаг состояния бота
bot_active = True

# Определяем состояния
class Form(StatesGroup):
    new_counter = State()

# Список сообщений для команды /new
messages = [
    "Внезапные сбои в оборудовании, вирусные атаки, случайное удаление файлов — все это может привести к невосполнимым потерям данных. Резервные копии страхуют вас от таких ситуаций, позволяя восстановить данные в случае необходимости.  /new",
    "Рекомендуется создавать резервные копии на отдельных носителях, отсоединенных от сети, чтобы предотвратить заражение вирусами и доступ злоумышленников к критической информации.  /new",
    "Некоторые программы резервного копирования позволяют вам сохранять несколько версий файлов. Это полезно для восстановления данных из определенного момента времени.  /new"
]

# Инициализируем состояние
async def on_startup(dispatcher: Dispatcher):
    await dispatcher.storage.set_state(chat_id=None, user_id=None, state=None)

# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    global bot_active
    if not bot_active:
        bot_active = True
        await message.answer("Бот активирован снова.")
    await state.set_state(Form.new_counter)
    await state.update_data(new_counter=0)
    await message.answer("Привет! Я был написан студентами группы Б9123-09.03.04.\n\nМеня создавали:\nВласова Валерия Владимировна\nПортнова Лидия Михайловна\nПапчук Елизавета Михайловна\nМельничук Алиса Викторовна\nКозлова Кристина Викторовна\n\nДля просмотра функций отправьте /help")

# Хэндлер на команду /help
@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    if bot_active:
        await message.answer("Для получения новой информации отправьте /new\nДля остановки нажмите /stop")
    else:
        await message.answer("Бот остановлен. Используйте команду /start для активации.")

# Хэндлер на команду /new
@dp.message(Command("new"))
async def cmd_new(message: types.Message, state: FSMContext):
    if not bot_active:
        await message.answer("Бот остановлен. Используйте команду /start для активации.")
        return

    data = await state.get_data()
    new_counter = data.get("new_counter", 0)

    if new_counter < len(messages):
        await message.answer(messages[new_counter])
        await state.update_data(new_counter=new_counter + 1)
    else:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Посетить сайт", url="https://github.com/SEyeziii")]
        ])
        await message.answer("Вы уже получили всю информацию. Вот ссылка:", reply_markup=keyboard)
# Хэндлер на команду /stop
@dp.message(Command("stop"))
async def cmd_stop(message: types.Message):
    global bot_active
    bot_active = False
    await message.answer("Бот остановлен. Используйте команду /start для активации.")
    
# Хэндлер для обработки сообщений, к которым бот не готов
@dp.message(F.text)
async def handle_unexpected_message(message: types.Message):
    if bot_active:
        await message.answer("Извините, я не понимаю это сообщение. Пожалуйста, используйте команды /help или /new.")
    else:
        await message.answer("Бот остановлен. Используйте команду /start для активации.")



# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot, on_startup=on_startup)

if __name__ == "__main__":
    asyncio.run(main())
