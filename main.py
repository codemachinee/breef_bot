import asyncio

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import BotCommand
from loguru import logger

from paswords import codemashine_test, loggs_acc, codemachinee_breef_bot
from FSM import (
    Breef,
    message_from_user,
    Get_admin,
    message_from_admin_chat,
    Message_from_admin,
    message_from_admin_text,
    rassylka,
    Rassylka,
)
from functions import clients_base
from google_sheets import get_sheet_base
from handlers import (
    check_callbacks,
    day_visitors,
    help,
    menu,
    post,
    sent_message,
    start, check_messages
)

logger.remove()
# Настраиваем логирование в файл с ограничением количества файлов
logger.add(
    "loggs.log",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    level="INFO",
    rotation="5 MB",  # Ротация файла каждые 10 MB
    retention="10 days",  # Хранить только 5 последних логов
    compression="zip",  # Сжимать старые логи в архив
    backtrace=True,     # Сохранение трассировки ошибок
    diagnose=True       # Подробный вывод
)

token = codemachinee_breef_bot
# token = codemashine_test

bot = Bot(token=token)
dp = Dispatcher()


dp.message.register(start, Command(commands='start'))
dp.message.register(help, Command(commands='help'))
dp.message.register(menu, Command(commands='menu'))
dp.message.register(post, Command(commands='post'))
dp.message.register(sent_message, Command(commands='sent_message'))
dp.message.register(day_visitors, Command(commands='day_visitors'))

dp.message.register(message_from_admin_chat, Message_from_admin.user_id)
dp.message.register(message_from_admin_text, Message_from_admin.message)
dp.message.register(rassylka, Rassylka.post)

dp.callback_query.register(check_callbacks, Breef.in_progress)
dp.callback_query.register(check_callbacks, F.data)
dp.message.register(check_messages, F.text, Breef.in_progress)
dp.message.register(message_from_user, Get_admin.message)


async def set_commands():
    commands = [
        BotCommand(command="start", description="запуск/перезапуск бота"),
        BotCommand(command="menu", description="главное функциональное меню"),
        BotCommand(command="help", description="справка по боту"),

    ]
    await bot.set_my_commands(commands)


async def main():
    try:
        logger.info('включение бота')
        sheet_base =  await get_sheet_base()
        await set_commands()
        await clients_base.load_base(await sheet_base.get_clients(bot))
        await dp.start_polling(bot)
    except Exception as e:
        logger.exception(f'Ошибка в боте: {e}')
    finally:
        await bot.send_message(loggs_acc, 'выключение бота')


if __name__ == '__main__':
    asyncio.run(main())
