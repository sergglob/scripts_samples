#!/usr/bin/python3
#Developed by Novikov Sergey (nose)
#WLN generator from KML linear geofence by the wialon routing tool
import json, time, random, math
from var import *	# import global variables from 'var.py' config file
#global var: "min" - grid per meter
utc_now=utct	#beginning time in UTC 
f=open(flname)
a=f.readlines()
###

#REG;1603666800;37.6215976299;55.7734807486;2;343;ALT:0.0;SATS:10;;;;
#UTC;LAT;LON;SPEED;CORCE;ALTITUDE;SATS;;;;
##### multiple the first coordinate to get beginning parking ##################
def park (t,a,b,fu):										#parkings - time, lat, lon
	for i in range(pc):
		sats=random.randint(sats_min,sats_max)		#sattelites randomizer
		a1=0 										#adc on parkinng = 0 V		
		a2=0 										#adc on parkinng = 0 V
		dig1=0 										#digital sensor 1 OFF
		fuel=random.uniform(fu-fchr,fu+fchr)
		print("REG;"+str(t)+";"+str(a)+";"+str(b)+";0;0;ALT:0.0,adc1:"+str(a1)+",adc2:"+str(a2)+",fuel:"+str(fuel)+";SATS:"+str(sats)+",in1:"+str(dig1)+";;")	
		t+=pt		#permanent parking time
	return t
#

#parking with the sensors ON
def park_on (t,a,b,i,fu):										#parkings - time, lat, lon, number of idling messages (sop)
	while i!=0:
		sats=random.randint(sats_min,sats_max)				#sattelites randomizer
		a1=round(random.uniform(adc1, adc1+adcd), 2)				#adc1 voltage from adc1 to adc1+adcd
		a2=round(random.uniform(adc2, adc2+adcd), 2)				#adc2 voltage from adc2 to adc1+adcd
		dig1=1 														#digital sensor 1 ON
		fu=fu-round(fch/3600*pt,2)
		fuel=random.uniform(fu-fchr,fu+fchr)
		print("REG;"+str(t)+";"+str(a)+";"+str(b)+";0;0;ALT:0.0,adc1:"+str(a1)+",adc2:"+str(a2)+",fuel:"+str(fuel)+";SATS:"+str(sats)+",in1:"+str(dig1)+";;")	
		t+=pt
		i-=1
	return t	

#######################
#park(utc_now,list(dic)[0],dic[list(dic)[0]])	#making 15 first messages
#######################
#utc_now=park(utc_now,list(dic)[0],dic[list(dic)[0]])
#print(utc_now, " - TIME!!!")
######################

#selector
def ch(utc_now, l):
	if l<10*mn:	
		tm=2
		sats=random.randint(sats_min,sats_max)		#sattelites randomizer
		sp=random.randint(1,round(speed/10))	#speed default 0 up to 5
	elif l<25*mn:	
		tm=5
		sats=random.randint(sats_min,sats_max)		#sattelites randomizer
		sp=random.randint(round(speed/10),round(speed/4))	#6 speed up to 15
	elif l<35*mn:	
		tm=5
		sats=random.randint(sats_min,sats_max)		#sattelites randomizer
		sp=random.randint(round(speed/4),round(speed/1.7))	#15 speed up to 35
	elif l<50*mn:	
		tm=5
		sats=random.randint(sats_min,sats_max)		#sattelites randomizer
		sp=random.randint(round(speed/1.7),round(speed/1.09))	#35 speed up to 55
	else:
		tm=int(round(l/16.7))	
		sats=random.randint(sats_min,sats_max)		#sattelites randomizer
		sp=random.randint(round(speed/1.09),speed)	#speed up to 60
	return tm,sats,sp

#print(dic)
def intp (utc_now):	#intermediate parkings (2 geozones)
	fu=fls 						# start fuel level
	for key in range(len(dic)):
	#REG;1603666800;37.6215976299;55.7734807486;2;343;ALT:0.0;SATS:10;;;;
	#UTC;LAT;LON;SPEED;COURSE;ALTITUDE;SATS;;;;
		try:
			la1=float(dic[key][0])
			lo1=float(dic[key][1])
			la2=float(dic[key-1][0])
			lo2=float(dic[key-1][1])
			l=round(abs(111000*((la1-la2)+(lo1-lo2)*math.cos(la1))))	#modul 111km* https://otvet.mail.ru/question/167181899
	#		print("The trip in meters - ", l)
	#		l=abs(la1+lo1-la2-lo2)	#modul 
		except:
			continue
		
		if dic[key] in ddic:	#checking the possible parking			
			utc_now=park_on(utc_now,la1,lo1,sop,fu)							#parking sensors ON
			utc_now=park(utc_now,la1,lo1,fu)									#parking
			utc_now=park_on(utc_now,la1,lo1,sop,fu)							#parking sensors ON
		else:
			a1=round(random.uniform(adc1, adc1+adcd), 2)				#adc1 voltage from adc1 to adc1+adcd
			a2=round(random.uniform(adc2, adc2+adcd), 2)				#adc2 voltage from adc2 to adc1+adcd
			dig1=1 														#digital sensor 1 ON

			tm,sats,sp=ch(utc_now, l)

			if sp<=isp:
				fu=fu-round(fch/3600*pt,2)
			elif isp<sp<=fs1:
				fu=fu-round(fcm1/100000*l,2)
			elif fs1<sp<=fs2:
				fu=fu-round(fcm2/10000*l,2)
			fuel=random.uniform(fu-fcmd,fu+fcmd)		
			print("REG;"+str(utc_now)+";"+str(la1)+";"+str(lo1)+";"+str(sp)+";0;ALT:0.0,adc1:"+str(a1)+",adc2:"+str(a2)+",fuel:"+str(fuel)+";SATS:"+str(sats)+",in1:"+str(dig1)+";;")	
			utc_now=utc_now+tm



