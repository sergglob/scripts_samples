#!/usr/bin/python3
#  icon, ACL, unit groups, agro, maintenance
#Developed by Novikov Sergey (nose)
#version 20.06.2022 for WL2204
#version 06.06.2022, units group copying added.
print("This is a python script to test SDK API wialon requests")
addr=input("Enter the sorce FROM URL with the http/https prefix, like 'http://hst-api.wialon.com': ")
#addr="http://hst-api.wialon.com"	#temp hosting hst api
tok=input("Enter the valid sorce user token: ")
#tok="a65c6e0b6745279bf440a7fb47281bf0EE91A0437227FAB76A8860B1A26B86B5962114AB"	#temp wialon hosting token
print("Sorce: ",addr, tok)
daddr=input("Enter the target TO URL with the http/https prefix, like 'http://hst-api.wialon.com': ")
#daddr="http://local.wialontest.com"	#temp wialon local address
dtok=input("Enter the valid target token: ")
#dtok="0133933863ed12823b5b5a83ca646bd0EF21DAA446A5D4E2E100ABA130F3AD861A5EC338"	#temp wialon local token
print("Sorce: ",addr, tok)
print("Target: ",daddr, dtok)
print("Trying to exec token login request")
import requests
import json
resp=requests.get(addr+'/wialon/ajax.html?svc=token/login&params={"token":"'+tok+'"}')
dresp=requests.get(daddr+'/wialon/ajax.html?svc=token/login&params={"token":"'+dtok+'"}')
#print(resp.status_code)
#print(resp.json())
st=resp.status_code
dst=dresp.status_code
data=resp.json()	#source token response
ddata=dresp.json()	#destination token response
sid=data['eid']
dsid=ddata['eid']
accid=data['user']['id']	#sorce user ID
daccid=ddata['user']['id']	#target user ID
nm=data['user']['nm']		#source user name
dnm=ddata['user']['nm']		#target user name
print("Source SID: ", sid, nm, accid)
print("Destination SID: ", dsid, dnm, daccid)
#

###########################################################UNIT PROPERTIES
def props(ex, unid, dhwid):
	exj=ex.json()	#dest unit props
	exjid=exj["item"]["id"]	#new unit ID
	print('#################| updating properties UNIT:',exj['item']['nm'],' |#################')
	pr=requests.post(addr+'/wialon/ajax.html?svc=core/search_item&params={"id":"'+str(unid)+'","flags":4611686018427387903}&sid='+sid)
	prj=pr.json()	#target unit props
	prjpu=prj['item']	#sorce unit props
	psw=prjpu['psw']
	rm_plus=prjpu["ph"] #remove + from phone number to replace it with %2B
	print("Importing general tab props")
	upd_gen=requests.post(daddr+'/wialon/ajax.html?svc=core/batch&params={"params":[{"svc":"unit/update_device_type","params":{"itemId":'+str(exjid)+',"deviceTypeId":"'+str(dhwid)+'","uniqueId":"'+str(prjpu["uid"])+'"}},{"svc":"unit/update_phone","params":{"itemId":'+str(exjid)+',"phoneNumber":"'+str("%2B"+rm_plus[1:])+'"}},{"svc":"unit/update_access_password","params":{"itemId":'+str(exjid)+',"accessPassword":"'+str(psw)+'"}},{"svc":"unit/update_calc_flags","params":{"itemId":'+str(exjid)+',"newValue":"'+str(prjpu['cfl'])+'"}},{"svc":"unit/update_mileage_counter","params":{"itemId":'+str(exjid)+',"newValue":'+str(prjpu['cnm'])+'}},{"svc":"unit/update_eh_counter","params":{"itemId":'+str(exjid)+',"newValue":'+str(prjpu['cneh'])+'}},{"svc":"unit/update_traffic_counter","params":{"itemId":'+str(exjid)+',"newValue":'+str(prjpu['cnkb'])+',"regReset":0}}],"flags":0}&sid='+dsid)	#update general props
	print(upd_gen.json())
