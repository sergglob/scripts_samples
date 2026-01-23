#!/usr/bin/python3.6
#  icon, ACL, unit groups, agro, maintenance
#Developed by Novikov Sergey (nose)
print("This is a python script to test SDK API wialon requests")
addr=input("Enter the FROM URL, press enter default https://hst-api.wialon.com ")
if not addr:
	addr="https://hst-api.wialon.com"
else:
	addr=addr	
#tok=input("Enter the valid token: ")
#temp wialon hosting token
tok="a65c6e0b6745279bf440a7fb47281bf0E3CF7F550A3CB34DEB2B80D30AFCF9211BBD4FA3"

print("Sorce: ",addr, tok)
daddr=input("Enter the destination TO URL, press enter default https://local.wialontest.com ")
if not daddr:
	daddr="https://local.wialontest.com"
else:
	daddr=daddr	
#dtok=input("Enter the valid deestination token: ")
#temp wialon local token
dtok="0133933863ed12823b5b5a83ca646bd07D1930FFEAAB49D5A12A2B814DFDE8C6E8E31019"
print("Sorce: ",addr, tok)
print("Destination: ",daddr, dtok)
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
accid=data['user']['id']
daccid=ddata['user']['id']
nm=data['user']['nm']
dnm=ddata['user']['nm']
print("Source SID: ", sid, nm, accid)
print("Destination SID: ", dsid, dnm, daccid)
#
def menu():
	print("Select what you want to create:")
	print("1 - Units")
	print("2 - Drivers")
	print("3 - Passengers")
	print("0 - Quit")
	choise=input()
	sel(choise)	
#
def drv_menu():	
	print("Select what you want to create:")
	print("1 - Import from XLS/XLSX file")
	print("2 - Copy from the target account to destinated token's resource via SDK")
	print("0 - Quit")
	drchoice=input()
	drsel(drchoice)		
#
def sel(ch):
	if int(ch)==1:
		print("Looking for units in the account")
		crunits()
	elif int(ch)==2:
		print("Creating Drivers")
		drv_menu()
	elif int(ch)==3:
		print("Creating Passengers from XLS/XLSX")
		psxls()
	elif int(ch)==0:
		quit()
	else:
		print("Wrong input, back to the menu")
		menu()
#
def drsel(drchoice):	#drivers method selector
	if int(drchoice)==1:
		drxls()
	elif int(drchoice)==2:
		crdrivers()
	elif int(ch)==0:
		quit()
	else:
		print("Wrong input, back to the menu")
		menu()

###########################################################
def props(ex, unid, dhwid):
#	print(ex.json())
	exj=ex.json()	#dest unit props
	print('#################| updating properties UNIT:',exj['item']['nm'],' |#################')
	pr=requests.post(addr+'/wialon/ajax.html?svc=core/search_item&params={"id":"'+str(unid)+'","flags":4611686018427387903}&sid='+sid)
	prj=pr.json()	#init unit props
#	print(prj)
	rm_plus=prj["item"]["ph"] #remove + from phone number to replace it with %2B
	print("Importing general tab props")
	upd_gen=requests.post(daddr+'/wialon/ajax.html?svc=core/batch&params={"params":[{"svc":"unit/update_device_type","params":{"itemId":'+str(exj["item"]["id"])+',"deviceTypeId":"'+str(dhwid)+'","uniqueId":"'+str(prj["item"]["uid"])+'"}},{"svc":"unit/update_phone","params":{"itemId":'+str(exj["item"]["id"])+',"phoneNumber":"'+str("%2B"+rm_plus[1:])+'"}},{"svc":"unit/update_mileage_counter","params":{"itemId":'+str(exj["item"]["id"])+',"newValue":'+str(prj['item']['cnm'])+'}},{"svc":"unit/update_eh_counter","params":{"itemId":'+str(exj["item"]["id"])+',"newValue":'+str(prj['item']['cneh'])+'}},{"svc":"unit/update_traffic_counter","params":{"itemId":'+str(exj["item"]["id"])+',"newValue":'+str(prj['item']['cnkb'])+',"regReset":0}}],"flags":0}&sid='+dsid)	#update general props
	print(upd_gen.json())
#
	print("Importing custom fields")
	c=0	
	for key in prj['item']['flds']:
