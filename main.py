import telebot
from logic import detect_trash

bot = telebot.TeleBot("8591309669:AAHtMhd1RHD2Cz29q0QgesEscnMC23dzae4")

@bot.message_handler(commands=['Старт', 'старт', 'start', 'Start'])
def start(message):
    bot.reply_to(message, f"Привет! Я бот {bot.get_me().first_name} моя задача помогать распределить мусор")

@bot.message_handler(content_types=['photo'])
def photo(message):
    file_info = bot.get_file(message.photo[-1].file_id)
    file_name = file_info.file_path.split('/')[-1]
    downloaded_file = bot.download_file(file_info.file_path)
    with open(file_name, "wb") as new_file:
        new_file.write(downloaded_file)
    name, count, content = detect_trash(img = file_name, model = "keras_model.h5", label = "labels.txt")
    bot.reply_to(message, f"Я распозал {name}, я уверен на {int(count*100)}% \n {content}")

@bot.message_handler(func=lambda message: True)
def echo(message):
    bot.reply_to(message, message.text)

bot.polling()