#
	print("Importing custom fields")
	if len(prjpu['flds'])!=0:
		print(len(prjpu['flds']), " - custom fields found")
		c=0	
		for key in prjpu['flds']:
			upd_cust=requests.post(daddr+'/wialon/ajax.html?svc=core/batch&params={"params":[{"svc":"item/update_custom_field","params":{"id":'+str(c)+',"n":"'+str(prjpu['flds'][''+str(key)+'']['n'])+'","v":"'+str(prjpu['flds'][''+str(key)+'']['v'])+'","itemId":'+str(exjid)+',"callMode":"create"}}],"flags":0}&sid='+dsid)		#update custom fields
			c+=1
			print(upd_cust.json())
	else:
		print("No custom fields found")
#
	print("Importing admin fields")
	if len(prjpu['aflds'])!=0:
		print(len(prjpu['aflds']), " - admin fields found")
		cc=0
		for ke in prjpu['aflds']:
			upd_adm=requests.post(daddr+'/wialon/ajax.html?svc=core/batch&params={"params":[{"svc":"item/update_admin_field","params":{"id":'+str(cc)+',"n":"'+str(prjpu['aflds'][''+str(ke)+'']['n'])+'","v":"'+str(prjpu['aflds'][''+str(ke)+'']['v'])+'","itemId":'+str(exjid)+',"callMode":"create"}}],"flags":0}&sid='+dsid)		#update admin fields
			print(upd_adm.json())		
	else:
		print("No admin fields found")
#
	print("Importing commands")
	if len(prjpu['cml'])!=0:
		print(len(prjpu['cml']), " - commands found")
		for s in prjpu['cml']:
			upd_comm=requests.post(daddr+'/wialon/ajax.html?svc=core/batch&params={"params":[{"svc":"unit/update_command_definition","params":{"id":'+str(s)+',"n":"'+str(prjpu['cml'][''+str(s)+'']['n'])+'","c":"'+str(prjpu['cml'][''+str(s)+'']['c'])+'","l":"'+str(prjpu['cml'][''+str(s)+'']['l'])+'","p":"'+str(prjpu['cml'][''+str(s)+'']['p'])+'","a":'+str(prjpu['cml'][''+str(s)+'']['a'])+',"f":"'+str(prjpu['cml'][''+str(s)+'']['f'])+'","que_length":0,"itemId":'+str(exjid)+',"callMode":"create"}}],"flags":0}&sid='+dsid)	#update commands
			print(upd_comm.json())
	else:
		print("No commands found")
#
	print("Importing trips detector tab")
	upd_trip=requests.post(daddr+'/wialon/ajax.html?svc=core/batch&params={"params":[{"svc":"unit/update_trip_detector","params":{"itemId":'+str(exjid)+',"type":'+str(prjpu['rtd']['type'])+',"gpsCorrection":'+str(prjpu['rtd']['gpsCorrection'])+',"minSat":'+str(prjpu['rtd']['minSat'])+',"minMovingSpeed":'+str(prjpu['rtd']['minMovingSpeed'])+',"minStayTime":'+str(prjpu['rtd']['minStayTime'])+',"maxMessagesDistance":'+str(prjpu['rtd']['maxMessagesDistance'])+',"minTripTime":'+str(prjpu['rtd']['minTripTime'])+',"minTripDistance":'+str(prjpu['rtd']['minTripDistance'])+'}}],"flags":0}&sid='+dsid)	#update trips detector
	print(upd_trip.json())

#
	print("Importing characteristics")
	if len(prjpu['pflds'])!=0:
		print(len(prjpu['pflds']), " - characteristcs found")
		for fl in prjpu['pflds']:
			upd_char=requests.post(daddr+'/wialon/ajax.html?svc=core/batch&params={"params":[{"svc":"item/update_profile_field","params":{"itemId":'+str(exjid)+',"n":"'+str(prjpu['pflds'][''+fl+'']['n'])+'","v":"'+str(prjpu['pflds'][''+fl+'']['v'])+'"}}],"flags":0}&sid='+dsid)	#update characteristics
			print(upd_char.json())
	else:
		print("No characteristics found")
