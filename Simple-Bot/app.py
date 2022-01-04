import telebot
from telebot import types
token = ''
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row("Хочу","/help","/Creator", "/Cat", "/Music")
    bot.send_message(message.chat.id, 'Привет! Хочешь узнать свежую информацию о МТУСИ?', reply_markup=keyboard)


@bot.message_handler(commands=['help'])
def send(message):
        bot.send_message(message.chat.id, 'Я умею отправлять модную музыку (/Music), кидать котиков (/Cat), могу сказать кто мой создатель(/Creator) и вы можете узнать свежую информацию о МТУСИ \n Умею отвечать на текстовые команды "я тебя люблю", "как у тебя дела?", "чему равно число пи?"')


@bot.message_handler(commands=['Creator'])
def send(message):
        bot.send_message(message.chat.id, 'Мой единственный и неповторимый создатель - @wasd_64')


@bot.message_handler(commands=['Cat'])
def send(message):
        bot.send_photo(message.chat.id, photo=open('/home/wasd64/Downloads/Cat.jpg', 'rb'))


@bot.message_handler(commands=['Music'])
def send(message):
        bot.send_message(message.chat.id, 'Чтоб шарить в музыке ты должен знать этот трек')
        bot.send_audio(message.chat.id, audio=open('/home/wasd64/Downloads/MORGENSHTERN-Cadillac.mp3', 'rb'))


@bot.message_handler(content_types=['text'])
def send(message):
    if message.text.lower() == "я тебя люблю":
        bot.send_message(message.chat.id, 'Я люблю Аллу Зепсен!')
    elif message.text.lower() == "как у тебя дела?":
        bot.send_message(message.chat.id, 'В моём королевстве цифр царит идилия хаоса и порядка, я в нём хозяин')
    elif message.text.lower() == "чему равно число пи?":
        bot.send_message(message.chat.id, '3,141592653589793238462643383279502884197169399375105820974944592307816406286208998628034825342117067982148086513282306647093844609550582231725359408128481117450284102701938521105559644622948954930381964428810975665933446284756482337867831652712019091')
    elif message.text.lower() == "хочу":
        bot.send_message(message.chat.id, 'Тогда тебе сюда – https://mtuci.ru/')




bot.polling(none_stop=True)