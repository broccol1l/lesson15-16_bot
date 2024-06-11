import telebot
import buttons as bt

bot = telebot.TeleBot(token="7322888967:AAFhyjpGoGS6ZlLcZCNhpfSs4jvCmpurOmg")

@bot.message_handler(commands=["start"])
def start(message):
    user_id = message.from_user.id
    bot.send_message(user_id, "Здравствуйте! Это бот доставки.\n"
                              "Пожалуйста, напишите свое имя")
    # указываю следующий после старта (функция,
    # которая должна сработать после функции старт)
    bot.register_next_step_handler(message, get_name)

def get_name(message):
    user_id = message.from_user.id
    name = message.text
    bot.send_message(user_id, "Отправьте свой номер", reply_markup=bt.phone_number_bt())
    bot.register_next_step_handler(message, get_number, name)

def get_number(message, name):
    user_id = message.from_user.id
    if message.contact:
        number = message.contact.phone_number
        print(name, number)
        bot.send_message(user_id, "Отправьте свою локацию",
                         reply_markup=bt.location_bt())
        bot.register_next_step_handler(message, get_location, name, number)
    else:
        bot.send_message(user_id, 'Отправьте свой номер через кнопку',
                         reply_markup=bt.phone_number_bt())
        bot.register_next_step_handler(message, get_number, name)

def get_location(message, name, number):
    user_id = message.from_user.id
    if message.location:
        location = message.location
        bot.send_message(user_id, f"Вы успешно прошли регистрацию.\n"
                                  f"Ваши данные:\n"
                                  f"Имя: {name}\n"
                                  f"Номер: {number}\n"
                                  f"Локация: {location}")
    else:
        bot.send_message(user_id, "Отправьте свою локацию через кнопку",
                         reply_markup=bt.location_bt())
        bot.register_next_step_handler(message, get_location, name, number)

bot.infinity_polling()