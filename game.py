# Модуль html нужен, чтобы безопасно показывать текст сообщений в режиме HTML
from html import escape
# ИЗМЕНЕНИЕ team_2: Модуль asyncio нужен, чтобы запускать таймер вопроса без остановки всего бота
import asyncio
# ИЗМЕНЕНИЕ team_2: Модуль time нужен, чтобы точно считать секунды ответа через monotonic()
import time

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
# ИЗМЕНЕНИЕ team_2: Из config.py берём лимит времени и максимум очков за один ответ
from config import ANSWER_TIME_LIMIT, MAX_POINTS_PER_ANSWER

# Создаём объект роутера для этого файла — он будет «хранить» все обработчики ниже
router = Router()


# Объявляем асинхронную функцию:
# message — объект сообщения (куда отправлять вопрос),
# session — словарь с текущим состоянием игры,
# state — блокнот FSM, куда нужно сохранить время старта вопроса
async def send_question(message, session, state):
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
    # ИЗМЕНЕНИЕ team_2: Запоминаем точное время, когда текущий вопрос появился у игрока
    session["question_started_at"] = time.monotonic()
    # ИЗМЕНЕНИЕ team_2: Увеличиваем номер таймера, чтобы старые таймеры не трогали новый вопрос
    session["question_token"] += 1
    # ИЗМЕНЕНИЕ team_2: Сохраняем номер таймера в отдельную переменную для фоновой проверки
    question_token = session["question_token"]
    # ИЗМЕНЕНИЕ team_2: Сохраняем номер игровой сессии, чтобы таймер старой игры не влиял на перезапуск
    session_id = session["session_id"]
    # ИЗМЕНЕНИЕ team_2: Записываем обновлённую сессию в FSM перед отправкой вопроса
    await state.update_data(session=session)

    # Экранируем текст кейса, чтобы символы <, > и & не ломали HTML-разметку Telegram
    case_text = escape(case["text"])

    # Формируем текст вопроса — большая строка с разными данными
    text = (
        # Заголовок: номер вопроса, жизни и очки в одну строку
        f"❓ <b>Вопрос {num}/{total}</b>   ❤️ {lives}   ⭐ {score}   ⏱ {ANSWER_TIME_LIMIT} сек.\n"
        # Горизонтальная линия-разделитель из символов
        "━━━━━━━━━━━━━━━━━━━━━━\n\n"
        # Подпись перед текстом задания
        "📩 <b>Сообщение:</b>\n\n"
        # Сам текст вопроса — сообщение, которое надо проанализировать
        f"{case_text}"
    )
    # Отправляем текст вопроса с кнопками «Скам» и «Безопасно»;
    # parse_mode="HTML" — разрешаем теги жирного текста
    sent_message = await message.answer(text, parse_mode="HTML", reply_markup=answer_keyboard())
    # ИЗМЕНЕНИЕ team_2: Запускаем фоновую задачу, которая сработает, если игрок не ответит вовремя
    asyncio.create_task(handle_question_timeout(sent_message, state, session_id, question_token))


