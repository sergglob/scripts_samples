#!/usr/bin/python3.6
import requests
import json
#NOT USE TOP SERVICE ACCOUNT TOKEN FOR UNITS CREATION, creation under TOP restricterd!!!!
# wr, ii, i, h, w, c, cc, p, l, t, cu, se, s, 
#default AUTO mileage, engine hours counter
#default fuel filling/theft timeout 300 sec, theft volume timeout 0 sec
#NO consumption math
#NO calculation table for sensors work, need to think
print("Script from PRO to HOSTING/LOCAL")
nv="-348201.3876"	#not valid infinity bounds for the calculation table
paddr=input("Enter PRO address with http/https prefix: ")
#paddr="http://localhost:8026"	#temp
plog=input("Enter PRO MAIN USER login: ")
#plog="nose"	#temp
ppas=input("Enter PRO password: ")
#ppas=""	#temp
laddr=input("Enter LOCAL/HOSTING address with http/https prefix: ")
#laddr="https://hst-api.wialon.com"	#temp
llog=input("Enter LOCAL/HOSTING token: ")
#llog="a65c6e0b6745279bf440a7fb47281bf0C5059D1942C8FF19A56E48F7C9BDD88712F3BC51"	#temp
pl=requests.post(paddr+'/ajax.html?svc=core/login&params={"user":"'+str(plog)+'","password":"'+str(ppas)+'"}')
plj=pl.json()
psid=plj['ssid']	#DEFAULT PRO sid
pcrtn=plj['user']['nm']	#DEFAULT PRO main user name
pcrti=plj['uid']	#DEFAULT PRO main user ID
ll=requests.post(laddr+'/wialon/ajax.html?svc=token/login&params={"token":"'+str(llog)+'"}')
llj=ll.json()
lsid=llj['eid']	#LOCAL/HOSTING sid
lcrtn=llj['user']['nm']	#DEFAULT local/hosting main user name
lcrti=llj['user']['id']	#DEFAULT local/hosting main user ID
phw=requests.post(paddr+'/ajax.html?svc=core/get_hw_types&params={}&ssid='+psid)
phwj=phw.json()	#hw list on pro
lhw=requests.post(laddr+'/wialon/ajax.html?svc=core/get_hw_types&params={"filterType":"name","filterValue":"id","includeType":1,"ignoreRename":1}&sid='+lsid)
lhwj=lhw.json()	#hw list on local/hosting
for wr in range(len(lhwj)):
	if lhwj[wr]['name']=='Wialon Retranslator':
		hwtype=lhwj[wr]['id']	#searching and setting Wialon Retranslator DEFAULT hardware type ID
pun=requests.post(paddr+'/ajax.html?svc=core/search_items&params={"spec":{"itemsType":"avl_unit","propName":"sys_name","propValueMask":"*","sortType":"sys_name"},"force":1,"flags":0x00000105,"from":0,"to":0xffffffff})&ssid='+psid)	
punjj=pun.json()
punj=punjj['items']	#list of PRO units
pus=requests.post(paddr+'/ajax.html?svc=core/search_items&params={"spec":{"itemsType":"user","propName":"sys_name","propValueMask":"*","sortType":"sys_name"},"force":1,"flags":0x00000001,"from":0,"to":0xffffffff})&ssid='+psid)
pusjj=pus.json()	
pusj=pusjj['items']	#list of PRO users
lus=requests.post(laddr+'/wialon/ajax.html?svc=core/search_items&params={"spec":{"itemsType":"user","propName":"sys_name","propValueMask":"*","sortType":"sys_name"},"force":1,"flags":1,"from":0,"to":0})&sid='+lsid)
lusjj=lus.json()
lusj=lusjj['items']	#list of local/hosting users


###############################################################################################
#units
def create():
	for ii in range(len(punj)):
		ucreate(ii)
		print("##########")
		#
		#

