#!/usr/bin/python3
#telegram bot by nose to control the Consulting team presence
#require: pip3 install prettytable, pip3 install pytelegrambotapi

# to delete webhook
#https://api.telegram.org/bot<token>/deleteWebhook

import telebot, datetime, random
from prettytable import PrettyTable

token='XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
bot=telebot.TeleBot(token)
group={'nose':{'Start work':'','Lunch begin':'','Lunch end':'','Finish work':''},'zark':{'Start work':'','Lunch begin':'','Lunch end':'','Finish work':''},'pach':{'Start work':'','Lunch begin':'','Lunch end':'','Finish work':''},'kovl':{'Start work':'','Lunch begin':'','Lunch end':'','Finish work':''},'grek':{'Start work':'','Lunch begin':'','Lunch end':'','Finish work':''},'vely':{'Start work':'','Lunch begin':'','Lunch end':'','Finish work':''},'veul':{'Start work':'','Lunch begin':'','Lunch end':'','Finish work':''},'shai':{'Start work':'','Lunch begin':'','Lunch end':'','Finish work':''},'alul':{'Start work':'','Lunch begin':'','Lunch end':'','Finish work':''},'kosa':{'Start work':'','Lunch begin':'','Lunch end':'','Finish work':''},'mevl':{'Start work':'','Lunch begin':'','Lunch end':'','Finish work':''}}	#all consulting team

#commands menu
@bot.message_handler(commands=['help'])
def start_message(message):
	bot.send_message(message.chat.id, "'/status' - to see the Consulting team current state\n'/<nickname>' - to register the work start\n'/<nickname>d' - to register the lunch start\n'/<nickname>e' - to register the lunch end'\n'/<nickname>q' - to register the work finish\n'/help' - to see the list of available commands")


#Consulting team status
@bot.message_handler(commands=['status'])
def start_message(message):	
#	text='pach: '+str(group['pach'])+'\nkovl: '+str(group['kovl'])+'\nnose: '+str(group['nose'])+'\nzark: '+str(group['zark'])+'\nvely: '+str(group['vely'])+'\ngrek: '+str(group['grek'])+'\nkosa: '+str(group['kosa'])+'\nveul: '+str(group['veul'])+'\nshai: '+str(group['shai'])+'\nalul: '+str(group['alul'])
#	text=tbl()
#	bot.send_message(message.chat.id, text)
	text="<pre>{}</pre>".format(tbl())
	bot.send_message(message.chat.id, text, parse_mode="HTML")

#table with data
def tbl():
	th=['ID','Start','Lunch','Back','End']
	td1=["nose",group['nose']['Start work'],group['nose']['Lunch begin'],group['nose']['Lunch end'],group['nose']['Finish work']]
	td2=["zark",group['zark']['Start work'],group['zark']['Lunch begin'],group['zark']['Lunch end'],group['zark']['Finish work']]
	td3=["veul",group['veul']['Start work'],group['veul']['Lunch begin'],group['veul']['Lunch end'],group['veul']['Finish work']]
	td4=["vely",group['vely']['Start work'],group['vely']['Lunch begin'],group['vely']['Lunch end'],group['vely']['Finish work']]
	td5=["pach",group['pach']['Start work'],group['pach']['Lunch begin'],group['pach']['Lunch end'],group['pach']['Finish work']]
	td6=["grek",group['grek']['Start work'],group['grek']['Lunch begin'],group['grek']['Lunch end'],group['grek']['Finish work']]
	td7=["kovl",group['kovl']['Start work'],group['kovl']['Lunch begin'],group['kovl']['Lunch end'],group['kovl']['Finish work']]
	td8=["kosa",group['kosa']['Start work'],group['kosa']['Lunch begin'],group['kosa']['Lunch end'],group['kosa']['Finish work']]
	td9=["shai",group['shai']['Start work'],group['shai']['Lunch begin'],group['shai']['Lunch end'],group['shai']['Finish work']]
	td10=["alul",group['alul']['Start work'],group['alul']['Lunch begin'],group['alul']['Lunch end'],group['alul']['Finish work']]
	td11=["mevl",group['mevl']['Start work'],group['mevl']['Lunch begin'],group['mevl']['Lunch end'],group['mevl']['Finish work']]
	columns=len(th)  # Подсчитаем кол-во столбцов на будущее.
	table=PrettyTable(th)  # Определяем таблицу.
	# Cкопируем список td, на случай если он будет использоваться в коде дальше.
	td_data1=td1[:]
	# Входим в цикл который заполняет нашу таблицу.
	# Цикл будет выполняться до тех пор пока у нас не кончатся данные
	# для заполнения строк таблицы (список td_data).
	while td_data1:
		table.add_row(td_data1[:columns])
		td_data1=td_data1[columns:]