# ИЗМЕНЕНИЕ team_2: Объявляем асинхронную функцию, которая ждёт лимит времени и завершает вопрос при молчании игрока
async def handle_question_timeout(message, state, session_id, question_token):
    """
    Следит за одним конкретным вопросом.

    Если игрок не ответил за ANSWER_TIME_LIMIT секунд, функция снимает жизнь,
    убирает кнопки и переводит игру к следующему вопросу или итогам.
    """
    # ИЗМЕНЕНИЕ team_2: Ждём столько секунд, сколько разрешено настройкой ANSWER_TIME_LIMIT
    await asyncio.sleep(ANSWER_TIME_LIMIT)
    # ИЗМЕНЕНИЕ team_2: Проверяем текущее состояние, потому что игрок мог нажать «Стоп» или закончить игру
    current_state = await state.get_state()
    # ИЗМЕНЕНИЕ team_2: Если игра уже не идёт, таймер ничего не делает
    if current_state != GameStates.playing.state:
        # ИЗМЕНЕНИЕ team_2: Выходим из функции без штрафа
        return
    # ИЗМЕНЕНИЕ team_2: Читаем свежие данные пользователя из FSM
    data = await state.get_data()
    # ИЗМЕНЕНИЕ team_2: Достаём игровую сессию, если она ещё существует
    session = data.get("session")
    # ИЗМЕНЕНИЕ team_2: Если сессии нет, значит таймер уже не нужен
    if session is None:
        # ИЗМЕНЕНИЕ team_2: Выходим из функции без действий
        return
    # ИЗМЕНЕНИЕ team_2: Проверяем, что таймер относится именно к текущей игре
    if session.get("session_id") != session_id:
        # ИЗМЕНЕНИЕ team_2: Старый таймер игнорируется
        return
    # ИЗМЕНЕНИЕ team_2: Проверяем, что таймер относится именно к текущему вопросу
    if session.get("question_token") != question_token:
        # ИЗМЕНЕНИЕ team_2: Старый таймер игнорируется
        return
    # ИЗМЕНЕНИЕ team_2: Увеличиваем номер таймера, чтобы этот вопрос нельзя было обработать второй раз
    session["question_token"] += 1
    # ИЗМЕНЕНИЕ team_2: Очищаем время старта, потому что этот вопрос уже закрыт
    session["question_started_at"] = None
    # ИЗМЕНЕНИЕ team_2: Убираем кнопки у вопроса, потому что время ответа закончилось
    await message.edit_reply_markup()
    # ИЗМЕНЕНИЕ team_2: Снимаем одну жизнь за пропущенный вопрос
    session["lives"] -= 1
    # ИЗМЕНЕНИЕ team_2: Переводим игру на следующий вопрос
    session["question_num"] += 1
    # ИЗМЕНЕНИЕ team_2: Сохраняем обновлённую сессию
    await state.update_data(session=session)
    # ИЗМЕНЕНИЕ team_2: Сообщаем игроку, что время вышло
    await message.answer("⏰ <b>Время вышло!</b>\n\nОтвет не засчитан, снята 1 жизнь.", parse_mode="HTML")
    # ИЗМЕНЕНИЕ team_2: Проверяем, закончилась ли игра после потери жизни или последнего вопроса
    game_over = (session["lives"] == 0) or (session["question_num"] >= session["total"])
    # ИЗМЕНЕНИЕ team_2: Если игра закончилась, показываем итоги
    if game_over:
        # ИЗМЕНЕНИЕ team_2: Переводим состояние в финальное
        await state.set_state(GameStates.game_over)
        # ИЗМЕНЕНИЕ team_2: Импортируем итоговый экран внутри функции, чтобы не создавать круг импортов
        from results import show_results
        # ИЗМЕНЕНИЕ team_2: Показываем итоговый экран
        await show_results(message, session)
    # ИЗМЕНЕНИЕ team_2: Если игра продолжается, показываем следующий вопрос
    else:
        # ИЗМЕНЕНИЕ team_2: Отправляем следующий вопрос и запускаем новый таймер
        await send_question(message, session, state)


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
    # ИЗМЕНЕНИЕ team_2: Увеличиваем номер таймера сразу, чтобы фоновая задача не обработала этот же вопрос второй раз
    session["question_token"] += 1

    # Определяем ответ игрока:
    # если нажали "scam" — True (считает скамом), если "safe" — False (считает безопасным)
    # Сравнение (==) само возвращает булево значение True или False
    player_answer = (callback.data == "scam")

    # Достаём словарь с текущим вопросом (содержит text, is_scam, explanation)
    case = get_current_case(session)
    # ИЗМЕНЕНИЕ team_2: Достаём время, когда вопрос был показан игроку
    question_started_at = session.get("question_started_at")
    # ИЗМЕНЕНИЕ team_2: Если время почему-то не записалось, считаем, что лимит уже истёк
    if question_started_at is None:
        # ИЗМЕНЕНИЕ team_2: Ставим ноль оставшихся секунд
        seconds_left = 0
    # ИЗМЕНЕНИЕ team_2: Если время записано нормально, считаем оставшиеся секунды
    else:
        # ИЗМЕНЕНИЕ team_2: Считаем, сколько секунд прошло после показа вопроса
        elapsed = time.monotonic() - question_started_at
        # ИЗМЕНЕНИЕ team_2: Считаем, сколько секунд осталось из лимита
        seconds_left = int(ANSWER_TIME_LIMIT - elapsed)
    # ИЗМЕНЕНИЕ team_2: Очищаем время старта, потому что вопрос уже получает ответ
    session["question_started_at"] = None
    # ИЗМЕНЕНИЕ team_2: Если время уже вышло, ответ считаем неправильным без начисления очков
    if seconds_left <= 0:
        # ИЗМЕНЕНИЕ team_2: Снимаем жизнь за ответ после истечения времени
        session["lives"] -= 1
        # ИЗМЕНЕНИЕ team_2: Готовим текст результата для игрока
        result_text = "⏰ <b>Время вышло!</b>\n\nОтвет не засчитан, снята 1 жизнь."
    # ИЗМЕНЕНИЕ team_2: Если время ещё есть, ответ проверяется обычной логикой
    else:
        # ИЗМЕНЕНИЕ team_2: Ограничиваем очки максимумом, даже если осталось больше 10 секунд
        points_for_answer = min(MAX_POINTS_PER_ANSWER, seconds_left)
        # ИЗМЕНЕНИЕ team_2: Проверяем ответ и начисляем рассчитанные очки только при правильном ответе
        result_text, session = process_answer(player_answer, case, session, points_for_answer)

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
        await send_question(callback.message, session, state)