#		for c in range(len(prj['item']['flds'])):
		upd_cust=requests.post(daddr+'/wialon/ajax.html?svc=core/batch&params={"params":[{"svc":"item/update_custom_field","params":{"id":'+str(c)+',"n":"'+str(prj['item']['flds'][''+str(key)+'']['n'])+'","v":"'+str(prj['item']['flds'][''+str(key)+'']['v'])+'","itemId":'+str(exj["item"]["id"])+',"callMode":"create"}}],"flags":0}&sid='+dsid)		#update custom fields
		c+=1
		print(upd_cust.json())
#
	print("Importing admin fields")
	cc=0
	for ke in prj['item']['aflds']:
#		for cc in range(len(prj['item']['aflds'])):
		upd_adm=requests.post(daddr+'/wialon/ajax.html?svc=core/batch&params={"params":[{"svc":"item/update_admin_field","params":{"id":'+str(cc)+',"n":"'+str(prj['item']['aflds'][''+str(ke)+'']['n'])+'","v":"'+str(prj['item']['aflds'][''+str(ke)+'']['v'])+'","itemId":'+str(exj["item"]["id"])+',"callMode":"create"}}],"flags":0}&sid='+dsid)		#update admin fields
		print(upd_adm.json())		
#
	print("Importing commands")
	for s in prj['item']['cml']:
		upd_comm=requests.post(daddr+'/wialon/ajax.html?svc=core/batch&params={"params":[{"svc":"unit/update_command_definition","params":{"id":'+str(s)+',"n":"'+str(prj['item']['cml'][''+str(s)+'']['n'])+'","c":"'+str(prj['item']['cml'][''+str(s)+'']['c'])+'","l":"'+str(prj['item']['cml'][''+str(s)+'']['l'])+'","p":"'+str(prj['item']['cml'][''+str(s)+'']['p'])+'","a":'+str(prj['item']['cml'][''+str(s)+'']['a'])+',"f":"'+str(prj['item']['cml'][''+str(s)+'']['f'])+'","que_length":0,"itemId":'+str(exj["item"]["id"])+',"callMode":"create"}}],"flags":0}&sid='+dsid)	#update commands
		print(upd_comm.json())
#
	print("Importing trips detector tab")
	upd_trip=requests.post(daddr+'/wialon/ajax.html?svc=core/batch&params={"params":[{"svc":"unit/update_trip_detector","params":{"itemId":'+str(exj["item"]["id"])+',"type":'+str(prj['item']['rtd']['type'])+',"gpsCorrection":'+str(prj['item']['rtd']['gpsCorrection'])+',"minSat":'+str(prj['item']['rtd']['minSat'])+',"minMovingSpeed":'+str(prj['item']['rtd']['minMovingSpeed'])+',"minStayTime":'+str(prj['item']['rtd']['minStayTime'])+',"maxMessagesDistance":'+str(prj['item']['rtd']['maxMessagesDistance'])+',"minTripTime":'+str(prj['item']['rtd']['minTripTime'])+',"minTripDistance":'+str(prj['item']['rtd']['minTripDistance'])+'}}],"flags":0}&sid='+dsid)	#update trips detector
	print(upd_trip.json())
#
	print("Importing fuel consumption tab")
	upd_fuel=requests.post(daddr+'/wialon/ajax.html?svc=core/batch&params={"params":[{"svc":"unit/update_fuel_calc_types","params":{"itemId":'+str(exj["item"]["id"])+',"calcTypes":'+str(prj['item']['rfc']['calcTypes'])+'}},{"svc":"unit/update_fuel_impulse_params","params":{"itemId":'+str(exj["item"]["id"])+',"maxImpulses":'+str(prj['item']['rfc']['fuelConsImpulse']['maxImpulses'])+',"skipZero":'+str(prj['item']['rfc']['fuelConsImpulse']['skipZero'])+'}},{"svc":"unit/update_fuel_level_params","params":{"itemId":'+str(exj["item"]["id"])+',"flags":'+str(prj['item']['rfc']['fuelLevelParams']['flags'])+',"ignoreStayTimeout":'+str(prj['item']['rfc']['fuelLevelParams']['ignoreStayTimeout'])+',"minFillingVolume":'+str(prj['item']['rfc']['fuelLevelParams']['minFillingVolume'])+',"minTheftTimeout":'+str(prj['item']['rfc']['fuelLevelParams']['minTheftTimeout'])+',"minTheftVolume":'+str(prj['item']['rfc']['fuelLevelParams']['minTheftVolume'])+',"filterQuality":'+str(prj['item']['rfc']['fuelLevelParams']['filterQuality'])+',"fillingsJoinInterval":'+str(prj['item']['rfc']['fuelLevelParams']['fillingsJoinInterval'])+',"theftsJoinInterval":'+str(prj['item']['rfc']['fuelLevelParams']['theftsJoinInterval'])+',"extraFillingTimeout":'+str(prj['item']['rfc']['fuelLevelParams']['extraFillingTimeout'])+'}}],"flags":0}&sid='+dsid)	#update fuel consumption
	print(upd_fuel.json())