#
def props(p,l,t):
	print("Importing unit properties")
	punit=requests.post(paddr+'/ajax.html?svc=core/search_item&params={"itemId":'+str(p)+',"flags":0xFFFFFFFF}&ssid='+psid)
	punitj=punit.json()
	gen=punitj	#general tab
	pup=punitj['pup']	#advanced tab
	sens=punitj['sens']	#sensors tab
	cml=punitj['cml']	#commands tab
	flds=punitj['flds']	#custom fields
	ptrip=requests.post(paddr+'/ajax.html?svc=unit/get_trip_detector&params={"itemId":'+str(p)+'}&ssid='+psid)
	ptripj=ptrip.json()
	trip=ptripj['trip_detection']	#trips detector tab
	pfuel=requests.post(paddr+'/ajax.html?svc=unit/get_fuel_settings&params={"itemId":'+str(p)+'}&ssid='+psid)
	fuel=pfuel.json()	#fuel consumption tab
	pfilt=requests.post(paddr+'/ajax.html?svc=unit/get_messages_filter&params={"itemId":'+str(p)+'}&ssid='+psid)
	filt=pfilt.json()	#messages filtration tab
	print("Updating general tab")
	upd_gen=requests.post(laddr+'/wialon/ajax.html?svc=core/batch&params={"params":[{"svc":"unit/update_device_type","params":{"itemId":'+str(l)+',"deviceTypeId":"'+str(t)+'","uniqueId":"'+str(gen["uid"])+'"}},{"svc":"unit/update_phone","params":{"itemId":'+str(l)+',"phoneNumber":"'+str(gen['ph']).replace("+","%2B")+'"}},{"svc":"unit/update_mileage_counter","params":{"itemId":'+str(l)+',"newValue":'+str(int(gen['cnm']/1000))+'}},{"svc":"unit/update_eh_counter","params":{"itemId":'+str(l)+',"newValue":'+str(gen['cneh']/3600)+'}},{"svc":"unit/update_calc_flags","params":{"itemId":'+str(l)+',"newValue":768}},{"svc":"unit/update_report_settings","params":{"itemId":'+str(l)+',"params":{"speedingMode":0,"speedLimit":'+str(pup["msl"])+',"speedingMinDuration":1}}}],"flags":0}&sid='+lsid)	
	print(upd_gen.json())
	print("Updating Advanced tab with GPS filtration")
	upd_adv=requests.post(laddr+'/wialon/ajax.html?svc=core/batch&params={"params":[{"svc":"unit/update_report_settings","params":{"itemId":'+str(l)+',"params":{"maxMessagesInterval":'+str(pup["mmi"])+',"dailyEngineHoursRate":'+str(pup["dehr"])+',"urbanMaxSpeed":'+str(pup["mus"])+',"mileageCoefficient":'+str(pup["mcoef"])+'}}},{"svc":"unit/update_messages_filter","params":{"itemId":'+str(l)+',"enabled":'+str(filt["enabled"])+',"skipInvalid":'+str(filt["skipInvalid"])+',"minSats":'+str(filt["minSats"])+',"maxHdop":'+str(filt["maxHdop"])+',"maxSpeed":'+str(filt["maxSpeed"])+'}}],"flags":0}&sid='+lsid)
	print(upd_adv.json())
	print("Updating custom fields")
	for cu in range(len(flds)):
		upd_cust=requests.post(laddr+'/wialon/ajax.html?svc=core/batch&params={"params":[{"svc":"item/update_custom_field","params":{"id":'+str(cu)+',"n":"'+str(flds[''+str(cu+1)+'']['nm'])+'","v":"'+str(flds[''+str(cu+1)+'']['vl'])+'","itemId":'+str(l)+',"callMode":"create"}}],"flags":0}&sid='+lsid)
		print(upd_cust.json())
	print("Updating Trips detector")
	upd_trip=requests.post(laddr+'/wialon/ajax.html?svc=core/batch&params={"params":[{"svc":"unit/update_trip_detector","params":{"itemId":'+str(l)+',"type":'+str(trip['type'])+',"gpsCorrection":'+str(trip['has_gps_correction'])+',"minSat":'+str(trip['min_sat'])+',"minMovingSpeed":'+str(trip['min_moving_speed'])+',"minStayTime":'+str(trip['min_stay_time'])+',"maxMessagesDistance":'+str(trip['max_msgs_distance'])+',"minTripTime":'+str(trip['min_trip_time'])+',"minTripDistance":'+str(trip['min_trip_distance'])+'}}],"flags":0}&sid='+lsid)	
	print(upd_trip.json())
	print("Updating fuel consumption")
	upd_fuel=requests.post(laddr+'/wialon/ajax.html?svc=core/batch&params={"params":[{"svc":"unit/update_fuel_calc_types","params":{"itemId":'+str(l)+',"calcTypes":'+str(fuel[0])+'}},{"svc":"unit/update_fuel_impulse_params","params":{"itemId":'+str(l)+',"maxImpulses":'+str(fuel[4]['max_impulses'])+',"skipZero":'+str(fuel[4]['skip_zero'])+'}},{"svc":"unit/update_fuel_level_params","params":{"itemId":'+str(l)+',"flags":'+str(fuel[1]['fl'])+',"ignoreStayTimeout":'+str(fuel[1]['fms'])+',"minFillingVolume":'+str(fuel[1]['fmv'])+',"minTheftTimeout":'+str(fuel[1]['tms'])+',"minTheftVolume":'+str(fuel[1]['tmv'])+',"filterQuality":'+str(fuel[1]['fq'])+',"fillingsJoinInterval":300,"theftsJoinInterval":300,"extraFillingTimeout":0}}],"flags":0}&sid='+lsid)	
	print(upd_fuel.json())
	print("Updating season consumption")
	upd_seas=requests.post(laddr+'/wialon/ajax.html?svc=core/batch&params={"params":[{"svc":"unit/update_fuel_rates_params","params":{"itemId":'+str(l)+',"idlingSummer":0,"idlingWinter":0,"consSummer":'+str(fuel[3]['summer_consumption'])+',"consWinter":'+str(fuel[3]['winter_consumption'])+',"winterMonthFrom":'+str(fuel[3]['winter_month_from'])+',"winterDayFrom":'+str(fuel[3]['winter_day_from'])+',"winterMonthTo":'+str(fuel[3]['winter_month_to'])+',"winterDayTo":'+str(fuel[3]['winter_day_to'])+'}}],"flags":0}&sid='+lsid)
	print(upd_seas.json())
	print("Creating sensors")
	for se in sens:
		print("Sensors - ", se)
		st=sens[se]['tbl']	#calculation table data
		table=[]
		x1,x2,x3="","",""
		if len(st)!=0:
			for tt in range(len(st)):
				if str(st[tt][2])!=nv:
					x1=st[tt][0]
					x2=st[tt][1]
					x3=st[tt][2]
					calctable={"x":x1,"a":x2,"b":x3}
					table.append(calctable)
				else: continue
			if nv==str(st[0][2]):
				minn=st[0][0]
			else: minn=""
			if nv==str(st[-1:][0][2]):
				maxx=st[-1:][0]
			else: maxx=""
			ccc={'appear_in_popup':'true','show_time':'false','pos':2,'cm':0,'mu':0,'act':0,'uct':0,'timeout':0,'ci':'{}','consumption':0,'lower_bound':str(minn),'upper_bound':str(maxx[0])}	
		else: ccc={'appear_in_popup':'true','show_time':'false','pos':2,'cm':0,'mu':0,'act':0,'uct':0,'timeout':0,'ci':'{}'}	
		upd_sens=requests.post(laddr+'/wialon/ajax.html?svc=core/batch&params={"params":[{"svc":"unit/update_sensor","params":{"n":"'+str(sens[''+str(se)+'']['nm'])+'","t":"'+str(sens[''+str(se)+'']['tp'])+'","d":"'+str(sens[''+str(se)+'']['de'])+'","m":"'+str(sens[''+str(se)+'']['me'])+'","p":"'+str(sens[''+str(se)+'']['pn']).replace('+','%2B').replace('#','%23').replace('^','%5E').replace('\\','%2F').replace(':','%3A')+'","f":'+str(sens[''+str(se)+'']['fl'])+',"c":"'+str(ccc).replace(' ','').replace("'", '\\"')+'","vt":'+str(sens[''+str(se)+'']['vt'])+',"vs":'+str(sens[''+str(se)+'']['vs'])+',"tbl":'+str(table).replace(' ','').replace("'", '"')+',"id":0,"itemId":'+str(l)+',"callMode":"create"}}],"flags":0}&sid='+lsid)
		print(upd_sens.json())	
	print("Creating commands")
	for s in cml:
		upd_comm=requests.post(laddr+'/wialon/ajax.html?svc=core/batch&params={"params":[{"svc":"unit/update_command_definition","params":{"id":'+str(s)+',"n":"'+str(cml[''+str(s)+'']['nm'])+'","c":"'+str(cml[''+str(s)+'']['cn'])+'","l":"'+str(cml[''+str(s)+'']['lt'])+'","p":"'+str(cml[''+str(s)+'']['cp'])+'","a":1,"f":"0","que_length":0,"itemId":'+str(l)+',"callMode":"create"}}],"flags":0}&sid='+lsid)	
		print(upd_comm.json())
	print("-----Unit props updated-----")