#repeat next table row
	td_data2=td2[:]
	while td_data2:
		table.add_row(td_data2[:columns])
		td_data2=td_data2[columns:]
#repeat next table row
	td_data3=td3[:]
	while td_data3:
		table.add_row(td_data3[:columns])
		td_data3=td_data3[columns:]
#repeat next table row
	td_data4=td4[:]
	while td_data4:
		table.add_row(td_data4[:columns])
		td_data4=td_data4[columns:]
#repeat next table row
	td_data5=td5[:]
	while td_data5:
		table.add_row(td_data5[:columns])
		td_data5=td_data5[columns:]
#repeat next table row
	td_data6=td6[:]
	while td_data6:
		table.add_row(td_data6[:columns])
		td_data6=td_data6[columns:]
#repeat next table row
	td_data7=td7[:]
	while td_data7:
		table.add_row(td_data7[:columns])
		td_data7=td_data7[columns:]
#repeat next table row
	td_data8=td8[:]
	while td_data8:
		table.add_row(td_data8[:columns])
		td_data8=td_data8[columns:]
#repeat next table row
	td_data9=td9[:]
	while td_data9:
		table.add_row(td_data9[:columns])
		td_data9=td_data9[columns:]
#repeat next table row
	td_data10=td10[:]
	while td_data10:
		table.add_row(td_data10[:columns])
		td_data10=td_data10[columns:]
#repeat next table row
	td_data11=td11[:]
	while td_data11:
		table.add_row(td_data11[:columns])
		td_data11=td_data11[columns:]
	return table
##########################################################
#nose
@bot.message_handler(commands=['nose'])		#start work
def start_message(message):
	bot.send_message(message.chat.id, str(rundphr(random.randint(1,11)))+"nose!")
	now=datetime.datetime.today()	#current time
	group['nose']['Start work']=now.strftime("%H:%M")

@bot.message_handler(commands=['nosed'])		#Lunch begin
def start_message(message):
	bot.send_message(message.chat.id, str(rundphr(random.randint(110,121)))+"nose!")
	now=datetime.datetime.today()	#current time
	group['nose']['Lunch begin']=now.strftime("%H:%M")

@bot.message_handler(commands=['nosee'])		#Lunch end
def start_message(message):
	bot.send_message(message.chat.id, str(rundphr(random.randint(220,231)))+"nose!")
	now=datetime.datetime.today()	#current time
	group['nose']['Lunch end']=now.strftime("%H:%M")

@bot.message_handler(commands=['noseq'])	#finish work
def start_message(message):
	bot.send_message(message.chat.id, str(rundphr(random.randint(330,342)))+"nose!")
	now=datetime.datetime.today()	#current time
	group['nose']['Finish work']=now.strftime("%H:%M")

##########################################################
#kovl
@bot.message_handler(commands=['kovl'])		#start work
def start_message(message):
	bot.send_message(message.chat.id, str(rundphr(random.randint(1,11)))+"Владислав!")
	now=datetime.datetime.today()	#current time
	group['kovl']['Start work']=now.strftime("%H:%M")

@bot.message_handler(commands=['kovld'])		#Lunch begin
def start_message(message):
	bot.send_message(message.chat.id, str(rundphr(random.randint(110,121)))+"Владислав!")
	now=datetime.datetime.today()	#current time
	group['kovl']['Lunch begin']=now.strftime("%H:%M")

@bot.message_handler(commands=['kovle'])		#Lunch end
def start_message(message):
	bot.send_message(message.chat.id, str(rundphr(random.randint(220,231)))+"Владислав!")
	now=datetime.datetime.today()	#current time
	group['kovl']['Lunch end']=now.strftime("%H:%M")

@bot.message_handler(commands=['kovlq'])	#finish work
def start_message(message):
	bot.send_message(message.chat.id, str(rundphr(random.randint(330,342)))+"Владислав!")
	now=datetime.datetime.today()	#current time
	group['kovl']['Finish work']=now.strftime("%H:%M")
##########################################################
#zark
@bot.message_handler(commands=['zark'])		#start work
def start_message(message):
	bot.send_message(message.chat.id, str(rundphr(random.randint(1,11)))+"Олег!")
	now=datetime.datetime.today()	#current time
	group['zark']['Start work']=now.strftime("%H:%M")