#
	print("Importing characteristics")
	for fl in prj['item']['pflds']:
		upd_char=requests.post(daddr+'/wialon/ajax.html?svc=core/batch&params={"params":[{"svc":"item/update_profile_field","params":{"itemId":'+str(exj["item"]["id"])+',"n":"'+str(prj['item']['pflds'][''+fl+'']['n'])+'","v":"'+str(prj['item']['pflds'][''+fl+'']['v'])+'"}}],"flags":0}&sid='+dsid)	#update characteristics
		print(upd_char.json())
#
	print("Importing sensors")
	for se in prj['item']['sens']:
		upd_sens=requests.post(daddr+'/wialon/ajax.html?svc=core/batch&params={"params":[{"svc":"unit/update_sensor","params":{"n":"'+str(prj['item']['sens'][''+str(se)+'']['n'])+'","t":"'+str(prj['item']['sens'][''+str(se)+'']['t'])+'","d":"'+str(prj['item']['sens'][''+str(se)+'']['d'])+'","m":"'+str(prj['item']['sens'][''+str(se)+'']['m'])+'","p":"'+str(prj['item']['sens'][''+str(se)+'']['p']).replace('+','%2B').replace('#','%23').replace('^','%5E').replace('\\','%2F').replace(':','%3A')+'","f":'+str(prj['item']['sens'][''+str(se)+'']['f'])+',"c":"'+str(prj['item']['sens'][''+str(se)+'']['c'].replace('"','\\"'))+'","vt":'+str(prj['item']['sens'][''+str(se)+'']['vt'])+',"vs":'+str(prj['item']['sens'][''+str(se)+'']['vs'])+',"tbl":'+str(prj['item']['sens'][''+str(se)+'']['tbl']).replace(' ','').replace("'", '"')+',"id":'+str(prj['item']['sens'][''+str(se)+'']['id'])+',"itemId":'+str(exj["item"]["id"])+',"callMode":"create"}}],"flags":0}&sid='+dsid)	#create sensors
		print(upd_sens.json())	
#
	print("Importing eco")
	ec=requests.post(addr+'/wialon/ajax.html?svc=unit/get_drive_rank_settings&params={"itemId":'+str(unid)+'}&sid='+sid)
	ecj=ec.json()
	if 'global' in ecj:
		upd_eco=requests.post(daddr+'/wialon/ajax.html?svc=core/batch&params={"params":[{"svc":"unit/update_drive_rank_settings","params":{"itemId":'+str(exj["item"]["id"])+',"driveRank":'+str(ecj).replace(' ','').replace("'", '"')[0:-1]+',"global":{"accel_mode":"'+str(ecj['global']['accel_mode'])+'"}}}}],"flags":0}&sid='+dsid)	#create eco criterias
	else:
		print("----------!!!!ECO SETINGS IMPORT FAILURE!!!!----------")
		
#		
	print("Importing advance tab settings")
	adv=requests.post(addr+'/wialon/ajax.html?svc=core/batch&params={"params":[{"svc":"unit/get_activity_settings","params":{"itemId":'+str(unid)+'}},{"svc":"unit/get_report_settings","params":{"itemId":'+str(unid)+'}},{"svc":"unit/get_messages_filter","params":{"itemId":'+str(unid)+'}}],"flags":0}&sid='+sid)
	advj=adv.json()
