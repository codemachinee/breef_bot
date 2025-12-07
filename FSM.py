from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from google_sheets import get_sheet_base
from paswords import admin_id


class Get_admin(StatesGroup):
    message = State()


class Message_from_admin(StatesGroup):
    user_id = State()
    message = State()


class Rassylka(StatesGroup):
    base = State()
    post = State()


class Breef(StatesGroup):
    in_progress = State()


async def message_from_user(message, state: FSMContext, bot):
    await bot.send_message(
        admin_id, f"Сообщение от пользователя @{message.from_user.username}:"
    )
    await bot.copy_message(admin_id, message.chat.id, message.message_id)
    await bot.send_message(message.chat.id, "Ваше сообщение отправлено ✅")
    await state.clear()


async def message_from_admin_chat(message, state: FSMContext, bot):
    if str.isdigit(message.text):
        await state.update_data(user_id=message.text)
        await bot.send_message(message.chat.id, "Введите сообщение")
        await state.set_state(Message_from_admin.message)
    else:
        await bot.send_message(
            message.chat.id,
            "Неверные данные... Повтори попытку используя цифры (Например: 1338281106)",
        )
        await state.set_state(Message_from_admin.user_id)


async def message_from_admin_text(message, state: FSMContext, bot):
    data = await state.get_data()
    user_id = data.get("user_id")
    await bot.copy_message(user_id, message.chat.id, message.message_id)
    await bot.send_message(message.chat.id, "Ваше сообщение отправлено ✅")
    await state.clear()


async def rassylka(message, bot, state: FSMContext):
    sheet_base = await get_sheet_base()
    await sheet_base.rasylka_v_bazu(bot, message)
    await state.clear()