#
	print("Importing sensors")
	if len(prjpu['sens'])!=0:
		print(len(prjpu['sens'])," - sensors found")
		for se in prjpu['sens']:
			upd_sens=requests.post(daddr+'/wialon/ajax.html?svc=core/batch&params={"params":[{"svc":"unit/update_sensor","params":{"n":"'+str(prjpu['sens'][''+str(se)+'']['n'])+'","t":"'+str(prjpu['sens'][''+str(se)+'']['t'])+'","d":"'+str(prjpu['sens'][''+str(se)+'']['d'])+'","m":"'+str(prjpu['sens'][''+str(se)+'']['m'])+'","p":"'+str(prjpu['sens'][''+str(se)+'']['p']).replace('+','%2B').replace('#','%23').replace('^','%5E').replace('\\','%2F').replace(':','%3A')+'","f":'+str(prjpu['sens'][''+str(se)+'']['f'])+',"c":"'+str(prjpu['sens'][''+str(se)+'']['c'].replace('"','\\"'))+'","vt":'+str(prjpu['sens'][''+str(se)+'']['vt'])+',"vs":'+str(prjpu['sens'][''+str(se)+'']['vs'])+',"tbl":'+str(prjpu['sens'][''+str(se)+'']['tbl']).replace(' ','').replace("'", '"')+',"id":'+str(prjpu['sens'][''+str(se)+'']['id'])+',"itemId":'+str(exjid)+',"callMode":"create"}}],"flags":0}&sid='+dsid)	#create sensors
			print(upd_sens.json())
	else:
		print("No sensors found")	
#
	print("Importing eco")
	ec=requests.post(addr+'/wialon/ajax.html?svc=unit/get_drive_rank_settings&params={"itemId":'+str(unid)+'}&sid='+sid)
	ecj=ec.json()
	if 'global' in ecj:
		upd_eco=requests.post(daddr+'/wialon/ajax.html?svc=core/batch&params={"params":[{"svc":"unit/update_drive_rank_settings","params":{"itemId":'+str(exjid)+',"driveRank":'+str(ecj).replace(' ','').replace("'", '"')[0:-1]+',"global":{"accel_mode":"'+str(ecj['global']['accel_mode'])+'"}}}}],"flags":0}&sid='+dsid)	#create eco criterias
		print(upd_eco.json())
	else:
		print("No eco settings found")
			
#		
	print("Importing advance tab settings")
	adv=requests.post(addr+'/wialon/ajax.html?svc=core/batch&params={"params":[{"svc":"unit/get_activity_settings","params":{"itemId":'+str(unid)+'}},{"svc":"unit/get_report_settings","params":{"itemId":'+str(unid)+'}},{"svc":"unit/get_messages_filter","params":{"itemId":'+str(unid)+'}}],"flags":0}&sid='+sid)
	advj=adv.json()
	upd_adv=requests.post(daddr+'/wialon/ajax.html?svc=core/batch&params={"params":[{"svc":"unit/update_activity_settings","params":{"itemId":'+str(exjid)+',"type":'+str(advj[0]["type"])+'}},{"svc":"unit/update_report_settings","params":{"itemId":'+str(exjid)+',"params":{"maxMessagesInterval":'+str(advj[1]["maxMessagesInterval"])+',"fuelRateCoefficient":'+str(advj[1]["fuelRateCoefficient"])+',"dailyEngineHoursRate":'+str(advj[1]["dailyEngineHoursRate"])+',"urbanMaxSpeed":'+str(advj[1]["urbanMaxSpeed"])+',"mileageCoefficient":'+str(advj[1]["mileageCoefficient"])+',"speedingMode":'+str(advj[1]["speedingMode"])+',"speedLimit":'+str(advj[1]["speedLimit"])+',"speedingTolerance":'+str(advj[1]["speedingTolerance"])+',"speedingMinDuration":'+str(advj[1]["speedingMinDuration"])+'}}},{"svc":"unit/update_messages_filter","params":{"itemId":'+str(exjid)+',"enabled":'+str(advj[2]["enabled"])+',"skipInvalid":'+str(advj[2]["skipInvalid"])+',"minSats":'+str(advj[2]["minSats"])+',"maxHdop":'+str(advj[2]["maxHdop"])+',"maxSpeed":'+str(advj[2]["maxSpeed"])+',"lbsCorrection":'+str(advj[2]["lbsCorrection"])+'}}],"flags":0}&sid='+dsid)	# updating activity type, reports constants, sats filtration level
	print(upd_adv.json())
	seas=requests.post(addr+'/wialon/ajax.html?svc=unit/get_fuel_settings&params={"itemId":'+str(unid)+'}&sid='+sid)
	seasj=seas.json()
	upd_seas=requests.post(daddr+'/wialon/ajax.html?svc=core/batch&params={"params":[{"svc":"unit/update_fuel_rates_params","params":{"itemId":'+str(exjid)+',"idlingSummer":0,"idlingWinter":0,"consSummer":'+str(seasj['fuelConsRates']['consSummer'])+',"consWinter":'+str(seasj['fuelConsRates']['consWinter'])+',"winterMonthFrom":'+str(seasj['fuelConsRates']['winterMonthFrom'])+',"winterDayFrom":'+str(seasj['fuelConsRates']['winterDayFrom'])+',"winterMonthTo":'+str(seasj['fuelConsRates']['winterMonthTo'])+',"winterDayTo":'+str(seasj['fuelConsRates']['winterDayTo'])+'}}],"flags":0}&sid='+dsid)	#updating season fuel settings
	print(upd_seas.json())
	for kz in prjpu['prp']:
		upd_colors=requests.post(daddr+'/wialon/ajax.html?svc=item/update_custom_property&params={"itemId":'+str(exjid)+',"name":"'+str(kz)+'","value":"'+str(prjpu['prp'][''+str(kz)+''])+'"}&sid='+dsid)	#update colors
		print(upd_colors.json())
	print('#################')
	print("Properties import completed.")

