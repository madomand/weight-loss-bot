import telebot
from telebot import types
import os
from amplitude import Amplitude, Event

# Загружаем ключи
TOKEN = os.getenv('BOT_TOKEN')
PAYMENT_TOKEN = os.getenv('PAYMENT_TOKEN')
AMP_KEY = os.getenv('AMPLITUDE_API_KEY')

bot = telebot.TeleBot(TOKEN)
amp_client = Amplitude(AMP_KEY) # Подключаем Amplitude
FILE_NAME = 'guide.pdf'

def track_event(user_id, event_name, properties=None):
    """Вспомогательная функция для отправки данных в Amplitude"""
    event = Event(
        event_type=event_name,
        user_id=str(user_id),
        event_properties=properties
    )
    amp_client.track(event)

@bot.message_handler(commands=['start'])
def start(message):
    # Отправляем событие в аналитику: "Бот запущен"
    track_event(message.from_user.id, "User Started Bot")
    
    welcome_text = (
        "Привет, красотка! 🌿\n\n"
        "Если ты здесь — скорее всего, тебе надоело... [ваш текст] ...\n\n"
        "👇 Жми — и погнали!"
    )
    
    bot.send_message(message.chat.id, welcome_text, parse_mode="Markdown")

    # Отправляем счет и событие "Показан счет на оплату"
    bot.send_invoice(
        message.chat.id, 
        "Гайд «Я выбираю себя»", 
        "Доступ к полной программе питания и тренировок.",
        "payload", 
        PAYMENT_TOKEN, 
        "RUB",         
        [types.LabeledPrice("Гайд", 39900)],
        start_parameter="diet_guide"
    )
    track_event(message.from_user.id, "Invoice Shown")

@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout(query):
    bot.answer_pre_checkout_query(query.id, ok=True)

@bot.message_handler(content_types=['successful_payment'])
def success_pay(message):
    # Отправляем событие "Покупка совершена" с суммой
    track_event(message.from_user.id, "Purchase Completed", {"amount": 399})
    
    bot.send_message(message.chat.id, "✅ Оплата прошла успешно! Лови свой гайд:")
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, 'rb') as f:
            bot.send_document(message.chat.id, f, caption="Твой гайд готов! 🚀")

if __name__ == "__main__":
    bot.infinity_polling()
