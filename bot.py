# Подключаем модуль asyncio — он умеет делать несколько дел «одновременно»,
# как шеф-повар, который следит за несколькими кастрюлями сразу
import asyncio
# Подключаем base64 — он помогает прочитать тело webhook, если платформа прислала его в закодированном виде
import base64
# Подключаем json — он превращает текст webhook от Telegram в обычный словарь Python
import json
# Подключаем модуль logging — он записывает всё что делает программа, как дневник
import logging

# Из библиотеки aiogram берём два класса:
# Bot — это сам бот (он умеет отправлять сообщения),
# Dispatcher — «диспетчер», который решает какому обработчику передать каждое входящее сообщение
from aiogram import Bot, Dispatcher
# Из нашего файла config.py берём токен — это секретный ключ нашего бота,
# без него Telegram не пустит нас подключиться
from config import BOT_TOKEN

# Из файла start.py берём роутер и называем его start_router —
# он обрабатывает команду /start и кнопку «Играть снова»
from start import router as start_router
# Из файла game.py берём роутер и называем его game_router —
# он обрабатывает нажатия кнопок «Скам» и «Безопасно» во время игры
from game import router as game_router
# Из файла results.py берём роутер и называем его results_router —
# он показывает итоговый экран по завершении игры
from results import router as results_router

# Говорим системе логирования: показывай все сообщения уровня INFO и выше
# (обычная информация, предупреждения и ошибки) — будем видеть в консоли что происходит
logging.basicConfig(level=logging.INFO)


# Объявляем функцию, которая собирает диспетчер с роутерами
def create_dispatcher():
    # Создаём диспетчер — это «командный центр» входящих сообщений
    dp = Dispatcher()
    # Подключаем роутер старта
    dp.include_router(start_router)
    # Подключаем роутер игры
    dp.include_router(game_router)
    # Подключаем роутер результатов
    dp.include_router(results_router)
    # Возвращаем готовый диспетчер
    return dp


# Создаём общий диспетчер один раз, чтобы webhook и локальный запуск использовали одинаковые правила
dp = create_dispatcher()


# Объявляем функцию, которая достаёт update Telegram из события cloud-function
def _event_body_to_update(event):
    # Берём body из события, а если body нет — считаем событие уже готовым словарём update
    body = event.get("body", event)
    # Проверяем, не пришло ли тело запроса в base64
    if event.get("isBase64Encoded") and isinstance(body, str):
        # Раскодируем base64 обратно в обычный текст JSON
        body = base64.b64decode(body).decode("utf-8")
    # Проверяем, осталось ли тело строкой
    if isinstance(body, str):
        # Превращаем JSON-строку в словарь Python
        return json.loads(body or "{}")
    # Возвращаем body как есть, если это уже словарь
    return body


# Объявляем асинхронную функцию обработки одного webhook update
async def _handle_webhook(event):
    # Достаём update Telegram из события Sourcecraft/Yandex Cloud Function
    update = _event_body_to_update(event)
    # Если update пустой или не похож на update Telegram, спокойно завершаем обработку
    if not update or "update_id" not in update:
        # Ничего не возвращаем, потому что это не ошибка Telegram-бота
        return
    # Создаём объект бота с токеном
    bot = Bot(token=BOT_TOKEN)
    # Начинаем блок, чтобы сессия бота закрылась даже при ошибке
    try:
        # Передаём update в aiogram так, как будто Telegram прислал его напрямую
        await dp.feed_webhook_update(bot, update)
    # Блок finally выполнится всегда
    finally:
        # Закрываем сетевую сессию бота
        await bot.session.close()


# Объявляем функцию handler — именно её вызывает Sourcecraft/Yandex Cloud Function
def handler(event, context):
    # Начинаем безопасный блок обработки webhook
    try:
        # Запускаем асинхронную обработку webhook из обычной cloud-function функции
        asyncio.run(_handle_webhook(event))
    # Ловим любую ошибку, чтобы Sourcecraft получил понятный HTTP-ответ
    except Exception:
        # Записываем подробность ошибки в логи функции
        logging.exception("Failed to process Telegram webhook update")
        # Возвращаем Telegram статус ошибки
        return {"statusCode": 500, "body": "error"}
    # Возвращаем Telegram успешный ответ
    return {"statusCode": 200, "body": "ok"}


# Объявляем главную асинхронную функцию main — она запускает весь бот
# Слово async означает, что функция умеет «ждать» без зависания программы
async def main():
    # Создаём объект бота и передаём ему токен —
    # теперь бот знает под каким именем он работает в Telegram
    bot = Bot(token=BOT_TOKEN)
    # Говорим Telegram: удали все старые сообщения, которые пришли пока бот спал —
    # чтобы не обрабатывать их заново при следующем запуске
    await bot.delete_webhook(drop_pending_updates=True)

    # Выводим в консоль сообщение, что бот успешно запустился
    print("Бот запущен. Нажми Ctrl+C для остановки.")
    # Запускаем «поллинг» — бот начинает постоянно спрашивать Telegram:
    # «Есть новые сообщения?» и обрабатывает их через диспетчер
    await dp.start_polling(bot)


# Эта строка означает: «выполни следующий код только если запустили именно этот файл,
# а не импортировали его из другого файла»
if __name__ == "__main__":
    # Запускаем нашу асинхронную функцию main() через asyncio —
    # это как нажать кнопку «Пуск» для всего бота
    asyncio.run(main())