@bot.message_handler(commands=['zarkd'])		#Lunch begin
def start_message(message):
	bot.send_message(message.chat.id, str(rundphr(random.randint(110,121)))+"Олег!")
	now=datetime.datetime.today()	#current time
	group['zark']['Lunch begin']=now.strftime("%H:%M")

@bot.message_handler(commands=['zarke'])		#Lunch end
def start_message(message):
	bot.send_message(message.chat.id, str(rundphr(random.randint(220,231)))+"Олег!")
	now=datetime.datetime.today()	#current time
	group['zark']['Lunch end']=now.strftime("%H:%M")

@bot.message_handler(commands=['zarkq'])	#finish work
def start_message(message):
	bot.send_message(message.chat.id, str(rundphr(random.randint(330,342)))+"Олег!")
	now=datetime.datetime.today()	#current time
	group['zark']['Finish work']=now.strftime("%H:%M")
##########################################################
#pach
@bot.message_handler(commands=['pach'])		#start work
def start_message(message):
	bot.send_message(message.chat.id, str(rundphr(random.randint(1,11)))+"Павел!")
	now=datetime.datetime.today()	#current time
	group['pach']['Start work']=now.strftime("%H:%M")

@bot.message_handler(commands=['pachd'])		#Lunch begin
def start_message(message):
	bot.send_message(message.chat.id, str(rundphr(random.randint(110,121)))+"Павел!")
	now=datetime.datetime.today()	#current time
	group['pach']['Lunch begin']=now.strftime("%H:%M")

@bot.message_handler(commands=['pache'])		#Lunch end
def start_message(message):
	bot.send_message(message.chat.id, str(rundphr(random.randint(220,231)))+"Павел!")
	now=datetime.datetime.today()	#current time
	group['pach']['Lunch end']=now.strftime("%H:%M")

@bot.message_handler(commands=['pachq'])	#finish work
def start_message(message):
	bot.send_message(message.chat.id, str(rundphr(random.randint(330,342)))+"Павел!")
	now=datetime.datetime.today()	#current time
	group['pach']['Finish work']=now.strftime("%H:%M")
##########################################################
#vely
@bot.message_handler(commands=['vely'])		#start work
def start_message(message):
	bot.send_message(message.chat.id, str(rundphr(random.randint(1,11)))+"Вероника!")
	now=datetime.datetime.today()	#current time
	group['vely']['Start work']=now.strftime("%H:%M")

@bot.message_handler(commands=['velyd'])		#Lunch begin
def start_message(message):
	bot.send_message(message.chat.id, str(rundphr(random.randint(110,121)))+"Вероника!")
	now=datetime.datetime.today()	#current time
	group['vely']['Lunch begin']=now.strftime("%H:%M")

@bot.message_handler(commands=['velye'])		#Lunch end
def start_message(message):
	bot.send_message(message.chat.id, str(rundphr(random.randint(220,231)))+"Вероника!")
	now=datetime.datetime.today()	#current time
	group['vely']['Lunch end']=now.strftime("%H:%M")

@bot.message_handler(commands=['velyq'])	#finish work
def start_message(message):
	bot.send_message(message.chat.id, str(rundphr(random.randint(330,342)))+"Вероника!")
	now=datetime.datetime.today()	#current time
	group['vely']['Finish work']=now.strftime("%H:%M")
##########################################################
#grek
@bot.message_handler(commands=['grek'])		#start work
def start_message(message):
	bot.send_message(message.chat.id, str(rundphr(random.randint(1,11)))+"Екатерина!")
	now=datetime.datetime.today()	#current time
	group['grek']['Start work']=now.strftime("%H:%M")

@bot.message_handler(commands=['grekd'])		#Lunch begin
def start_message(message):
	bot.send_message(message.chat.id, str(rundphr(random.randint(110,121)))+"Екатерина!")
	now=datetime.datetime.today()	#current time
	group['grek']['Lunch begin']=now.strftime("%H:%M")

@bot.message_handler(commands=['greke'])		#Lunch end
def start_message(message):
	bot.send_message(message.chat.id, str(rundphr(random.randint(220,231)))+"Екатерина!")
	now=datetime.datetime.today()	#current time
	group['grek']['Lunch end']=now.strftime("%H:%M")

@bot.message_handler(commands=['grekq'])	#finish work
def start_message(message):
	bot.send_message(message.chat.id, str(rundphr(random.randint(330,342)))+"Екатерина!")
	now=datetime.datetime.today()	#current time
	group['grek']['Finish work']=now.strftime("%H:%M")
