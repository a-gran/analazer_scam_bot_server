# Модуль html нужен, чтобы безопасно показывать текст сообщений в режиме HTML
from html import escape

# Router — маршрутизатор, который собирает все обработчики этого файла
from aiogram import Router
# Message — текстовое сообщение, CallbackQuery — нажатие на inline-кнопку
from aiogram.types import Message, CallbackQuery
# FSMContext — блокнот бота с состоянием и данными конкретного пользователя
from aiogram.fsm.context import FSMContext

# Наши состояния игры из states.py
from states import GameStates
# Функция из keyboards.py, которая создаёт кнопки «Скам» и «Безопасно»
from keyboards import answer_keyboard
# Функция из answer.py — проверяет ответ игрока и обновляет счёт/жизни
from answer import process_answer
# Функция из session.py — возвращает текущий вопрос из сессии
from session import get_current_case

# Создаём объект роутера для этого файла — он будет «хранить» все обработчики ниже
router = Router()


# Объявляем асинхронную функцию:
# message — объект сообщения (куда отправлять вопрос),
# session — словарь с текущим состоянием игры
async def send_question(message, session):
    """
    Формирует текст одного вопроса и отправляет его пользователю с кнопками.

    Берёт текущий вопрос через get_current_case() и показывает:
        - прогресс (номер вопроса / всего)
        - жизни и очки
        - текст сообщения для анализа
    """
    # Получаем текущий вопрос из сессии;
    # если вопросы закончились — функция вернёт None
    case = get_current_case(session)
    # Проверяем: если вопросов больше нет — просто выходим из функции
    # (handle_answer сам обработает этот случай через проверку game_over)
    if case is None:
        return

    # Вычисляем номер вопроса для отображения:
    # +1 потому что question_num — это индекс (счёт с нуля), а людям удобнее счёт с единицы
    num = session["question_num"] + 1
    # Берём из сессии общее количество вопросов в этой игре
    total = session["total"]
    # Берём из сессии текущее количество жизней
    lives = session["lives"]
    # Берём из сессии текущее количество очков
    score = session["score"]

    # Экранируем текст кейса, чтобы символы <, > и & не ломали HTML-разметку Telegram
    case_text = escape(case["text"])

    # Формируем текст вопроса — большая строка с разными данными
    text = (
        # Заголовок: номер вопроса, жизни и очки в одну строку
        f"❓ <b>Вопрос {num}/{total}</b>   ❤️ {lives}   ⭐ {score}\n"
        # Горизонтальная линия-разделитель из символов
        "━━━━━━━━━━━━━━━━━━━━━━\n\n"
        # Подпись перед текстом задания
        "📩 <b>Сообщение:</b>\n\n"
        # Сам текст вопроса — сообщение, которое надо проанализировать
        f"{case_text}"
    )
    # Отправляем текст вопроса с кнопками «Скам» и «Безопасно»;
    # parse_mode="HTML" — разрешаем теги жирного текста
    await message.answer(text, parse_mode="HTML", reply_markup=answer_keyboard())


# Декоратор с двумя фильтрами одновременно:
# 1) GameStates.playing — реагируем только пока игра в процессе
# 2) lambda — реагируем только если нажата кнопка "scam" или "safe"
@router.callback_query(GameStates.playing, lambda c: c.data in ("scam", "safe"))
# Объявляем обработчик ответа:
# callback — нажатая кнопка (в ней есть callback.data и callback.message),
# state — блокнот состояния пользователя
async def handle_answer(callback, state):
    """
    Обрабатывает нажатие кнопки «Скам» или «Безопасно».

    Шаги:
        1. Убираем кнопки с вопроса (edit_reply_markup)
        2. Читаем сессию из FSM
        3. Определяем ответ игрока: "scam" → True, "safe" → False
        4. Вызываем process_answer() — она возвращает текст результата + обновлённые данные
        5. Отправляем результат игроку
        6. Если игра закончена — переходим к результатам
        7. Иначе — увеличиваем question_num и показываем следующий вопрос
    """
    # Убираем «часики» на кнопке — обязательное подтверждение Telegram что нажатие получено
    await callback.answer()
    # Убираем кнопки «Скам»/«Безопасно» с вопроса —
    # чтобы нельзя было нажать ещё раз на тот же вопрос
    await callback.message.edit_reply_markup()

    # Читаем всё что хранится в блокноте для этого пользователя — возвращает словарь
    data = await state.get_data()
    # Достаём из словаря нашу игровую сессию по ключу "session"
    session = data["session"]

    # Определяем ответ игрока:
    # если нажали "scam" — True (считает скамом), если "safe" — False (считает безопасным)
    # Сравнение (==) само возвращает булево значение True или False
    player_answer = (callback.data == "scam")

    # Достаём словарь с текущим вопросом (содержит text, is_scam, explanation)
    case = get_current_case(session)

    # Вызываем логику проверки ответа:
    # функция проверяет правильность, обновляет очки/жизни в сессии
    # и возвращает сразу два значения — текст объяснения и обновлённую сессию
    result_text, session = process_answer(player_answer, case, session)

    # Отправляем игроку текст с результатом: «Правильно!» или «Неправильно!» и объяснение
    await callback.message.answer(result_text, parse_mode="HTML")

    # Увеличиваем индекс текущего вопроса на 1 — переключаемся на следующий вопрос
    session["question_num"] += 1

    # Записываем обновлённую сессию обратно в блокнот FSM — чтобы изменения сохранились
    await state.update_data(session=session)

    # Проверяем условия завершения игры:
    # игра закончена если жизней больше нет ИЛИ все вопросы уже показаны
    game_over = (session["lives"] == 0) or (session["question_num"] >= session["total"])

    # Если игра закончилась...
    if game_over:
        # Переключаем состояние на «игра завершена» —
        # кнопки «Скам»/«Безопасно» больше не будут работать
        await state.set_state(GameStates.game_over)
        # Импортируем функцию show_results здесь (внутри функции), а не вверху файла —
        # это нужно чтобы избежать «замкнутого круга» импортов между файлами
        from results import show_results
        # Вызываем функцию показа итогов — она отправит финальный экран с результатами
        await show_results(callback.message, session)
    # Если игра ещё продолжается...
    else:
        # Вызываем send_question — она покажет следующий вопрос из сессии
        await send_question(callback.message, session)
