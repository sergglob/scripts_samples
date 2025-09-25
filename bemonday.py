#bemonday_bot
'''
Done! Congratulations on your new bot. You will find it at t.me/bemonday_bot.
Use this token to access the HTTP API:
6753732347:AAFA0wsDWOA228eC2nCY5zVydHpe9eyj3YA
'''
#novikov_vm01 ext IP 185.32.226.191

import telebot
import ast
import time
from telebot import types
from datetime import date

bot = telebot.TeleBot("6753732347:AAFA0wsDWOA228eC2nCY5zVydHpe9eyj3YA")
today = date.today()

stringList = {
        "1": "Бобрик Наталья \U0001F9AB",       #beaver
        "2": "Бутько Павел \U0001F4E3",         #megaphone
        "3": "Вакуленчик Андрей \U0001F4F8",    #camera
        "4": "Ворошкевич Игорь \U0001F57A",     #man dance
        "5": "Герасимчик Дмитрий \u2620",       #skull vs bones
        "6": "Зизеко Юрий \U0001F61E",          #disappointed face
        "7": "Карасёв Дмитрий \U0001F41F",      #fish
        "8": "Клепча Дмитрий \U0001F4BB",       #computer
        "9": "Короткевич Константин \U0001F640",#screaming cat
        "10": "Кособука Александр \u24E5",       #v logo
        "11": "Лазуко Дмитрий \U0001F34F",      #green apple
        "12": "Медведь Дмитрий \U0001F9F8",     #teddy bear
        "13": "Нелюб Иван \U0001F91F",          #Ilove hand sign
        "14": "Новиков Сергей \U0001F525",      #fire
        "15": "Сидоров Андрей \U0001F454",      #nekite
        "16": "Фукс Виталий \U0001F98A",        #fox
        "17": "ГЭСИО \u2694"                    #cross swords
}

#\U0001F480 skull
#\U0001F621 angry face
#\U0001F47F imp face
#\U0001F5D1 waste backet 
#\U0001F6AE man throwing into trash
def makeKeyboard():
    markup = types.InlineKeyboardMarkup()

    for key, value in stringList.items():
        markup.add(types.InlineKeyboardButton(text=value,callback_data="['value', '" + key + "']"))

    return markup

@bot.message_handler(commands=['test'])                 #launching command
def handle_command_adminwindow(message):
    bot.send_message(chat_id=message.chat.id,
                     text="%s | Жми на себя, если впорядке \U0001F634" % (today),            #sleeping face
                     reply_markup=makeKeyboard(),
                     parse_mode='HTML')

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if (call.data.startswith("['value'")):
        keyFromCallBack = ast.literal_eval(call.data)[1]
        del stringList[keyFromCallBack]
        bot.edit_message_text(chat_id=call.message.chat.id,
                              text="%s | Жми на себя, если впорядке \U0001F928" % (today),   #conserned face with one eye raised
                              message_id=call.message.message_id,
                              reply_markup=makeKeyboard(),
                              parse_mode='HTML')
####
    if len(stringList)==0:
                bot.edit_message_text(chat_id=call.message.chat.id,
                              text="%s | Все впорядке!!! \U0001F60A" % (today), #happy face
                              message_id=call.message.message_id,
                              reply_markup=makeKeyboard(),
                              parse_mode='HTML')
while True:
    try:
        bot.polling(none_stop=True, interval=0, timeout=0)
    except:
        time.sleep(10)

