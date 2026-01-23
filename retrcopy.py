#!/bin/python3
#Develioed Novikov Siarhei @nose, 02.06.2022

#Require source\destination URL and TOKEN
#The retranslators' copies created from the source list, available for the source token. If there will be in destination account the retranslator with the same name - the additional retranslator with the same name will be created
#The script checks the retranslator 'creator' by exact name match. If the creator with the same name will be found in destination account - the creator will be set with this name. Otherwise - the creator will be set as a name of the token user.
#The second script mode allows to copy the units list. If the same unit name  from the source retranslator will be found in the destination account, the system will add this unit by name into the list of destination retranslator. Otherwise unit will be skipped, the record 'Unit: <SOURCE UNIT NAME> , NOT found in destination account! will be displayed
#The script doesn't check the ACL, access rules to create retranslators and to use units in the retranslators must be guarantee by the client.

#Known errors:
#"error":6 - the retranslator can not be created, if there is no such retranslator protocol. For example WL has CyberGLX retranslator protocol, but there is no such on Hosting at all.
#Unit ID: XXXX  - not found. Pribably deleted from the system, but stored in the retranslator's property.  - Possible bug was found. If the unit add into retranslator, delete the unit from the system - on display the retranslator won't have this unit in the list, but still it will be in the retranslator's list through API. 

import requests,json

#global variables 
rsa=input("Enter the retransator source address, e.g.: https://hst-api.wialon.com: ")
st=input("Enter the source access token: ")
#rsa='https://cms-local.wialontest.com'			#retransator source address
#st='0133933863ed12823b5b5a83ca646bd0B91B24AA9B6F3308BD420FB9102BCD68E65D1FE8'										#source access token
login_s=requests.post(rsa+'/wialon/ajax.html?svc=token/login&params={"token":"'+str(st)+'"}')
ssid=login_s.json()['eid']						#sorce SID
suid=login_s.json()['user']['id']				#source user ID
sunm=login_s.json()['user']['nm']				#source user name
s_users_dict={suid:sunm}						#source users dictionary ID:NAME, added token user

print('---------------------------------------------------------------------------------------------------')
rsd=input("Enter the retransator destination address, e.g.: https://hst-api.wialon.com: ")
dt=input("Enter the destination access token: ")
#rsd='https://hst-api.wialon.com'				#retranslator destination address
#dt='a65c6e0b6745279bf440a7fb47281bf090DEA311625C3F9EA48BDAA232704E8BF8A4B0D7'										#destination access token
login_d=requests.post(rsd+'/wialon/ajax.html?svc=token/login&params={"token":"'+str(dt)+'"}')
dsid=login_d.json()['eid']						#destination SID
duid=login_d.json()['user']['id']				#destination user ID
dunm=login_d.json()['user']['nm']				#destination user name
d_users_dict={dunm:duid}						#detination users dictionary NAME:ID, added token user
print('---------------------------------------------------------------------------------------------------')

#ID:NAME and NAME:ID is for further search by source ID->NAME = destination NAME->ID
#############################################################################################################################################
print("Source ",rsa, sunm, "| got SID: ", ssid)
print("Destination  ",rsd, dunm, "| got SID: ", dsid)
print('##############################################################################################')
#mode selector
def ch():
	choice=input("Choose the retranslators creation mode.\n1 - just retranslator configuration (without units)\n2 - retranslator with the units (if the same units by name will be found)\n1 or 2: ")
	if choice=='1':
		print("Trying to create the retranslators without units\n")
		retr()
		print("##############################################################################################\nScript work completed!\n")
	elif choice=='2':
		print("Trying to create the retranslators with units\n")
		retrun()
		print("##############################################################################################\nScript work completed!\n")
	else:
		print('Wrong choice ')
		ch()

###########################################################################################################################################################################################
# retranslator copying without units 
def retr():
	sear_us=requests.post(rsa+'/wialon/ajax.html?svc=core/search_items&params={"spec":{"itemsType":"user","propName":"*","propValueMask":"*","sortType":"*"},"force":1,"flags":1,"from":0,"to":0}&sid='+ssid)
	for i in range(len(sear_us.json()['items'])):
		s_users_dict[sear_us.json()['items'][i]['id']]=sear_us.json()['items'][i]['nm']
