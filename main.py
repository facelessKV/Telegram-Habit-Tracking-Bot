import logging
import sqlite3
import asyncio
from datetime import datetime
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Токен бота из BotFather
API_TOKEN = 'YOUR_BOT_TOKEN_HERE'

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Подключение к базе данных SQLite
conn = sqlite3.connect('habits.db')
cursor = conn.cursor()

# Создание необходимых таблиц
def init_db():
    """
    Инициализация базы данных: создание таблиц habits и completions.
    """
    # Таблица с привычками
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS habits (
        id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL,
        habit_name TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Таблица с отметками о выполнении
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS completions (
        id INTEGER PRIMARY KEY,
        habit_id INTEGER NOT NULL,
        completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (habit_id) REFERENCES habits (id)
    )
    ''')
    
    conn.commit()

# Определение состояний для машины состояний
class HabitStates(StatesGroup):
    add_habit = State()  # Состояние для добавления привычки
    select_habit = State()  # Состояние для выбора привычки из списка

# Обработчик команды /start
@dp.message(Command("start"))
async def cmd_start(message: Message):
    """
    Обработчик команды /start - приветствует пользователя.
    """
    await message.answer(
        "👋 Привет! Я бот для отслеживания привычек.\n\n"
        "Что я умею:\n"
        "• /add - Добавить новую привычку\n"
        "• /done - Отметить привычку как выполненную\n"
        "• /stats - Посмотреть статистику привычек"
    )

# Обработчик команды /add
@dp.message(Command("add"))
async def cmd_add(message: Message, state: FSMContext):
    """
    Обработчик команды /add - начинает процесс добавления привычки.
    """
    await state.set_state(HabitStates.add_habit)
    await message.answer("Введите название новой привычки, которую хотите отслеживать:")

# Обработчик ввода названия привычки
@dp.message(HabitStates.add_habit)
async def process_habit_name(message: Message, state: FSMContext):
    """
    Обработчик ввода названия привычки - сохраняет новую привычку в БД.
    """
    habit_name = message.text.strip()
    user_id = message.from_user.id
    
    # Проверка на пустое название
    if not habit_name:
        await message.answer("Название привычки не может быть пустым. Пожалуйста, введите название:")
        return
    
    # Добавление привычки в базу данных
    cursor.execute(
        "INSERT INTO habits (user_id, habit_name) VALUES (?, ?)",
        (user_id, habit_name)
    )
    conn.commit()
    
    # Сбрасываем состояние
    await state.clear()
    await message.answer(f"✅ Привычка '{habit_name}' успешно добавлена!")

# Функция для создания клавиатуры с привычками пользователя
def get_habits_keyboard(user_id: int):
    """
    Создает клавиатуру со списком привычек пользователя.
    Возвращает None, если у пользователя нет привычек.
    """
    cursor.execute(
        "SELECT id, habit_name FROM habits WHERE user_id = ?",
        (user_id,)
    )
    habits = cursor.fetchall()
    
    if not habits:
        return None
    
    # Формируем кнопки с привычками
    buttons = []
    for habit_id, habit_name in habits:
        buttons.append([
            InlineKeyboardButton(text=habit_name, callback_data=f"habit_{habit_id}")
        ])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)

# Обработчик команды /done
@dp.message(Command("done"))
async def cmd_done(message: Message, state: FSMContext):
    """
    Обработчик команды /done - предлагает выбрать привычку для отметки.
    """
    user_id = message.from_user.id
    keyboard = get_habits_keyboard(user_id)
    
    if not keyboard:
        await message.answer("У вас пока нет ни одной привычки. Добавьте с помощью /add")
        return
    
    await state.set_state(HabitStates.select_habit)
    await message.answer("Выберите привычку, которую вы выполнили:", reply_markup=keyboard)

# Обработчик нажатия на кнопку с привычкой
@dp.callback_query(F.data.startswith("habit_"))
async def process_habit_selection(callback: CallbackQuery, state: FSMContext):
    """
    Обработчик выбора привычки - отмечает привычку как выполненную.
    """
    current_state = await state.get_state()
    if current_state != HabitStates.select_habit.state:
        await callback.answer("Пожалуйста, используйте команду /done")
        return

    habit_id = int(callback.data.split("_")[1])
    
    # Получаем информацию о привычке
    cursor.execute("SELECT habit_name FROM habits WHERE id = ?", (habit_id,))
    result = cursor.fetchone()
    
    if not result:
        await callback.answer("Привычка не найдена.")
        await state.clear()
        return
    
    habit_name = result[0]
    
    # Добавляем запись о выполнении привычки
    cursor.execute(
        "INSERT INTO completions (habit_id) VALUES (?)",
        (habit_id,)
    )
    conn.commit()
    
    # Сбрасываем состояние
    await state.clear()
    await callback.message.answer(f"🎉 Отлично! Привычка '{habit_name}' отмечена как выполненная!")
    await callback.answer()

# Обработчик команды /stats
@dp.message(Command("stats"))
async def cmd_stats(message: Message):
    """
    Обработчик команды /stats - показывает статистику по привычкам.
    """
    user_id = message.from_user.id
    
    # Получаем статистику по привычкам
    cursor.execute("""
        SELECT h.habit_name, COUNT(c.id) as count
        FROM habits h
        LEFT JOIN completions c ON h.id = c.habit_id
        WHERE h.user_id = ?
        GROUP BY h.id
        ORDER BY count DESC
    """, (user_id,))
    
    habits_stats = cursor.fetchall()
    
    if not habits_stats:
        await message.answer("У вас пока нет ни одной привычки. Добавьте с помощью /add")
        return
    
    # Формируем ответ со статистикой
    response = "📊 Статистика ваших привычек:\n\n"
    
    for habit_name, count in habits_stats:
        response += f"• {habit_name}: выполнено {count} раз\n"
    
    await message.answer(response)

# Главная функция для запуска бота
async def main():
    """
    Главная функция - инициализирует БД и запускает бота.
    """
    # Инициализация базы данных
    init_db()
    
    # Запуск бота
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())