def nop (utc_now):	#no intermediate parkings, only 1 trip geozone
	fu=fls
	utc_now=park(utc_now,dic[0][0],dic[0][1],fu)								#parking
	utc_now=park_on(utc_now,dic[0][0],dic[0][1],sop,fu)							#parking sensors ON
	for key in range(len(dic)):
	#REG;1603666800;37.6215976299;55.7734807486;2;343;ALT:0.0;SATS:10;;;;
	#UTC;LAT;LON;SPEED;COURSE;ALTITUDE;SATS;;;;
		try:
			la1=float(dic[key][0])
			lo1=float(dic[key][1])
			la2=float(dic[key-1][0])
			lo2=float(dic[key-1][1])
			l=round(abs(111000*((la1-la2)+(lo1-lo2)*math.cos(la1))))	#modul 111km* https://otvet.mail.ru/question/167181899
	#		print("The trip in meters - ", l)
	#		l=abs(la1+lo1-la2-lo2)	#modul 
		except:
			continue
		
		a1=round(random.uniform(adc1, adc1+adcd), 2)				#adc1 voltage from adc1 to adc1+adcd
		a2=round(random.uniform(adc2, adc2+adcd), 2)				#adc2 voltage from adc2 to adc1+adcd
		dig1=1

		tm,sats,sp=ch(utc_now, l)	

		if sp<=isp:
			fu=fu-round(fch/3600*pt,2)
		elif isp<sp<=fs1:
			fu=fu-round(fcm1/100000*l,2)
		elif fs1<sp<=fs2:
			fu=fu-round(fcm2/10000*l,2)
		fuel=random.uniform(fu-fcmd,fu+fcmd)			
		print("REG;"+str(utc_now)+";"+str(la1)+";"+str(lo1)+";"+str(sp)+";0;ALT:0.0,adc1:"+str(a1)+",adc2:"+str(a2)+",fuel:"+str(fuel)+";SATS:"+str(sats)+",in1:"+str(dig1)+";;")	
		utc_now=utc_now+tm
	utc_now=park_on(utc_now,dic[len(dic)-1][0],dic[len(dic)-1][1],sop,fu)
	utc_now=park(utc_now,dic[len(dic)-1][0],dic[len(dic)-1][1],fu)
	
#aadc random


#MAIN
#
if int_parks==1:
	ddic=[]
	b=a[24]	#dots coordinates string from KML
	b2=b.replace(',0',';').replace(' ','').replace('\n','').replace('\t\t\t\t\t','')
	b3=b2.split(';')
	#print(len(b3))
	for i in range(len(b3)-1):
		b4=b3[i]
		b5=b4.split(',')
		ddic.append(b5)
	#print(ddic)
	###
	dic=[]
	d=a[45]	#coordinates string from KML
	d2=d.replace(',0',';').replace(' ','').replace('\n','').replace('\t\t\t\t\t','')
	d3=d2.split(';')
	#print(len(d3))
	for i in range(len(d3)-1):
		d4=d3[i]
		d5=d4.split(',')
		if len(dic)==0:
			dic.append(d5)
		elif d5!=dic[len(dic)-1]:
			dic.append(d5)
	intp(utc_now)
else:
	dic=[]
	d=a[24]	#coordinates string from KML
	d2=d.replace(',0',';').replace(' ','').replace('\n','').replace('\t\t\t\t\t','')
	d3=d2.split(';')
	#print(len(d3))
	for i in range(len(d3)-1):
		d4=d3[i]
		d5=d4.split(',')
		if len(dic)==0:
			dic.append(d5)
		elif d5!=dic[len(dic)-1]:
			dic.append(d5)
	nop(utc_now)
#print(dic)
#print(ddic, dic)
#print(len(dic))


#######################
###########- checking time difference - ############
#print("Current UTC time in sec - ", round(time.time())," , the diff is: ", round(time.time())-utc_now)	#checking time difference, comment this string
#######################
#######################


