#!/usr/bin/python3.6
import requests
import json
print("This script only for Hosting retranslators units search")
sid=input("Enter the valid SID: ")
def rsear():
	uid=input("Enter the unit ID to search: ")
	sear=requests.post('https://hst-api.wialon.com/wialon/ajax.html?svc=core/search_items&params={"spec":{"itemsType":"avl_retranslator","propName":"retranslator_units","propValueMask":"*","sortType":"retranslator_units","propType":"propitemname"},"force":1,"flags":513,"from":0,"to":0}&sid='+sid)	#retranslators with units full data
	sj=sear.json()
	hw=requests.post('https://hst-api.wialon.com/wialon/ajax.html?svc=core/get_hw_types&params={"filterType":"name","filterValue":"name","includeType":1,"ignoreRename":1}&sid='+sid)	#hardware types
	hwj=hw.json()
	oun=requests.post('https://hst-api.wialon.com/wialon/ajax.html?svc=core/search_items&params={"spec":{"itemsType":"avl_unit","propName":"sys_name","propValueMask":"*","sortType":"sys_name","propType":"propitemname"},"force":1,"flags":257,"from":0,"to":0}&sid='+sid)	#search units 
	ounj=oun.json()
	ouid,nouid=str(0),str(0)
	for a in range(len(ounj['items'])):
		if uid==ounj['items'][a]['uid']:
			ouid=ounj['items'][a]['id']	#original unit API uid
			nouid=ounj['items'][a]['nm']
		else:
			continue
	for i in range(len(sj['items'])):	#search the presense of the unit ID in the retranslators
		for j in range(len(sj['items'][i]['rtru'])):
			if ouid==sj['items'][i]['rtru'][j]['i']:
				print("Original unit used with ID change. Retanslator name: ", sj['items'][i]['nm'])
				print(" | ",nouid," | ",sj['items'][i]['rtru'][j]['a']," | ")
				print("********************************************************************")
			elif uid==sj['items'][i]['rtru'][j]['a']:
				print("Retanslator name: ", sj['items'][i]['nm'])
				un=requests.post('https://hst-api.wialon.com/wialon/ajax.html?svc=core/search_item&params={"id":'+str(sj['items'][i]['rtru'][j]['i'])+',"flags":257}&sid='+sid)
				unj=un.json()
				unhw=unj['item']['hw']
				for k in range(len(hwj)):
					if unhw==hwj[k]['id']:
						hwname=hwj[k]['name']
					else:
						continue
#				print("| Original unit | name | original UID | HW type |")
				print(" | ",unj['item']['nm']," | ",unj['item']['uid']," | ",hwname)
				print("--------------------------------------------------------------------")				
			else:
				continue
	print('##############################################################################################')

while True:
	rsear()
