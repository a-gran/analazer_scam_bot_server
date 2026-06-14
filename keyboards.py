# Из aiogram берём два класса:
# InlineKeyboardMarkup — вся клавиатура целиком (список строк с кнопками),
# InlineKeyboardButton — одна отдельная кнопка на этой клавиатуре
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# Функция создаёт клавиатуру с двумя кнопками — появляется под каждым вопросом
# Кнопки расположены в одну строку рядом друг с другом
def answer_keyboard():
    """Клавиатура с двумя кнопками — появляется под каждым вопросом."""
    # Создаём и сразу возвращаем клавиатуру
    # inline_keyboard — это список строк, каждая строка — список кнопок
    # Здесь одна строка с двумя кнопками рядом
    return InlineKeyboardMarkup(inline_keyboard=[[
        # Первая кнопка с текстом «Скам»
        # callback_data="scam" — тайное слово, которое бот получит при нажатии этой кнопки
        InlineKeyboardButton(text="🚨 Скам",       callback_data="scam"),
        # Вторая кнопка с текстом «Безопасно»
        # callback_data="safe" — тайное слово для этой кнопки
        InlineKeyboardButton(text="✅ Безопасно",  callback_data="safe"),
    ]])


# Функция создаёт клавиатуру с одной кнопкой — появляется на итоговом экране
def play_again_keyboard():
    """Клавиатура с одной кнопкой — появляется на итоговом экране."""
    # Одна строка с одной кнопкой «Играть снова»
    return InlineKeyboardMarkup(inline_keyboard=[[
        # Кнопка «Играть снова»
        # callback_data="play_again" — тайное слово, бот узнает что игрок хочет начать заново
        InlineKeyboardButton(text="🔄 Играть снова", callback_data="play_again"),
    ]])


# Функция создаёт клавиатуру с одной кнопкой — появляется после показа правил
# callback_data "play_again" намеренно совпадает с кнопкой «Играть снова»,
# чтобы один обработчик в handlers/start.py работал для обоих случаев
def start_keyboard():
    """Клавиатура с одной кнопкой — появляется после показа правил."""
    # Одна строка с одной кнопкой «Начать игру»
    return InlineKeyboardMarkup(inline_keyboard=[[
        # Кнопка «Начать игру» — намеренно используем то же тайное слово "play_again",
        # что и у кнопки «Играть снова», чтобы один обработчик покрывал оба случая
        InlineKeyboardButton(text="▶️ Начать игру", callback_data="play_again"),
    ]])