###########################################################UNITS
def crunits():
#getting units list
	u=requests.post(addr+'/wialon/ajax.html?svc=core/search_items&params={"spec":{"itemsType":"avl_unit","propName":"","propValueMask":"*","sortType":"","propType":""},"force":1,"flags":4611686018427387903,"from":0,"to":0}&sid='+sid)
#	print(addr+'/wialon/ajax.html?svc=core/search_items&params={"spec":{"itemsType":"avl_unit","propName":"","propValueMask":"*","sortType":"","propType":""},"force":1,"flags":4611686018427387903,"from":0,"to":0}&sid='+sid)
	units=u.json()
#getting hw types
	hw_r=requests.post(addr+'/wialon/ajax.html?svc=core/get_hw_types&params={"filterType":"name","filterValue":"id","includeType":1,"ignoreRename":1}&sid='+sid)
	dhw_r=requests.post(daddr+'/wialon/ajax.html?svc=core/get_hw_types&params={"filterType":"name","filterValue":"id","includeType":1,"ignoreRename":1}&sid='+dsid)
	hw=hw_r.json()	#list of source hardware
	dhw=dhw_r.json() #list of destination hardware
	search_dus=requests.post(daddr+'/wialon/ajax.html?svc=core/search_items&params={"spec":{"itemsType":"user","propName":"sys_name","propValueMask":"*","sortType":"sys_name","or_logic":0},"force":1,"flags":1,"from":0,"to":0}&sid='+dsid)	#searching users on target server
	search=search_dus.json()
	tusearch=search['items']	#list of target server users
	for h in range(len(dhw)):
		if dhw[h]['name']=='Wialon Retranslator':
			dhwwr=dhw[h]['id']
	print("Default HW WIALON RETRANSLATOR: ", dhwwr)
	for i in range(len(units['items'])):
		print('----------------------------')
		print("Trying ", i+1, " from ", len(units['items'])) 
		print('----------------------------')
		un=units['items'][i]
#		print(un)
		try:
			dhwid=hws(un['hw'],hw,dhw,dhwwr)
			dcrt=tcrt(un['crt'],tusearch,daccid)
			print("Creating unit: ", un['nm'])
			ex=requests.post(daddr+'/wialon/ajax.html?svc=core/create_unit&params={"creatorId":"'+str(dcrt)+'","name":"'+str(un['nm'])+'","hwTypeId":"'+str(dhwid)+'","dataFlags":1}&sid='+dsid)
			print(ex.json())
			print("\nUnit creation completed\n----------------------------")
			props(ex, un['id'], dhwid)				#updating units properties
			print("###############################################################################################################################################")
		except:
			print("----------------------------\n!!!!!!!!!!! -------- Error creating unit. Probably no enough rights to read the source unit properties")
			print("###############################################################################################################################################")
			continue