#	print(advj)
	upd_adv=requests.post(daddr+'/wialon/ajax.html?svc=core/batch&params={"params":[{"svc":"unit/update_activity_settings","params":{"itemId":'+str(exj["item"]["id"])+',"type":'+str(advj[0]["type"])+'}},{"svc":"unit/update_report_settings","params":{"itemId":'+str(exj["item"]["id"])+',"params":{"maxMessagesInterval":'+str(advj[1]["maxMessagesInterval"])+',"fuelRateCoefficient":'+str(advj[1]["fuelRateCoefficient"])+',"dailyEngineHoursRate":'+str(advj[1]["dailyEngineHoursRate"])+',"urbanMaxSpeed":'+str(advj[1]["urbanMaxSpeed"])+',"mileageCoefficient":'+str(advj[1]["mileageCoefficient"])+',"speedingMode":'+str(advj[1]["speedingMode"])+',"speedingTolerance":'+str(advj[1]["speedingTolerance"])+',"speedingMinDuration":'+str(advj[1]["speedingMinDuration"])+'}}},{"svc":"unit/update_messages_filter","params":{"itemId":'+str(exj["item"]["id"])+',"enabled":'+str(advj[2]["enabled"])+',"skipInvalid":'+str(advj[2]["skipInvalid"])+',"minSats":'+str(advj[2]["minSats"])+',"maxHdop":'+str(advj[2]["maxHdop"])+',"maxSpeed":'+str(advj[2]["maxSpeed"])+',"lbsCorrection":'+str(advj[2]["lbsCorrection"])+'}}],"flags":0}&sid='+dsid)	# updating activity type, reports constants, sats filtration level
	seas=requests.post(addr+'/wialon/ajax.html?svc=unit/get_fuel_settings&params={"itemId":'+str(unid)+'}&sid='+sid)
	seasj=seas.json()
#	print(seasj)
	upd_seas=requests.post(daddr+'/wialon/ajax.html?svc=core/batch&params={"params":[{"svc":"unit/update_fuel_rates_params","params":{"itemId":'+str(exj["item"]["id"])+',"idlingSummer":0,"idlingWinter":0,"consSummer":'+str(seasj['fuelConsRates']['consSummer'])+',"consWinter":'+str(seasj['fuelConsRates']['consWinter'])+',"winterMonthFrom":'+str(seasj['fuelConsRates']['winterMonthFrom'])+',"winterDayFrom":'+str(seasj['fuelConsRates']['winterDayFrom'])+',"winterMonthTo":'+str(seasj['fuelConsRates']['winterMonthTo'])+',"winterDayTo":'+str(seasj['fuelConsRates']['winterDayTo'])+'}}],"flags":0}&sid='+dsid)	#updating season fuel settings
	for kz in prj['item']['prp']:
		upd_colors=requests.post(daddr+'/wialon/ajax.html?svc=item/update_custom_property&params={"itemId":'+str(exj["item"]["id"])+',"name":"'+str(kz)+'","value":"'+str(prj['item']['prp'][''+str(kz)+''])+'"}&sid='+dsid)	#update colors
	print('#################')

###########################################################
def crunits():
#getting units list
	u=requests.post(addr+'/wialon/ajax.html?svc=core/search_items&params={"spec":{"itemsType":"avl_unit","propName":"","propValueMask":"*","sortType":"","propType":""},"force":1,"flags":4611686018427387903,"from":0,"to":0}&sid='+sid)
	units=u.json()
#getting hw types
#	print(addr+'/wialon/ajax.html?svc=core/get_hw_types&params={"filterType":"name","filterValue":id,"includeType":1,"ignoreRename":1}&sid='+sid)
	hw_r=requests.post(addr+'/wialon/ajax.html?svc=core/get_hw_types&params={"filterType":"name","filterValue":"id","includeType":1,"ignoreRename":1}&sid='+sid)
	dhw_r=requests.post(daddr+'/wialon/ajax.html?svc=core/get_hw_types&params={"filterType":"name","filterValue":"id","includeType":1,"ignoreRename":1}&sid='+dsid)
	hw=hw_r.json()	#list of source hardware
	dhw=dhw_r.json() #list of destination hardware
	for i in range(len(units['items'])):
		if 'hw' in units['items'][i]:
			print("Unit name: ",units['items'][i]['nm']," Unit HW ID: ",units['items'][i]['hw']," Unit creator ID: ",units['items'][i]['crt'])
			unid=units['items'][i]['id']
			print(unid)
			for k in range(len(hw)):
				if units['items'][i]['hw']==hw[k]['id']:
					hwname=hw[k]['name']
#					print(hwname)
					for j in range(len(dhw)):
						if hwname==dhw[j]['name']:
							dhwid=dhw[j]['id']	#the hw id on destination server
