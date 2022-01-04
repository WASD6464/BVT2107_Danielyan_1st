from datetime import datetime, date, time
import telebot 
from telebot import types
import psycopg2

token = ""
bot = telebot.TeleBot(token)


conn = psycopg2.connect(database="Bot",
                        user="postgres",
                        password="qwe123",
                        host="localhost",
                        port="5432")
cursor = conn.cursor()


start = date(2021, 9, 1)
d = datetime.now() 
week = d.isocalendar()[1] - start.isocalendar()[1] + 1


if week%2 == 1:
    top_week = True
    text_week = "верхней"
else:
    top_week = False
    text_week = "нижней"


@bot.message_handler(commands = ['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row("/mtuci", "/week", "/help")
    keyboard.row("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday")
    keyboard.row("Schedule for this week", "Schedule for next week")
    bot.send_message(message.chat.id, '/help', reply_markup=keyboard)


@bot.message_handler(commands = ['help'])
def help(message):
    bot.send_message(message.chat.id, 'Расписание для группы БВТ2107\n\
Для того чтобы узнать расписание на определенный день недели нужно нажать на соответсвующую кнопку \
или введя день недели на русском или английском языке \
расписание будет показано для данной недели (верхняя/нижняя)\n\
Чтобы узнать какая сейчас неделя воспользуйтесь командой /week\n\
Также можно посмотреть расписание полностью на эту и следующую неделю нажав соответсвующие кнопки\n\
Подробнее о ВУЗе можно узнать с помощью команды /mtuci')


@bot.message_handler(commands = ['week'])
def week(message):
    if top_week:
        bot.send_message(message.chat.id, 'верхняя')
    else:
        bot.send_message(message.chat.id, 'нижняя')
        

@bot.message_handler(commands = ['mtuci'])
def about_mtuci(message):
    bot.send_message(message.chat.id, 'Тогда тебе сюда – https://mtuci.ru/')


@bot.message_handler()
def answer(message):
    weeks = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота']
    if message.text.lower() in weeks:
        if message.text.lower() == "monday" or message.text.lower() == "понедельник":
            dof = 1
            text_ru = "понедельник"
        elif message.text.lower() ==  "tuesday" or message.text.lower() ==  "вторник":
            dof = 2
            text_ru = "вторник"
        elif message.text.lower() ==  "wednesday" or message.text.lower() == "среда":
            dof = 3
            text_ru = "среду"
        elif message.text.lower() ==  "thursday" or message.text.lower() == "четверг":
            dof = 4
            text_ru = "четверг"
        elif message.text.lower() ==  "friday" or message.text.lower() == "пятница":
            dof = 5
            text_ru = "пятницу"
        else:
            dof = 6
            text_ru = "субботу"
        
            
        cursor.execute(f'SELECT subject.subject_name, timetable.room, timetable.start_time, teachers.full_name\
                        FROM subject\
                        INNER JOIN timetable ON subject.id = timetable.fk_subject\
                        INNER JOIN teachers ON subject.id = teachers.fk_subject\
                        WHERE dof = {dof} and top_week = {top_week}\
                        ORDER BY timetable.start_time')
        records = list(cursor.fetchall())
        bot.send_message(message.chat.id, f"Расписание на {text_ru} (по {text_week} неделе):")
        if records == []:
            for i in range(5):
                bot.send_message(message.chat.id, 'CPC')
        for i in range(len(records)):
            bot.send_message(message.chat.id, f"{records[i][0]} | {records[i][1]} \n{records[i][2]} | {records[i][3]}")

    elif message.text.lower() == "schedule for this week":
        cursor.execute(f'SELECT subject.subject_name, timetable.room, timetable.start_time, teachers.full_name, timetable.dof\
                        FROM subject\
                        INNER JOIN timetable ON subject.id = timetable.fk_subject\
                        INNER JOIN teachers ON subject.id = teachers.fk_subject\
                        WHERE top_week = {top_week}\
                        ORDER BY timetable.dof, timetable.start_time')
        records = list(cursor.fetchall())
        bot.send_message(message.chat.id, f"Расписание на эту неделю:")
        week = ['','Понедельник','Вторник','Среда','Четверг','Пятница','Суббота']
        for i in range(len(records)):
            bot.send_message(message.chat.id, f"{week[records[i][4]]} \n{records[i][0]} | {records[i][1]} \n{records[i][2]} | {records[i][3]}")

    elif message.text.lower() == "schedule for next week":
        cursor.execute(f'SELECT subject.subject_name, timetable.room, timetable.start_time, teachers.full_name, timetable.dof\
                        FROM subject\
                        INNER JOIN timetable ON subject.id = timetable.fk_subject\
                        INNER JOIN teachers ON subject.id = teachers.fk_subject\
                        WHERE top_week = {not(top_week)}\
                        ORDER BY timetable.dof, timetable.start_time')
        records = list(cursor.fetchall())
        bot.send_message(message.chat.id, f"Расписание на следующую неделю:")
        week = ['','Понедельник','Вторник','Среда','Четверг','Пятница','Суббота']
        for i in range(len(records)):
            bot.send_message(message.chat.id, f"{week[records[i][4]]} \n{records[i][0]} | {records[i][1]} \n{records[i][2]} | {records[i][3]}")
    elif message.text.lower() == "я тебя люблю":
        bot.send_message(message.chat.id, 'Я люблю Аллу Зепсен!❤️❤️❤️❤️❤️')
        bot.send_photo(message.chat.id, photo=open('C:\\Users\\WASD\\Desktop\\index.jpg', 'rb'))
        
    else:
        bot.send_message(message.chat.id, 'Извините, я Вас не понял')

bot.polling()