# searching target hardware
def hws (hw,hws,hwt,hwwr):	#sorce unit hw id, list of sorce hw, list of target hw, target wialon retranslator hw type
	unithw=hwwr
	for i in range(len(hws)):
		if hw==hws[i]['id']:
			hwname=hws[i]['name']
	for j in range(len(hwt)):
			if hwname==hwt[j]['name']:
				unithw=hwt[j]['id']
	print("Applying HW ID ", unithw)
	return unithw
	
# searching target creator
def tcrt(uncrt,tuslist,tokus):	#unit creator id, list of the users on target server, token user id
	targcrt=tokus
	us_r=requests.post(addr+'/wialon/ajax.html?svc=core/search_item&params={"id":"'+str(uncrt)+'","flags":1}&sid='+sid) #search creator user by ID
	us=us_r.json() #sorce user
	usname=us['item']['nm']
	for i in range(len(tuslist)):
		if usname==tuslist[i]['nm']:
			print("New creator found! ", usname)
			targcrt=tuslist[i]['id']
		else:
			print("Creator not found, using token creator ", usname)
	return targcrt

# creating  units' grops
def ungrp ():
	sgrp=requests.post(addr+'/wialon/ajax.html?svc=core/search_items&params={"spec":{"itemsType":"avl_unit_group","propName":"","propValueMask":"*","sortType":"","propType":""},"force":1,"flags":5,"from":0,"to":0}&sid='+sid) #search source units' groups
	sgrpj=sgrp.json()['items']
	sun=requests.post(addr+'/wialon/ajax.html?svc=core/search_items&params={"spec":{"itemsType":"avl_unit","propName":"","propValueMask":"*","sortType":"","propType":""},"force":1,"flags":1,"from":0,"to":0}&sid='+sid) #search source units
	sunj=sun.json()['items']
#	print(sunj)
	dun=requests.post(daddr+'/wialon/ajax.html?svc=core/search_items&params={"spec":{"itemsType":"avl_unit","propName":"","propValueMask":"*","sortType":"","propType":""},"force":1,"flags":1,"from":0,"to":0}&sid='+dsid) #search target units	
	dunj=dun.json()['items']
#	print(dunj)
	sus=requests.post(addr+'/wialon/ajax.html?svc=core/search_items&params={"spec":{"itemsType":"user","propName":"","propValueMask":"*","sortType":"","propType":""},"force":1,"flags":1,"from":0,"to":0}&sid='+sid) #search source users
	susj=sus.json()['items']
#	print(susj)
	dus=requests.post(daddr+'/wialon/ajax.html?svc=core/search_items&params={"spec":{"itemsType":"user","propName":"","propValueMask":"*","sortType":"","propType":""},"force":1,"flags":1,"from":0,"to":0}&sid='+dsid) #search target users
	dusj=dus.json()['items']