#	print('Source users ID:NAME list:\n',s_users_dict)

	sear_ud=requests.post(rsd+'/wialon/ajax.html?svc=core/search_items&params={"spec":{"itemsType":"user","propName":"*","propValueMask":"*","sortType":"*"},"force":1,"flags":1,"from":0,"to":0}&sid='+dsid)
	for i in range(len(sear_ud.json()['items'])):
		d_users_dict[sear_ud.json()['items'][i]['nm']]=sear_ud.json()['items'][i]['id']
#	print('Destination users NAME:ID list:\n',d_users_dict)

	sear_r=requests.post(rsa+'/wialon/ajax.html?svc=core/search_items&params={"spec":{"itemsType":"avl_retranslator","propName":"retranslator_units","propValueMask":"*","sortType":"retranslator_units"},"force":1,"flags":263,"from":0,"to":0}&sid='+ssid)
	s_retr=sear_r.json()['items']
#	print(s_retr)
	for i in range(len(s_retr)):
		print('----------------------------------- Trying to create: ', s_retr[i]['nm'], '-----------------------------------')
		if s_users_dict[s_retr[i]['crt']] in d_users_dict:
#			print(rsd+'/wialon/ajax.html?svc=core/create_retranslator&params={"creatorId":'+str(d_users_dict[s_users_dict[s_retr[i]['crt']]])+',"name":"'+str(s_retr[i]['nm'])+'","config":'+str(s_retr[i]['rtrc']).replace("'",'"')+',"dataFlags":1}&sid='+dsid)
			try:
				print("Creator found, ", s_users_dict[s_retr[i]['crt']],", id: ", s_retr[i]['crt'])
				c_retr=requests.post(rsd+'/wialon/ajax.html?svc=core/create_retranslator&params={"creatorId":'+str(d_users_dict[s_users_dict[s_retr[i]['crt']]])+',"name":"'+str(s_retr[i]['nm'])+'","config":'+str(s_retr[i]['rtrc']).replace("'",'"')+',"dataFlags":1}&sid='+dsid)
				print(c_retr.json())
			except:
				continue
		else:
#			print(rsd+'/wialon/ajax.html?svc=core/create_retranslator&params={"creatorId":'+str(duid)+',"name":"'+str(s_retr[i]['nm'])+'","config":'+str(s_retr[i]['rtrc']).replace("'",'"')+',"dataFlags":1}&sid='+dsid)

			try:
				print("Creator not found, applying ", dunm,", id: ",duid)
				c_retr=requests.post(rsd+'/wialon/ajax.html?svc=core/create_retranslator&params={"creatorId":'+str(duid)+',"name":"'+str(s_retr[i]['nm'])+'","config":'+str(s_retr[i]['rtrc']).replace("'",'"')+',"dataFlags":1}&sid='+dsid)
				print(c_retr.json())
			except:
				continue

###########################################################################################################################################################################################
# retranslator copying with units 
def retrun():
	sear_us=requests.post(rsa+'/wialon/ajax.html?svc=core/search_items&params={"spec":{"itemsType":"user","propName":"*","propValueMask":"*","sortType":"*"},"force":1,"flags":1,"from":0,"to":0}&sid='+ssid)
	for i in range(len(sear_us.json()['items'])):
		s_users_dict[sear_us.json()['items'][i]['id']]=sear_us.json()['items'][i]['nm']
#	print('Source users ID:NAME list:\n',s_users_dict)

	s_units_dict={}				#Empty dictionary for the source units list ID:NAME
	sear_uns=requests.post(rsa+'/wialon/ajax.html?svc=core/search_items&params={"spec":{"itemsType":"avl_unit","propName":"*","propValueMask":"*","sortType":"*"},"force":1,"flags":1,"from":0,"to":0}&sid='+ssid)
	for i in range(len(sear_uns.json()['items'])):
		s_units_dict[sear_uns.json()['items'][i]['id']]=sear_uns.json()['items'][i]['nm']