##########################################################
#veul
@bot.message_handler(commands=['veul'])		#start work
def start_message(message):
	bot.send_message(message.chat.id, str(rundphr(random.randint(1,11)))+"Юлия!")
	now=datetime.datetime.today()	#current time
	group['veul']['Start work']=now.strftime("%H:%M")

@bot.message_handler(commands=['veuld'])		#Lunch begin
def start_message(message):
	bot.send_message(message.chat.id, str(rundphr(random.randint(110,121)))+"Юлия!")
	now=datetime.datetime.today()	#current time
	group['veul']['Lunch begin']=now.strftime("%H:%M")

@bot.message_handler(commands=['veule'])		#Lunch end
def start_message(message):
	bot.send_message(message.chat.id, str(rundphr(random.randint(220,231)))+"Юлия!")
	now=datetime.datetime.today()	#current time
	group['veul']['Lunch end']=now.strftime("%H:%M")

@bot.message_handler(commands=['veulq'])	#finish work
def start_message(message):
	bot.send_message(message.chat.id, str(rundphr(random.randint(330,342)))+"Юлия!")
	now=datetime.datetime.today()	#current time
	group['veul']['Finish work']=now.strftime("%H:%M")

##########################################################
#shai
@bot.message_handler(commands=['shai'])		#start work
def start_message(message):
	bot.send_message(message.chat.id, str(rundphr(random.randint(1,11)))+"Шайма!")
	now=datetime.datetime.today()	#current time
	group['shai']['Start work']=now.strftime("%H:%M")

@bot.message_handler(commands=['shaid'])		#Lunch begin
def start_message(message):
	bot.send_message(message.chat.id, str(rundphr(random.randint(110,121)))+"Шайма!")
	now=datetime.datetime.today()	#current time
	group['shai']['Lunch begin']=now.strftime("%H:%M")

@bot.message_handler(commands=['shaie'])		#Lunch end
def start_message(message):
	bot.send_message(message.chat.id, str(rundphr(random.randint(220,231)))+"Шайма!")
	now=datetime.datetime.today()	#current time
	group['shai']['Lunch end']=now.strftime("%H:%M")

@bot.message_handler(commands=['shaiq'])	#finish work
def start_message(message):
	bot.send_message(message.chat.id, str(rundphr(random.randint(330,342)))+"Шайма!")
	now=datetime.datetime.today()	#current time
	group['shai']['Finish work']=now.strftime("%H:%M")
##########################################################
#alul
@bot.message_handler(commands=['alul'])		#start work
def start_message(message):
	bot.send_message(message.chat.id, str(rundphr(random.randint(1,11)))+"Юлия!")
	now=datetime.datetime.today()	#current time
	group['alul']['Start work']=now.strftime("%H:%M")

@bot.message_handler(commands=['aluld'])		#Lunch begin
def start_message(message):
	bot.send_message(message.chat.id, str(rundphr(random.randint(110,121)))+"Юлия!")
	now=datetime.datetime.today()	#current time
	group['alul']['Lunch begin']=now.strftime("%H:%M")

@bot.message_handler(commands=['alule'])		#Lunch end
def start_message(message):
	bot.send_message(message.chat.id, str(rundphr(random.randint(220,231)))+"Юлия!")
	now=datetime.datetime.today()	#current time
	group['alul']['Lunch end']=now.strftime("%H:%M")

@bot.message_handler(commands=['alulq'])	#finish work
def start_message(message):
	bot.send_message(message.chat.id, str(rundphr(random.randint(330,342)))+"Юлия!")
	now=datetime.datetime.today()	#current time
	group['alul']['Finish work']=now.strftime("%H:%M")
##########################################################
#kosa
@bot.message_handler(commands=['kosa'])		#start work
def start_message(message):
	bot.send_message(message.chat.id, str(rundphr(random.randint(1,11)))+"Александра!")
	now=datetime.datetime.today()	#current time
	group['kosa']['Start work']=now.strftime("%H:%M")

@bot.message_handler(commands=['kosad'])		#Lunch begin
def start_message(message):
	bot.send_message(message.chat.id, str(rundphr(random.randint(110,121)))+"Александра!")
	now=datetime.datetime.today()	#current time
	group['kosa']['Lunch begin']=now.strftime("%H:%M")

@bot.message_handler(commands=['kosae'])		#Lunch end
def start_message(message):
	bot.send_message(message.chat.id, str(rundphr(random.randint(220,231)))+"Александра!")
	now=datetime.datetime.today()	#current time
	group['kosa']['Lunch end']=now.strftime("%H:%M")

