#bemonday_bot
'''
Done! Congratulations on your new bot. You will find it at t.me/bemonday_bot.
Use this token to access the HTTP API:
xxxx:yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy
'''
import telebot
import ast
import time
from telebot import types
from datetime import date

bot = telebot.TeleBot("xxxx:yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy")
today = date.today()

stringList = {
        "1": "Наталья \U0001F9AB",       #beaver
        "2": "Павел \U0001F4E3",         #megaphone
        "3": "Андрей \U0001F4F8",    #camera
        "4": "Игорь \U0001F57A",     #man dance
        "5": "Дмитрий \u2620",       #skull vs bones
        "6": "Юрий \U0001F61E",          #disappointed face
        "7": "Дмитрий \U0001F41F",      #fish
        "8": "Дмитрий \U0001F4BB",       #computer
        "9": "Константин \U0001F640",#screaming cat
        "10": "Александр \u24E5",       #v logo
        "11": "Дмитрий \U0001F34F",      #green apple
        "12": "Дмитрий \U0001F9F8",     #teddy bear
        "13": "Иван \U0001F91F",          #Ilove hand sign
        "14": "Сергей \U0001F525",      #fire
        "15": "Андрей \U0001F454",      #nekite
        "16": "Виталий \U0001F98A",        #fox
        "17": "О \u2694"                    #cross swords
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

