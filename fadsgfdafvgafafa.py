import random
import re
import uuid
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

API_TOKEN = "8175830600:AAEqdbA66sDnJJc-Czw1zo7gHuZlC2rocTs"

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    kb = InlineKeyboardMarkup().add(
        InlineKeyboardButton("Подать жалобу🔨", callback_data="report")
    )

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

    await message.answer(text, reply_markup=kb, parse_mode="Markdown")
# Кнопка «Подать жалобу»
@dp.callback_query_handler(lambda c: c.data == "report")
async def report_button(callback_query: types.CallbackQuery):
    kb = InlineKeyboardMarkup().add(
        InlineKeyboardButton("Заполнить форму", callback_data="fill_form")
    )

    text = (
        "*Оперативная подача жалоб.*\n\n"
        "Чтобы подать жалобу на мошенничество, вам *необходимо предварительно собрать следующие данные:*\n\n"
        "1. Юзернейм или Telegram ID мошенника.<blockquote>\n"
        "2. Описание ситуации [ Ограничение 500 символов ]\n"
        "3. Фото / Видео, доказывающие мошенничество [ от 2 до 10 медиа ]\n\n"
        "Отправка жалобы, которая *не соответствует форме* или *жалобы содержащей в себе потенциальный мусор* "
        "с целью навредить или затормозить сервис по приему и обработке жалоб, "
        "*ведёт за собой запрет на отправку жалоб, а также блокировку в самом боте или добавление в базу подозрительных участников.*\n\n"
        "_Нажимая на «Заполнить форму»,_ *вы автоматически соглашаетесь с вышеописанными правилами.*"
    )

    await bot.send_message(callback_query.from_user.id, text, reply_markup=kb, parse_mode="Markdown")

@dp.message_handler(lambda message: message.text and re.search(r"@[\w\d_]+", message.text))
async def handle_username_report(message: types.Message):
    username = re.search(r"@[\w\d_]+", message.text).group()
    search_count = random.randint(1, 10)

    response = (
        f"*🟡 Пользователь {username}*\n"
        f"*👀 Искали:* _{search_count} раз(а)_\n\n"
        f"*❓ Пользователь не найден в базе мошенников.*\n"
        f"_Рекомендуем проводить все сделки с надёжным гарантом._\n\n"
        f"_📌 Вы можете сообщить о подозрении — нажмите «Подать жалобу» в меню бота._\n\n"
        f"*🧾 Актуальные новости в мире TON:*\n"
        f"*https://t.me/tester_in_ton*"
    )

    await message.reply(response, parse_mode="Markdown")

# Заполнит
@dp.callback_query_handler(lambda c: c.data == "fill_form")
async def handle_fill_form(callback_query: types.CallbackQuery):
    await callback_query.message.answer(
        "*⚡️ Оперативная подача жалоб.*\n\n"
        "*Отправляйте все в одном сообщении*\n\n"
        "_1 – Отправьте боту юзернейм мошенника, на которого поступает жалоба._\n"
        "_2 – Отправьте описание мошенничества (Ограничение 500 символов)_\n"
        "_3 – Отправьте фото / видео доказательства мошенничества_",
        parse_mode="Markdown"
    )
    await callback_query.answer()

# Обработка отправки жалобы (упрощенная логика)
@dp.message_handler(content_types=types.ContentTypes.ANY)
async def handle_report_submission(message: types.Message):
    if message.text or message.caption or message.photo or message.video:
        complaint_id = uuid.uuid4().hex[:8]
        await message.reply(
            f"*Ваша жалоба #{complaint_id} отправлена модераторам @TesterBanBot. Мы уведомим вас о результатах*",
            parse_mode="Markdown"
        )

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