#	print("Source service units list: \n", s_units_dict)

	sear_ud=requests.post(rsd+'/wialon/ajax.html?svc=core/search_items&params={"spec":{"itemsType":"user","propName":"*","propValueMask":"*","sortType":"*"},"force":1,"flags":1,"from":0,"to":0}&sid='+dsid)
	for i in range(len(sear_ud.json()['items'])):
		d_users_dict[sear_ud.json()['items'][i]['nm']]=sear_ud.json()['items'][i]['id']
#	print('Destination users NAME:ID list:\n',d_users_dict)

	d_units_dict={}				#Empty dictionary for the destination units list NAME:ID
	sear_und=requests.post(rsd+'/wialon/ajax.html?svc=core/search_items&params={"spec":{"itemsType":"avl_unit","propName":"*","propValueMask":"*","sortType":"*"},"force":1,"flags":1,"from":0,"to":0}&sid='+dsid)
	for i in range(len(sear_und.json()['items'])):
		d_units_dict[sear_und.json()['items'][i]['nm']]=sear_und.json()['items'][i]['id']
#	print("Destination service units list: \n", d_units_dict)

	sear_r=requests.post(rsa+'/wialon/ajax.html?svc=core/search_items&params={"spec":{"itemsType":"avl_retranslator","propName":"retranslator_units","propValueMask":"*","sortType":"retranslator_units"},"force":1,"flags":775,"from":0,"to":0}&sid='+ssid)
	s_retr=sear_r.json()['items']
#	print(s_retr)
#	print(s_units_dict)
#	print(d_units_dict)
#	print(s_retr)
	for i in range(len(s_retr)):
		print('----------------------------------- Trying to create: ', s_retr[i]['nm'], '-----------------------------------')
		if s_users_dict[s_retr[i]['crt']] in d_users_dict:
#			print(rsd+'/wialon/ajax.html?svc=core/create_retranslator&params={"creatorId":'+str(d_users_dict[s_users_dict[s_retr[i]['crt']]])+',"name":"'+str(s_retr[i]['nm'])+'","config":'+str(s_retr[i]['rtrc']).replace("'",'"')+',"dataFlags":1}&sid='+dsid)
			try:
				print("Creator found, ", s_users_dict[s_retr[i]['crt']],", id: ", s_retr[i]['crt'])
				c_retr=requests.post(rsd+'/wialon/ajax.html?svc=core/create_retranslator&params={"creatorId":'+str(d_users_dict[s_users_dict[s_retr[i]['crt']]])+',"name":"'+str(s_retr[i]['nm'])+'","config":'+str(s_retr[i]['rtrc']).replace("'",'"')+',"dataFlags":1}&sid='+dsid)
				print(c_retr.json())
				c_retr_id=c_retr.json()['item']['id']
			except:
				continue
		else:
#			print(rsd+'/wialon/ajax.html?svc=core/create_retranslator&params={"creatorId":'+str(duid)+',"name":"'+str(s_retr[i]['nm'])+'","config":'+str(s_retr[i]['rtrc']).replace("'",'"')+',"dataFlags":1}&sid='+dsid)

			try:
				print("Creator not found, applying ", dunm,", id: ",duid)
				c_retr=requests.post(rsd+'/wialon/ajax.html?svc=core/create_retranslator&params={"creatorId":'+str(duid)+',"name":"'+str(s_retr[i]['nm'])+'","config":'+str(s_retr[i]['rtrc']).replace("'",'"')+',"dataFlags":1}&sid='+dsid)
				print(c_retr.json())
				c_retr_id=c_retr.json()['item']['id']

			except:
				continue