@bot.message_handler(commands=['kosaq'])	#finish work
def start_message(message):
	bot.send_message(message.chat.id, str(rundphr(random.randint(330,342)))+"Александра!")
	now=datetime.datetime.today()	#current time
	group['kosa']['Finish work']=now.strftime("%H:%M")
##########################################################
#mevl
@bot.message_handler(commands=['mevl'])         #start work
def start_message(message):
        bot.send_message(message.chat.id, str(rundphr(random.randint(1,11)))+"Владимир!")
        now=datetime.datetime.today()   #current time
        group['mevl']['Start work']=now.strftime("%H:%M")

@bot.message_handler(commands=['mevld'])                #Lunch begin
def start_message(message):
        bot.send_message(message.chat.id, str(rundphr(random.randint(110,121)))+"Владимир!")
        now=datetime.datetime.today()   #current time
        group['mevl']['Lunch begin']=now.strftime("%H:%M")

@bot.message_handler(commands=['mevle'])                #Lunch end
def start_message(message):
        bot.send_message(message.chat.id, str(rundphr(random.randint(220,231)))+"Владимир!")
        now=datetime.datetime.today()   #current time
        group['mevl']['Lunch end']=now.strftime("%H:%M")

@bot.message_handler(commands=['mevlq'])        #finish work
def start_message(message):
        bot.send_message(message.chat.id, str(rundphr(random.randint(330,342)))+"Владимир!")
        now=datetime.datetime.today()   #current time
        group['mevl']['Finish work']=now.strftime("%H:%M")
#########################################################
#########################################################
def rundphr(a):		#random phrases
	if a==1:		#greeting
		phr="Hello "
	elif a==2:
		phr="Guten Tag "
	elif a==3:
		phr="Hola "
	elif a==4:
		phr="Ahlan wa sahlan "
	elif a==5:
		phr="Прывітанне "
	elif a==6:
		phr="Aloha "
	elif a==7:
		phr="Гамарджоба "
	elif a==8:
		phr="Ave "
	elif a==9:
		phr="Салам алейкум "
	elif a==9:
		phr="Konnichi wa "
	elif a==10:
		phr="I love the smell of napalm in the morning "
	elif a==11:
		phr="It's time to START,  "
#			lunch
	elif a==110:
		phr="Have a good lunch "
	elif a==111:
		phr="Bon appétit "
	elif a==112:
		phr="Смачна есьці "
	elif a==113:
		phr="Be-teavon "
	elif a==114:
		phr="Buen apetito "
	elif a==115:
		phr="Ас болсын "
	elif a==116:
		phr="Приятного аппетита "
	elif a==117:
		phr="Itadakimasu "
	elif a==118:
		phr="Guten Appetit "
	elif a==119:
		phr="Wèikǒu hǎo "
	elif a==120:
		phr="war is war, but lunch has to be on time, "
	elif a==121:
		phr="You'll be back... "
#			end lunch
	elif a==220:
		phr="Welcome back "
	elif a==221:
		phr="Back to the work "
	elif a==222:
		phr="New tickets are waiting for you "
	elif a==223:
		phr="We missed you, "
	elif a==224:
		phr="Ну наконец то ты вернулся "
	elif a==225:
		phr="З вяртаннем "
	elif a==226:
		phr="Start doing something useful already, "
	elif a==227:
		phr="57 65 6c 63 6f 6d 65 20 62 61 63 6b 21 "
	elif a==228:
		phr="New missions are available on the quest board,  "
	elif a==229:
		phr="We'll pretend you haven't gone anywhere "
	elif a==230:
		phr="You can not live on bread alone, "
	elif a==231:
		phr="Pablo was waiting for you, "
#					farewell
	elif a==330:
		phr="Goodbye "
	elif a==331:
		phr="Au revoir "
	elif a==332:
		phr="Adiós "
	elif a==333:
		phr="Auf Wiedersehen "
	elif a==334:
		phr="Arrivederci "
	elif a==335:
		phr="До побачення "
	elif a==336:
		phr="Sayonara "
	elif a==337:
		phr="Hoşçakalın "
	elif a==338:
		phr="Саг олун "
	elif a==339:
		phr="Нахвамдис "
	elif a==340:
		phr="Do not live by WIALON alone, "
	elif a==341:
		phr="It's time to STOP, "
	elif a==342:
		phr="Бывай "
#		bot.send_photo(message.chat.id, 'gif/ku.gif')
	return phr

bot.polling()	#waiting the  command all the time
