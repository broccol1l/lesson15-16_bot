import telebot
import buttons as bt
import database as db

bot = telebot.TeleBot(token="7322888967:AAFhyjpGoGS6ZlLcZCNhpfSs4jvCmpurOmg")

# db.add_product(pr_name="Бургер", pr_desc="лучший", pr_price=50000, pr_quantity=10, pr_photo="https://ic.pics.livejournal.com/lenkasokolova/72298496/90320/90320_original.jpg")
# db.add_product(pr_name="Чизбургер", pr_desc="лучший", pr_price=50000, pr_quantity=10, pr_photo="https://s9.travelask.ru/system/images/files/000/130/524/wysiwyg_jpg/24.jpg?1486447532")
print(db.get_all_product())
@bot.message_handler(commands=["start"])
def start(message):
    user_id = message.from_user.id
    checker = db.check_user(user_id)
    if checker == True:
        bot.send_message(user_id, "Выберите действие", reply_markup=bt.main_menu_kb())
    elif checker == False:
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
                                  f"Локация: {location}", reply_markup=bt.main_menu_kb())
        db.add_user(user_id, name, number)
    else:
        bot.send_message(user_id, "Отправьте свою локацию через кнопку",
                         reply_markup=bt.location_bt())
        bot.register_next_step_handler(message, get_location, name, number)

@bot.callback_query_handler(lambda call: call.data in ["main_menu"])
def all_calls(call):
    user_id = call.message.chat.id
    if call.data == "main_menu":
        bot.delete_message(user_id, call.message.message_id)
        bot.send_message(user_id, "Выберите действие", reply_markup=bt.main_menu_kb())

@bot.callback_query_handler(lambda call: "prod_" in call.data)
def product_call(call):
    user_id = call.message.chat.id
    bot.delete_message(user_id, call.message.message_id)
    product_id = int(call.data.replace("prod_", ""))
    product_info = db.get_exact_product(product_id)
    bot.send_photo(user_id, photo=product_info[3], caption=f"{product_info[0]}\n\n"
                                                           f"Описание: {product_info[2]}\n"
                                                           f"Цена: {product_info[1]} сум")
@bot.message_handler(content_types=["text"])
def main_menu(message):
    user_id = message.from_user.id
    text = message.text
    if text == "Меню":
        all_products = db.get_pr_id_name()
        bot.send_message(user_id, "Выберите продукт", reply_markup=bt.products_in(all_products))
    elif text == "Корзина":
        bot.send_message(user_id, "Ваша корзина")
    elif text == "Оставить отзыв":
        bot.send_message(user_id, "Напишите текст вашего отзыва")




bot.infinity_polling()