#		print(len(s_retr[i]['rtru']))
		if len(s_retr[i]['rtru'])!=0:
			rtr_units_list=[]
			for k in range(len(s_retr[i]['rtru'])):
				un_id=s_retr[i]['rtru'][k]['i']				#Retranslator unit ID	
				if un_id in s_units_dict:					#Possible bug was found. If the unit add into retranslator, delete the unit from the system - on display the retranslator won't have this unit in the list, but still it will be in the retranslator's list through API. Probably will be fixed, discussed with @mani 2 JUN 2022 https://gurtam.slack.com/archives/D013SKK63L6/p1654157936682649
					if s_units_dict[un_id] in d_units_dict:
						print('Unit: ', s_units_dict[un_id],' , found. Adding into retransator\n')
						rtr_un_prop={"i":d_units_dict[s_units_dict[un_id]],"a":s_retr[i]['rtru'][k]['a']}			#retranslator's unit properties
						rtr_units_list.append(rtr_un_prop)
					else:
						print('Unit: ', s_units_dict[un_id],' , NOT found in destination account!\n')
					print(rtr_units_list)
					try:
						un_upd_rtr=requests.post(rsd+'/wialon/ajax.html?svc=retranslator/update_units&params={"itemId":'+str(c_retr_id)+',"units":'+str(rtr_units_list).replace("'",'"')+',"dataFlags":1}&sid='+dsid)
						print(un_upd_rtr.json())
					except:
						continue
				else:
					print('Unit ID: ', un_id, " - not found. Pribably deleted from the system, but stored in the retranslator's property.")
		else:
			print('No units found! No units to update in retranslator. \n')



'''

https://local.wialontest.com/wialon/ajax.html?svc=core/search_items&params={"spec":{"itemsType":"avl_unit","propName":"*","propValueMask":"*","sortType":"*"},"force":1,"flags":1,"from":0,"to":0}&sid=8423bdf37bd5e1da6173c49c90f7226c


https://local.wialontest.com/wialon/ajax.html?svc=core/search_items&params={"spec":{"itemsType":"avl_retranslator","propName":"retranslator_units","propValueMask":"*","sortType":"retranslator_units"},"force":1,"flags":4611686018427387903,"from":0,"to":0}&sid=0b5378de202d4f7d7d3bb4f3d248c982

https://cms-local.wialontest.com/wialon/ajax.html?svc=core/create_retranslator&sid=a9ef564f3ffe2449fe3823608ebe33ab&params={"creatorId":998,"name":"test_aaa","config":{"protocol":"wialon","server":"111.222.333.444","port":"20163","attach_sensors":0},"dataFlags":1}
https://hst-api.wialon.com/wialon/ajax.html?svc=core/create_retranslator&params={"creatorId":5622128,"name":"nose2_retr","config":{"protocol":"adams","sender_id":"e14","server":"api.server.ru","x_api_key":"gkjrk2j342dngd"}},"dataFlags":1}&sid=023ba4e2a92a084ee296cb10ed16d95e
https://hst-api.wialon.com/wialon/ajax.html?svc=core/create_retranslator&sid=02e26fce88c3970b6cdcd801e7abfbd&params={"creatorId":5622128,"name":"nose2_retr","config":{"protocol":"adams","server":"api.server.ru","x_api_key":"gkjrk2j342dngd","sender_id":"e14"},"dataFlags":1}



{"creatorId":998,"name":"test_aaa","config":{"protocol":"wialon","server":"111.222.333.444","port":"20163","attach_sensors":0},"dataFlags":1}
{"creatorId":5622128,"name":"nose2_retr","config":{"protocol":"adams","sender_id":"e14","server":"api.server.ru","x_api_key":"gkjrk2j342dngd"}},"dataFlags":1}
{"creatorId":5622128,"name":"nose2_retr","config":{"protocol":"adams","server":"api.server.ru","x_api_key":"gkjrk2j342dngd","sender_id":"e14"},"dataFlags":1}



https://cms-local.wialontest.com/wialon/ajax.html?svc=core/batch&sid=a9ef564f3ffe2449fe3823608ebe33ab&params={"params":[{"svc":"retranslator/update_config","params":{"itemId":4617,"config":{"protocol":"wialon","server":"111.222.333.444","port":"20163","attach_sensors":0}}},{"svc":"retranslator/update_units","params":{"itemId":4617,"units":[{"i":4153,"a":"xcom12"},{"i":1845,"a":"866104029559161_"}]}}],"flags":0}
'''
ch()