#			
			us_r=requests.post(addr+'/wialon/ajax.html?svc=core/search_item&params={"id":"'+str(units['items'][i]['crt'])+'","flags":1}&sid='+sid) #search creator user by ID
#			print(addr+'/wialon/ajax.html?svc=core/search_item&params={"id":"'+str(units['items'][i]['crt'])+'","flags":1}&sid='+sid)
			us=us_r.json() #list of source users
			search_dus=requests.post(daddr+'/wialon/ajax.html?svc=core/search_items&params={"spec":{"itemsType":"user","propName":"sys_name","propValueMask":"*","sortType":"sys_name","or_logic":0},"force":1,"flags":1,"from":0,"to":0}&sid='+dsid)	#searching users on destination server
			search=search_dus.json()
			if units['items'][i]['crt']==data['user']['id']:
				uname=data['user']['nm']
				if uname==ddata['user']['nm']:
					dcrt=ddata['user']['id']	#Destination creator ID
					print("Set the main creator: ",dcrt)
					ex=requests.post(daddr+'/wialon/ajax.html?svc=core/create_unit&params={"creatorId":"'+str(dcrt)+'","name":"'+str(units['items'][i]['nm'])+'","hwTypeId":"'+str(dhwid)+'","dataFlags":1}&sid='+dsid)
					props(ex, unid, dhwid)
				else:
					for g in range(len(search['items'])):
						if uname==search['items'][g]['nm']:
							dcrt=search['items'][g]['id']
							print("The destination user found: ", dcrt)
							ex=requests.post(daddr+'/wialon/ajax.html?svc=core/create_unit&params={"creatorId":"'+str(dcrt)+'","name":"'+str(units['items'][i]['nm'])+'","hwTypeId":"'+str(dhwid)+'","dataFlags":1}&sid='+dsid)
							props(ex, unid, dhwid)
#						

						else:
							dcrt=ddata['user']['id']
							print("The destination user NOT found. Applying the creator as a main destination user", dcrt)	
							ex=requests.post(daddr+'/wialon/ajax.html?svc=core/create_unit&params={"creatorId":"'+str(dcrt)+'","name":"'+str(units['items'][i]['nm'])+'","hwTypeId":"'+str(dhwid)+'","dataFlags":1}&sid='+dsid)
							props(ex, unid, dhwid)
			else:					
#		elif units['items'][i]['crt']!=data['user']['id']:
				if 'error' in us:
					dcrt=ddata['user']['id']
					print("The creator not found. Applying the creator as a main destination user", dcrt)
					ex=requests.post(daddr+'/wialon/ajax.html?svc=core/create_unit&params={"creatorId":"'+str(dcrt)+'","name":"'+str(units['items'][i]['nm'])+'","hwTypeId":"'+str(dhwid)+'","dataFlags":1}&sid='+dsid)
					props(ex, unid, dhwid)
				else:
					for h in range(len(search['items'])):
						if us['item']['nm']==search['items'][h]['nm']:						
							dcrt=search['items'][h]['id']
							print("The destination user found: ", dcrt)
							ex=requests.post(daddr+'/wialon/ajax.html?svc=core/create_unit&params={"creatorId":"'+str(dcrt)+'","name":"'+str(units['items'][i]['nm'])+'","hwTypeId":"'+str(dhwid)+'","dataFlags":1}&sid='+dsid)
							props(ex, unid, dhwid)
		else:
			print("--------------!!!!NOT ENOUGH ACCESS TO: ", units['items'][i]['nm'])
			continue
###########################################################

def crdrivers():	#creating the drivers from account source via SDK
	#getting drivers list
	dr=requests.post(addr+'/wialon/ajax.html?svc=core/search_items&params={"spec":{"itemsType":"avl_resource","propName":"drivers","propValueMask":"*","sortType":"","propType":""},"force":1,"flags":256,"from":0,"to":0}&sid='+sid)
	drivers=dr.json()
	for drv in drivers['items'][0]['drvrs']:
		driv=drivers['items'][0]['drvrs'][''+str(drv)+'']
		cdr=requests.post(daddr+'/wialon/ajax.html?svc=resource/update_driver&params={"c":"'+str(driv['c'])+'","ck":'+str(driv['ck'])+',"ds":"'+str(driv['ds'])+'","id":"'+str(driv['id'])+'","n":"'+str(driv['n'])+'","p":"'+str(driv['p'].replace('+','%2B'))+'","r":'+str(driv['r'])+',"f":'+str(driv['f'])+',"pwd":"'+str(driv['pwd'])+'","jp":'+str(driv['jp']).replace("'", '"')[0:-1]+'},"itemId":'+str(daccid+1)+''+',"callMode":"create"}&sid='+dsid)
		print(cdr.json())
	print("Task completed. Returning to the menu.")
	menu()

