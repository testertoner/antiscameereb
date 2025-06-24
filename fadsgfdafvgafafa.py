import asyncio
import random
import re
import uuid
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from aiogram.enums import ParseMode
from aiogram.fsm.strategy import FSMStrategy
from aiogram.router import Router

API_TOKEN = "8175830600:AAEqdbA66sDnJJc-Czw1zo7gHuZlC2rocTs"

bot = Bot(token=API_TOKEN, parse_mode=ParseMode.MARKDOWN)
dp = Dispatcher()
router = Router()

# /start
@router.message(lambda msg: msg.text and msg.text.startswith("/start"))
async def start_command(message: Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Подать жалобу🔨", callback_data="report")]
    ])
    text = (
        "*Это лучший анти-скам проект* на рынке TG\n\n"
        "*Что ты можешь сделать в личке бота*\n\n"
        "_╙ Отправить @username_\n\n"
        "*Что отправит бот в ответ*\n\n"
        "_╟ ID пользователя_\n"
        "_╟ Наличие в скам базе_\n"
        "_╟ Наличие в базе проверенных исполнителей_\n"
        "_╙ Наличие в базе ТОП Гарантов_\n\n"
        "*╓ Есть жалоба на мошенника?*\n"
        "*╙ Скорее жми на «Подать жалобу»*"
    )
    await message.answer(text, reply_markup=kb)

# Кнопка "Подать жалобу"
@router.callback_query(lambda c: c.data == "report")
async def report_button(callback: CallbackQuery):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Заполнить форму", callback_data="fill_form")]
    ])
    text = (
        "*Оперативная подача жалоб.*\n\n"
        "Чтобы подать жалобу на мошенничество, вам *необходимо предварительно собрать следующие данные:*\n\n"
        "> 1. Юзернейм или Telegram ID мошенника.\n"
        "> 2. Описание ситуации [ Ограничение 500 символов ]\n"
        "> 3. Фото / Видео, доказывающие мошенничество [ от 2 до 10 медиа ]\n\n"
        "Отправка жалобы, которая *не соответствует форме* или *жалобы содержащей в себе потенциальный мусор* "
        "с целью навредить или затормозить сервис по приему и обработке жалоб, "
        "*ведёт за собой запрет на отправку жалоб, а также блокировку в самом боте или добавление в базу подозрительных участников.*\n\n"
        "_Нажимая на «Заполнить форму»,_ *вы автоматически соглашаетесь с вышеописанными правилами.*"
    )
    await callback.message.answer(text, reply_markup=kb)
    await callback.answer()

# Кнопка "Заполнить форму"
@router.callback_query(lambda c: c.data == "fill_form")
async def fill_form(callback: CallbackQuery):
    text = (
        "*⚡️ Оперативная подача жалоб.*\n\n"
        "*Отправляйте все в одном сообщении*\n\n"
        "_1 – Отправьте боту юзернейм мошенника, на которого поступает жалоба._\n"
        "_2 – Отправьте описание мошенничества (Ограничение 500 символов)_\n"
        "_3 – Отправьте фото / видео доказательства мошенничества_"
    )
    await callback.message.answer(text)
    await callback.answer()

# Поиск по username
@router.message(lambda msg: msg.text and re.search(r"@[\w\d_]+", msg.text))
async def handle_username_report(message: Message):
    username = re.search(r"@[\w\d_]+", message.text).group()
    search_count = random.randint(1, 10)

    response = (
        f"*🟡 Пользователь {username}*\n"
        f"*👀 Искали:* _{search_count} раз(а)_\n\n"
        f"*❓ Пользователь не найден в базе мошенников.*\n"
        f"_Рекомендуем проводить все сделки с надёжным гарантом._\n\n"
        f"_📌 Вы можете сообщить о подозрении — нажмите «Подать жалобу» в меню бота._\n\n"
        f"*🧾 Актуальные новости в мире TON:*\n"
        f"https://t.me/tester_in_ton"
    )

    await message.answer(response)

# Обработка жалобы
@router.message()
async def handle_report_submission(message: Message):
    if message.text or message.caption or message.photo or message.video:
        complaint_id = uuid.uuid4().hex[:8]
        await message.answer(
            f"*Ваша жалоба #{complaint_id} отправлена модераторам @TesterBanBot. Мы уведомим вас о результатах*"
        )

# Основной запуск
async def main():
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
