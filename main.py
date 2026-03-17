import telebot
from telebot import types
import os

TOKEN = os.getenv('BOT_TOKEN')
PAYMENT_TOKEN = os.getenv('PAYMENT_TOKEN')

bot = telebot.TeleBot(TOKEN)
FILE_NAME = 'guide.pdf'

@bot.message_handler(commands=['start'])
def start(message):
    # 1. Сначала отправляем ваш красивый текст
    welcome_text = (
        "Привет, красотка! 🌿\n\n"
        "Если ты здесь — скорее всего, тебе надоело. Надоело начинать заново. "
        "Надоело смотреть в зеркало и вздыхать. \n"
        "Сколько раз ты уже говорила себе «с понедельника»?\n"
        "5? 10? Потеряла счёт? 😅\n\n"
        "Я знаю, как это бывает:\n"
        "— диеты, которые работают ровно 3 дня\n"
        "— голодовки, после которых срываешься на всё подряд\n"
        "— обещания себе, которые тают вместе с мотивацией 😔\n\n"
        "А что если по-другому? Без голода, без мучений, без «буду есть траву»?\n"
        "🔥 **Гайд «Я выбираю себя» — всё, что тебе нужно для старта:**\n"
        "✅ 20 рецептов с фото и расчетами\n"
        "✅ 28 дней готового меню (завтрак, обед, ужин, перекус)\n"
        "✅ План на случай срыва\n"
        "✅ Фитнес для тех, кто в танке\n"
        "✅ Гид по выживанию в общепите\n"
        "✅ Психология еды и магия лимфодренажа\n"
        "✅ Мотивация: подборка фильмов\n\n"
        "Ты уже потратила достаточно времени на «потом». Пора попробовать «сейчас». 💪\n"
        "Один раз купила — используешь всю жизнь.\n\n"
        "👇 Жми — и погнали!"
    )
    
    bot.send_message(message.chat.id, welcome_text, parse_mode="Markdown")

    # 2. Сразу следом отправляем счет (Invoice) без лишних кнопок
    bot.send_invoice(
        message.chat.id, 
        "Гайд «Я выбираю себя»", 
        "Доступ к полной программе питания и тренировок.",
        "payload", 
        PAYMENT_TOKEN, 
        "RUB",         
        [types.LabeledPrice("Гайд", 39900)], # 399 рублей
        start_parameter="diet_guide"
    )

@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout(query):
    bot.answer_pre_checkout_query(query.id, ok=True)

@bot.message_handler(content_types=['successful_payment'])
def success_pay(message):
    bot.send_message(message.chat.id, "✅ Оплата прошла успешно! Лови свой гайд:")
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, 'rb') as f:
            bot.send_document(message.chat.id, f, caption="Твой гайд готов! Начинаем преображение. 🚀")

if __name__ == "__main__":
    bot.infinity_polling()
