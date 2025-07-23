from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackContext, filters

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

REVIEWS_LIST = [
    "★★★★★ (Анна): Отличные преподаватели!",
    "★★★★☆ (Иван): Хорошая атмосфера.",
    "★★★★★ (Мария): Ребёнок в восторге!",
    "★★★☆☆ (Пётр): Нужно больше практики."
]

current_review_index = 0


# Главное меню
async def start(update: Update, context: CallbackContext):
    buttons = [["📚 Предметы", "📞 Контакты"], ["📢 Отзывы"]]
    markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    await update.message.reply_text(
        "Добро пожаловать в онлайн-школу! Выберите опцию:",
        reply_markup=markup
    )


# Показ предметов (кнопки)
async def show_subjects(update: Update, context: CallbackContext):
    buttons = [
                  [subject] for subject in SUBJECTS.keys()
              ] + [["Меню"]]
    markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    await update.message.reply_text(
        "Выберите предмет:",
        reply_markup=markup
    )


# Описание предмета
async def handle_subject(update: Update, context: CallbackContext):
    subject = update.message.text
    if subject in SUBJECTS:
        buttons = [["Меню"]]
        markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
        await update.message.reply_text(
            SUBJECTS[subject],
            reply_markup=markup
        )
    elif subject == "Меню":
        await start(update, context)
    else:
        await update.message.reply_text("Пожалуйста, выберите предмет из списка.")

async def contacts(update: Update, context: CallbackContext):
    await update.message.reply_text(CONTACTS)

async def handle_subject(update: Update, context: CallbackContext):
    subject = update.message.text
    if subject in SUBJECTS:
        await update.message.reply_text(SUBJECTS[subject])
    else:
        await update.message.reply_text("Такого предмета нет в списке.")


async def show_reviews(update: Update, context: CallbackContext):
    global current_review_index
    review = REVIEWS_LIST[current_review_index]
    buttons = [["Ещё", "Меню"]]
    markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    await update.message.reply_text(
        f"Отзыв {current_review_index + 1}/{len(REVIEWS_LIST)}:\n{review}",
        reply_markup=markup
    )


# Обработка кнопок "Ещё" и "Меню"
async def handle_review_buttons(update: Update, context: CallbackContext):
    global current_review_index
    user_choice = update.message.text

    if user_choice == "Ещё":
        current_review_index = (current_review_index + 1) % len(REVIEWS_LIST)
        await show_reviews(update, context)
    elif user_choice == "Меню":
        await start(update, context)

def main():
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.Regex("^📚 Предметы$"), show_subjects))
    application.add_handler(MessageHandler(filters.Regex("^📞 Контакты$"), contacts))
    application.add_handler(MessageHandler(filters.Regex("^📢 Отзывы$"), show_reviews))
    application.add_handler(MessageHandler(filters.Regex("^(Ещё|Меню)$"), handle_review_buttons))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_subject))

    application.run_polling()


if __name__ == "__main__":
    main()