#	print(dusj)
	#creating  dictionaries
	sunj_dict={}
	for i in range(len(sunj)):
		sunj_dict[sunj[i]['id']]=sunj[i]['nm']		#source units ID/NAME list
	dunj_dict={}
	for i in range(len(dunj)):
		dunj_dict[dunj[i]['nm']]=dunj[i]['id']		#destination units NAME/ID list
	susj_dict={accid:nm}	
	for i in range(len(susj)):
		susj_dict[susj[i]['id']]=susj[i]['nm']		#source user ID/NAME list
	dusj_dict={dnm:daccid}	
	for i in range(len(dusj)):
		dusj_dict[dusj[i]['nm']]=dusj[i]['id']		#destination user NAME/ID list
	#creating units groups
	for i in range(len(sgrpj)):
		print('-------------------------Trying create group ', sgrpj[i]['nm'], '-------------------------')
		if sgrpj[i]['crt'] in susj_dict:
			if susj_dict[sgrpj[i]['crt']] in dusj_dict:
				crtgrp=requests.post(daddr+'/wialon/ajax.html?svc=core/create_unit_group&params={"creatorId":'+str(dusj_dict[susj_dict[sgrpj[i]['crt']]])+',"name":"'+str(sgrpj[i]['nm'])+'","dataFlags":1}&sid='+dsid)
				grpcrt=crtgrp.json()['item']['id']			#created units group ID
				print('Group created: ', sgrpj[i]['nm'], grpcrt)
				print("Trying update units in group")
				gun=[]			#new units IDs in group
				if len(sgrpj[i]['u'])!=0:
					for j in range(len(sgrpj[i]['u'])):
	#					print(sunj_dict[sgrpj[i]['u'][j]], ' ---  ', dunj_dict)
						if sunj_dict[sgrpj[i]['u'][j]] in dunj_dict:
							print("----111--- ", dunj_dict)
							print("----22--- ", sunj_dict[sgrpj[i]['u'][j]])
							gun.append(dunj_dict[sunj_dict[sgrpj[i]['u'][j]]])
						else:
							print('Unit not found on destination account: ', sunj_dict[sgrpj[i]['u'][j]])
				updgrp=requests.post(daddr+'/wialon/ajax.html?svc=unit_group/update_units&params={"itemId":'+str(grpcrt)+',"units":'+str(gun)+'}&sid='+dsid)
				print('Group updated with units IDs: ', updgrp.json())
			else:
				print("Units group creator not found,applying main token user")
				crtgrp=requests.post(daddr+'/wialon/ajax.html?svc=core/create_unit_group&params={"creatorId":'+str(daccid)+',"name":"'+str(sgrpj[i]['nm'])+'","dataFlags":1}&sid='+dsid)
				grpcrt=crtgrp.json()['item']['id']			#created units group ID
				print('Group created: ', sgrpj[i]['nm'])
				if len(sgrpj[i]['u'])!=0:
					gun=[]			#new units IDs in group
					for j in range(len(sgrpj[i]['u'])):
						if sunj_dict[sgrpj[i]['u'][j]] in dunj_dict:
							gun.append(dunj_dict[sunj_dict[sgrpj[i]['u'][j]]])
						else:
							print('Unit not found on destination account: ', susj_dict[sgrpj[i]['u'][j]])
				updgrp=requests.post(daddr+'/wialon/ajax.html?svc=unit_group/update_units&params={"itemId":'+str(grpcrt)+',"units":'+str(gun)+'}&sid='+dsid)
				print('Group updated with units IDs: ', updgrp.json())
		else:
			print("Units group creator not found in the source list. Applying the source token user creator.")
			print(daddr+'/wialon/ajax.html?svc=core/create_unit_group&params={"creatorId":'+str(daccid)+',"name":"'+str(sgrpj[i]['nm'])+'","dataFlags":1}&sid='+dsid)
			crtgrp=requests.post(daddr+'/wialon/ajax.html?svc=core/create_unit_group&params={"creatorId":'+str(daccid)+',"name":"'+str(sgrpj[i]['nm'])+'","dataFlags":1}&sid='+dsid)
			grpcrt=crtgrp.json()['item']['id']			#created units group ID
			print('Group created: ', sgrpj[i]['nm'])
			if len(sgrpj[i]['u'])!=0:
				gun=[]			#new units IDs in group
				for j in range(len(sgrpj[i]['u'])):
					if sunj_dict[sgrpj[i]['u'][j]] in dunj_dict:
						gun.append(dunj_dict[sunj_dict[sgrpj[i]['u'][j]]])
					else:
						print('Unit not found on destination account: ', sunj_dict[sgrpj[i]['u'][j]])
			updgrp=requests.post(daddr+'/wialon/ajax.html?svc=unit_group/update_units&params={"itemId":'+str(grpcrt)+',"units":'+str(gun)+'}&sid='+dsid)
			print('Group updated with units IDs: ', updgrp.json())			
		print('---------------------------------------------------------------------------------------------------------------------------------------------------')


################MAIN
if st==200:
	print("All fine!")
	crunits()
	ungrp()
	print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\nScript work completed!\n^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
else:	print("Error occured! Error code: ", st)
###########################################################