#
def ucreate(i):
	for h in range(len(phwj)):
		if punj[i]['hw']==phwj[h]['id']:
				for w in range(len(lhwj)):
					if phwj[h]['name']==lhwj[w]['name']:
						hwt=lhwj[w]['id']
						hwn=lhwj[w]['name']
		else:
			hwt=hwtype
	cname=pcrtn
	for c in range(len(pusj)):
		if punj[i]['crt']==pusj[c]['id']:
			cname=pusj[c]['nm']	#searching the unit's creator name
		else:
			continue
	crtn=lcrtn	#setting the default creator's name for the unit
	crti=lcrti	#setting the default creator's ID for the unit
	for cc in range(len(lusj)):
		if cname==lusj[cc]['nm']:
			crtn=lusj[cc]['nm']	#setting the new creator's name for the unit
			crti=lusj[cc]['id']	#setting the new creator's ID for the unit
		else: 	
			continue
						
	print("Creating unit name: ",punj[i]['nm'],", hw type: ",hwn,", creator original: ",pcrti, ", creator new: ",crti)
	uncr=requests.post(laddr+'/wialon/ajax.html?svc=core/create_unit&params={"creatorId":'+str(crti)+',"name":"'+str(punj[i]['nm'])+'","hwTypeId":'+str(hwt)+',"dataFlags":1}&sid='+lsid)
	uncrj=uncr.json()
	props(punj[i]['id'],uncrj['item']['id'], hwt)	#fuction props for the unit
#{'item': {'nm': 'PROunit', 'cls': 2, 'id': 20646382, 'mu': 0, 'uacl': 880333094911}, 'flags': 1}
	

###############################################################################################
create()
