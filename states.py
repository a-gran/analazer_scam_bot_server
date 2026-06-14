# Из aiogram берём два класса:
# State — описывает одно конкретное состояние (например «игра идёт»),
# StatesGroup — группа состояний, как папка в которой они все хранятся
from aiogram.fsm.state import State, StatesGroup


# Создаём класс GameStates — группа всех возможных состояний нашей игры
# Наследуемся от StatesGroup, чтобы aiogram умел с ним работать
class GameStates(StatesGroup):
    # Игра идёт — бот ждёт нажатия кнопки «Скам» или «Безопасно»
    playing = State()
    # Игра закончена — бот показал итоги и ждёт нажатия «Играть снова» или /start
    game_over = State()
