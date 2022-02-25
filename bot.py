import telebot
from telebot import types
import sqlite3

TOKEN = '5233219459:AAHdU6Db-F4ZnTfay_2MZIMKWCP-rsjPuqA' #token bota in telegram
bot = telebot.TeleBot(TOKEN)

#подключаю базу данных SQLite3 к своему проекту
ID_CHAT = -1001756928504

#текст после написания start
@bot.message_handler(commands = "start")
def text(message):

    #элементы главного меню
    markup = types.ReplyKeyboardMarkup(resize_keyboard= True)
    item1 = types.KeyboardButton('🔥 F.A.Q.')
    item2 = types.KeyboardButton('🔧 Задать вопрос')
    item3 = types.KeyboardButton('❗ Сообщить об ошибке')
    markup.add(item1, item2, item3)

    #вывод самого сообщения
    bot.send_message(message.chat.id, 'Здраствуйте, вас приветствует команда RedVision. Благодаря этому боту вы сможете, получить ответ на интересующие вас вопросы или сообщить об ошибке в игре.', reply_markup = markup)

@bot.message_handler(content_types=['text'])
def text_q(message):
   if message.text == "🔧 Задать вопрос":
    #элементы главного меню
    markup = types.ReplyKeyboardMarkup(resize_keyboard= True)
    item1 = types.KeyboardButton('◀️ Назад')
    markup.add(item1)

    #вывод самого сообщения
    sent = bot.send_message(message.chat.id, 'Напишите текст вопроса!', reply_markup = markup)
    bot.register_next_step_handler(sent,blup)

   elif message.text == "❗ Cообщить об ошибке":
    #элементы главного меню
    markup = types.ReplyKeyboardMarkup(resize_keyboard= True)
    item1 = types.KeyboardButton('◀️ Назад')
    markup.add(item1)
    #вывод самого сообщения
    sent = bot.send_message(message.chat.id, 'Опишите ошибку с которой вы столкнулись.', reply_markup = markup)
    bot.register_next_step_handler(sent,bug)

   elif message.text == "🔥 F.A.Q.":
    #элементы главного меню
    markup = types.ReplyKeyboardMarkup(resize_keyboard= True)
    item1 = types.KeyboardButton('◀️ Назад')
    markup.add(item1)

    connect = sqlite3.connect('telegramBD.db', check_same_thread=False)
    cursor = connect.cursor()

    #вывод из базы данных всех вопрос и ответов
    cursor.execute("SELECT question.Text FROM question WHERE ID < 7")
    Q = cursor.fetchall()
    cursor.execute("SELECT answers.Text FROM answers WHERE ID < 7")
    A = cursor.fetchall()
    connect.close()
    message_str = ""
    i = 0
    while i < min(len(A), len(Q)):
     message_str += f"Q: {Q[i]}\nA: {A[i]}\n\n"
     i += 1
    bot.send_message(message.chat.id, "Вот вопросы которые часто задают пользователи: \n\n" + message_str, reply_markup = markup)

   elif message.text == "◀️ Назад":
    #элементы главного меню
    markup = types.ReplyKeyboardMarkup(resize_keyboard= True)
    item1 = types.KeyboardButton('🔥 F.A.Q.')
    item2 = types.KeyboardButton('🔧 Задать вопрос')
    item3 = types.KeyboardButton('❗ Cообщить об ошибке')
    markup.add(item1, item2, item3)

    #вывод самого сообщения
    bot.send_message(message.chat.id, 'Что хотите сделать сейчас?', reply_markup = markup)

#Запись вопроса "🔧 Задать вопрос" в БД
def blup(message):
 name=message.text
 username = message.from_user.username
 user_id = message.from_user.id

 bot.send_message(ID_CHAT, 'Новое уведомление! \n Пользователь задал вам вопрос. Проверьте БД и ответьте на него!\n\n' + name)
 connect = sqlite3.connect('telegramBD.db', check_same_thread=False)
 cursor = connect.cursor()
 cursor = connect.cursor()
 cursor.execute("INSERT OR IGNORE INTO users (User_heshtag) VALUES (?)", (user_id,))
 cursor.execute("INSERT INTO question (Text,User_heshtag,username) VALUES (?,?,?)", (name,user_id,username,))
 connect.commit()

 bot.send_message(message.chat.id, 'Я отправил ваш запрос админам, ожидайте')
 connect.close()

def bug(message):
 name=message.text
 username = message.from_user.username

 bot.send_message(ID_CHAT, 'Новое уведомление! \n Пользователь обнаружил новую ошибку в игре! Нужно обозначить тип ошибки в БД! Вот текст сообщения:\n\n' + name)
 connect = sqlite3.connect('telegramBD.db', check_same_thread=False)
 cursor = connect.cursor()
 cursor = connect.cursor()
 cursor.execute("INSERT INTO Bugs (User_Text,username) VALUES (?,?)", (name,username,))
 connect.commit()

 bot.send_message(message.chat.id, 'Сообщение об ошибке было отправленно разработчикам! Спасибо за вашу наблюдательность!')
 connect.close()

bot.polling(none_stop=True)