#
def drxls():	#creating drivers from XLS
	print("XLRD library required!")
	print("The XLS/XLSX data columns string: Driver name|Driver code(optional)|Description(optional)|Phone number(optional)|Mobile code(optional)")	
	print("The XLS/XLSX file should containe only 1 sheet")
	import xlrd
	drtok=input("Enter the deestination Drivers account  token, or press enter if it is the same as the main token: ")
	if not drtok:
		drtok=dtok
	#temp wialon local token
#	drtok="0133933863ed12823b5b5a83ca646bd07D1930FFEAAB49D5A12A2B814DFDE8C6E8E31019"
	drresp=requests.get(daddr+'/wialon/ajax.html?svc=token/login&params={"token":"'+drtok+'"}')
	drdata=drresp.json()
	drsid=drdata['eid']
	drfile=input("Enter the path to the file or file name, if it in the same directory as the script: ")
#	print(drfile)
	wb=xlrd.open_workbook(drfile)
	sheet=wb.sheet_by_index(0)
	drvals = [sheet.row_values(rownum) for rownum in range(sheet.nrows)]
#	print(drvals)
	for drkey in range(len(drvals)):
		print("Creating driver: ", drvals[drkey][0])
		cdrxls=requests.post(daddr+'/wialon/ajax.html?svc=resource/update_driver&params={"c":"'+str(drvals[drkey][1]).replace(".0", "")+'","ck":0,"ds":"'+str(drvals[drkey][2])+'","id":0,"n":"'+str(drvals[drkey][0])+'","p":"'+str(drvals[drkey][3].replace('+','%2B'))+'","r":0,"f":0,"pwd":"'+str(drvals[drkey][4]).replace(".0", "")+'","jp":{},"itemId":'+str(daccid+1)+''+',"callMode":"create"}&sid='+drsid)
		print(cdrxls.json())
	print("Task completed. Returning to the menu.")
	menu()
	
#
def psxls():	#creating passengers from XLS
	print("XLRD library required!")
	print("The XLS/XLSX data columns string: Passenger name|Passenger code(optional)|Custom field col1(optional)|Custom field col2(optional)|Automatic unbinding hours (specify)")	
	print("The XLS/XLSX file should containe only 1 sheet")
	import xlrd
	pstok=input("Enter the deestination Passengers' account  token, or press enter if it is the same as the main token: ")
	if not pstok:
		pstok=dtok
	#temp wialon local token
#	pstok="0133933863ed12823b5b5a83ca646bd07D1930FFEAAB49D5A12A2B814DFDE8C6E8E31019"
	psresp=requests.get(daddr+'/wialon/ajax.html?svc=token/login&params={"token":"'+pstok+'"}')
	psdata=psresp.json()
	pssid=psdata['eid']
	psfile=input("Enter the path to the file or file name, if it in the same directory as the script: ")
#	print(drfile)
	wb=xlrd.open_workbook(psfile)
	sheet=wb.sheet_by_index(0)
	psvals = [sheet.row_values(rownum) for rownum in range(sheet.nrows)]
	art=input("Specify the automatic unbinding mask in hours: ")
	arts=int(art)*3600
#	print(drvals)
	for pskey in range(len(psvals)):
		print("Creating passenger: ", psvals[pskey][0])
		cpsxls=requests.post(daddr+'/wialon/ajax.html?svc=resource/update_tag&params={"c":"'+str(psvals[pskey][1]).replace(".0", "").replace(" ","")+'","art":'+str(arts).replace(".0", "")+',"ck":0,"id":0,"n":"'+str(psvals[pskey][0])+'","r":0,"jp":{"'+str(psvals[pskey][2])+'":"'+str(psvals[pskey][3])+'"},"itemId":'+str(daccid+1)+',"callMode":"create"}&sid='+pssid)
		print(cpsxls.json())
	print("Task completed. Returning to the menu.")
	menu()
#main
while st==200:
	print("All fine!")
	menu()
else:	print("Error occured! Error code: ", st)
###########################################################