# ИЗМЕНЕНИЕ team_1: Обработчик кнопки «Стоп» работает только во время игры
@router.callback_query(GameStates.playing, lambda c: c.data == "stop_game")
# ИЗМЕНЕНИЕ team_1: Объявляем функцию, которая завершает текущую игру досрочно
async def handle_stop_game(callback, state):
    """
    Останавливает игру по кнопке «Стоп» и показывает текущий результат.
    """
    # ИЗМЕНЕНИЕ team_1: Подтверждаем Telegram, что нажатие кнопки получено
    await callback.answer()
    # ИЗМЕНЕНИЕ team_1: Убираем кнопки у текущего вопроса
    await callback.message.edit_reply_markup()
    # ИЗМЕНЕНИЕ team_1: Читаем данные пользователя из FSM
    data = await state.get_data()
    # ИЗМЕНЕНИЕ team_1: Достаём текущую игровую сессию
    session = data["session"]
    # ИЗМЕНЕНИЕ team_2: Увеличиваем токен, чтобы старый таймер вопроса больше не сработал
    session["question_token"] += 1
    # ИЗМЕНЕНИЕ team_2: Очищаем время старта, потому что игра остановлена
    session["question_started_at"] = None
    # ИЗМЕНЕНИЕ team_1: Сохраняем сессию перед показом итогов
    await state.update_data(session=session)
    # ИЗМЕНЕНИЕ team_1: Переводим игру в состояние завершения
    await state.set_state(GameStates.game_over)
    # ИЗМЕНЕНИЕ team_1: Импортируем итоговый экран здесь, чтобы избежать круговых импортов
    from results import show_results
    # ИЗМЕНЕНИЕ team_1: Показываем итоговый экран с кнопкой «Играть снова»
    await show_results(callback.message, session)


# ИЗМЕНЕНИЕ team_1: Обработчик кнопки «Перезапуск» работает только во время игры
@router.callback_query(GameStates.playing, lambda c: c.data == "restart_game")
# ИЗМЕНЕНИЕ team_1: Объявляем функцию, которая сбрасывает текущую игру и сразу запускает новую
async def handle_restart_game(callback, state):
    """
    Перезапускает игру по кнопке «Перезапуск».
    """
    # ИЗМЕНЕНИЕ team_1: Подтверждаем Telegram, что нажатие кнопки получено
    await callback.answer()
    # ИЗМЕНЕНИЕ team_1: Убираем кнопки у старого вопроса
    await callback.message.edit_reply_markup()
    # ИЗМЕНЕНИЕ team_1: Импортируем создание новой сессии здесь, чтобы не усложнять верх файла
    from session import new_session
    # ИЗМЕНЕНИЕ team_1: Создаём полностью новую игровую сессию
    session = new_session()
    # ИЗМЕНЕНИЕ team_1: Сохраняем новую сессию в FSM
    await state.update_data(session=session)
    # ИЗМЕНЕНИЕ team_1: Оставляем состояние «игра идёт»
    await state.set_state(GameStates.playing)
    # ИЗМЕНЕНИЕ team_1: Сообщаем игроку, что игра началась заново
    await callback.message.answer("🔁 Игра перезапущена. Начинаем заново!")
    # ИЗМЕНЕНИЕ team_1: Показываем первый вопрос новой игры
    await send_question(callback.message, session, state)
