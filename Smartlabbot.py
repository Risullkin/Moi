from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackContext,
    filters
)

TOKEN = "8058467033:AAE3BRIYlDj7rv0kbapyYwtgu8z4GpTfWvQ"

SUBJECTS = {
    "Математика": "📚 Математика: Алгебра, Геометрия, Подготовка к ЕГЭ.",
    "Русский": "📖 Русский язык: Грамматика, Сочинения, ОГЭ/ЕГЭ.",
    "Английский": "🌍 Английский: Разговорный, IELTS, TOEFL.",
    "Китайский": "🐉 Китайский: Иероглифы, HSK, Бизнес-курс.",
    "Химия": "⚗️ Химия: Органическая, Неорганическая, Олимпиады."
}

CONTACTS = """
📞 Контакты школы:
Телефон: +7 (XXX) XXX-XX-XX
Email: school@example.com
Адрес: г. Москва, ул. Образцова, 1
"""

REVIEWS = """
📢 Отзывы о школе:
1. ★★★★★ (Анна): "Отличные преподаватели!"
2. ★★★★☆ (Иван): "Хорошая атмосфера."
3. ★★★★★ (Мария): "Ребенок в восторге!"
"""

async def start(update: Update, context: CallbackContext):
    buttons = [["📚 Предметы", "📞 Контакты"], ["📢 Отзывы"]]
    markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    await update.message.reply_text("Добро пожаловать в онлайн-школу! Выберите опцию:", reply_markup=markup)

async def subjects(update: Update, context: CallbackContext):
    subjects_list = "\n".join([f"• {sub}" for sub in SUBJECTS.keys()])
    await update.message.reply_text(f"Доступные предметы:\n{subjects_list}\n\nНапишите название предмета, чтобы узнать подробности.")

async def contacts(update: Update, context: CallbackContext):
    await update.message.reply_text(CONTACTS)

async def reviews(update: Update, context: CallbackContext):
    await update.message.reply_text(REVIEWS)

async def handle_subject(update: Update, context: CallbackContext):
    subject = update.message.text
    if subject in SUBJECTS:
        await update.message.reply_text(SUBJECTS[subject])
    else:
        await update.message.reply_text("Такого предмета нет в списке.")

def main():
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.Regex("^📚 Предметы$"), subjects))
    application.add_handler(MessageHandler(filters.Regex("^📞 Контакты$"), contacts))
    application.add_handler(MessageHandler(filters.Regex("^📢 Отзывы$"), reviews))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_subject))

    application.run_polling()

if __name__ == "__main__":
    main()
