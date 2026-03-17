import telebot
from telebot import types
import os

# Бот тянет ключи из "Переменных окружения" Bothost
TOKEN = os.getenv('BOT_TOKEN')
PAYMENT_TOKEN = os.getenv('PAYMENT_TOKEN')

bot = telebot.TeleBot(TOKEN)
# Название твоего файла с гайдом
FILE_NAME = 'guide.pdf'

@bot.message_handler(commands=['start'])
def start(message):
    welcome_text = (
        "Привет, красотка! 🌿\n"
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
        "✅ 20 рецептов с фото и подробными расчетами\n"
        "✅ 28 дней готового меню (завтрак, обед, ужин, перекус)\n"
        "✅ План на случай срыва (потому что он будет — и это ок)\n"
        "✅ Фитнес для тех, кто в танке: 5 упражнений для кровати\n"
        "✅ Гид по выживанию в общепите без майонезных шуб\n"
        "✅ Психология еды и магия лимфодренажа от отеков\n"
        "✅ Мотивация: подборка фильмов и правильных установок\n\n"
        "Ты уже потратила достаточно времени на «потом». Пора попробовать «сейчас». 💪\n"
        "Один раз купила — используешь всю жизнь.\n\n"
        "👇 Жми — и погнали!"
    )

    markup = types.InlineKeyboardMarkup()
    btn_pay = types.InlineKeyboardButton("💳 Оплатить и получить гайд (399 руб.)", callback_data='buy')
    markup.add(btn_pay)
    
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == 'buy')
def send_invoice(call):
    # Выставляем счет в рублях через ЮKassa
    bot.send_invoice(
        call.message.chat.id, 
        "Гайд «Я выбираю себя»", 
        "diet_guide_payload", 
        PAYMENT_TOKEN, 
        "RUB",         
        [types.LabeledPrice("Гайд по похудению", 39900)], # 39900 копеек = 399 рублей
        start_parameter="get_diet_guide"
    )

@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout(query):
    bot.answer_pre_checkout_query(query.id, ok=True)

@bot.message_handler(content_types=['successful_payment'])
def success_pay(message):
    bot.send_message(message.chat.id, "✅ Оплата прошла успешно! Твой гайд готовится к отправке...")
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, 'rb') as f:
            bot.send_document(message.chat.id, f, caption="Твой гайд готов! Начинаем. 🚀")
    else:
        bot.send_message(message.chat.id, "Ошибка: файл не найден. Напишите админу.")

if __name__ == "__main__":
    bot.infinity_polling()
