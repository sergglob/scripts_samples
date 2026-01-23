#!/bin/python3
#pip3 install BeautifulSoup4, xlrd, defusedxml
#The '.' not allowed in the passengers code. If the code 1234.0, the system will split and take code 1234
#
#version release 06 Jun 2022

import xlrd
sfl=input("Enter the source file name XLS: ")			#source XLSX file from the command line
#sfl='drivers_EN.xls'
ofl=sfl.split('.')[0]+'.wlp'							#rename file name XLS to output WLP file

#
ch=input('Select what to create:\n1 - Drivers\nThe expexted columns order: | Name | Code | Description | Phone number | Mobile key | Exclusive (0 or 1) | Custom field name | Custom field value | ... |\n\n2 - Trailers\nThe expexted columns order: | Name | Code | Description | Exclusive (0 or 1) | Custom field name | Custom field value | ... |\n\n3 - Passengers\nThe expexted columns order: | Name | Code | Time | Custom field name | Custom field value | ... |\n---------------------------------------------------------------------------------------------------------------------------------------------------------\n')	#program selector Drivers, Trailers, Passengers

#main prog to select the function
def main(a,b,c):
	if a=="1":
		drivers(b,c)
	elif a=="2":
		trailers(b,c)
	elif a=="3":
		passengers(b,c)
	else:
		print('Wrong choice - ', a, ". Try again\n", main(a,b,c))

###################################################################-PASSENGERS-######################################################################################
def passengers(inpf, outpf):
	print ('Trying to create the Passengers file', outpf, '\n')
	tfile=open(outpf, 'w')
	head='{"type":"avl_resource","version":"b4","mu":0,"tags":'
	tail='}'
	ps=[]												#passengers data array
	wb=xlrd.open_workbook(inpf)
	sheet=wb.sheet_by_index(0)
	un = [sheet.row_values(rownum) for rownum in range(1,sheet.nrows)]
	for i in range(len(un)):							#cycle xls file
		p={}
		name=str(un[i][0]).replace('.0','')				#passenger name
		code=str(un[i][1]).split('.')[0]				#passenger code
		tm=str(un[i][2]*3600)							#passenger autounbind time
		jp={}
		cust=list(un[i][3:])
		if len(cust)%2!=0:
			cust.append('')
		j=len(cust)
		while j>0:
			if len(cust[0])==0:
				cust=cust[2:]
				j-=2
			else:
				jp[cust[0]]=str(cust[1]).replace('.0','')	#custom field name:custom field value
				cust=cust[2:]
				j-=2
		jpf=str(jp)										#formatted custom fields 
		p={"n":str(name),"c":str(code),"art":str(tm).split('.')[0],"jp":jpf}			#main parameters dictionary: Name, code, time
		ps.append(p)
	output=head+str(ps).replace("'",'"')+tail											#form the result string, but there is an issue with key "jp". It will have the quoters like "jp":'{data}'. Solved below.
	print(output.replace('"{','{').replace('}"','}').replace('O"',"O'").replace("O',",'O",').replace('L"E',"L'E").replace("NULL',",'NULL",').replace("NULL'}",'NULL"}'),file=tfile) 	#	, L'Estrange, but allow "NULL"
	print (outpf, ' created!')

###################################################################-DRIVERS-######################################################################################
def drivers(inpf, outpf):
	print ('Trying to create the Drivers file', outpf, '\n')
	tfile=open(outpf, 'w')
	head='{"type":"avl_resource","version":"b4","mu":0,"drivers":'
	tail='}'
	ps=[]												#driver data array
	wb=xlrd.open_workbook(inpf)
	sheet=wb.sheet_by_index(0)
	un = [sheet.row_values(rownum) for rownum in range(1,sheet.nrows)]
	for i in range(len(un)):							#cycle xls file
		p={}
		name=str(un[i][0]).replace('.0','')				#driver name
		code=str(un[i][1]).split('.')[0]				#driver code
		dscr=str(un[i][2])								#driver description
		pn=str(un[i][3])								#driver phone number (text with '+'!!!!)
		mk=str(un[i][4])								#driver mobile key
		if str(un[i][5]).split('.')[0]=="1":			#driver exclusive flag
			e="5"										#exclusive ON
		else:
			e="1"										#eclusive OFF
		jp={}
#		cust=list(filter(None, un[i][6:]))				#custom fields, filter without empty strings
		cust=list(un[i][6:])
#		cust=un[i][6:]									#custom fields
		if len(cust)%2!=0:
			cust.append('')
		j=len(cust)
		while j>0:
			if len(cust[0])==0:
				cust=cust[2:]
				j-=2
			else:
				jp[cust[0]]=str(cust[1]).replace('.0','')	#custom field name:custom field value
				cust=cust[2:]
				j-=2
		jpf=str(jp)											#formatted custom fields 
		p={"n":str(name),"c":str(code),"ds":str(dscr),"p":str(pn),"pwd":str(mk),"f":e,"jp":jpf}			#main parameters dictionary: Name, code, time
		ps.append(p)
	output=head+str(ps).replace("'",'"')+tail											#form the result string, but there is an issue with key "jp". It will have the quoters like "jp":'{data}'. Solved below.
	print(output.replace('"{','{').replace('}"','}').replace('O"',"O'").replace("O',",'O",').replace('L"E',"L'E").replace("NULL',",'NULL",').replace("NULL'}",'NULL"}'),file=tfile) 	#O'Connel, L'Estrange, but allow "NULL"
	print (outpf, ' created!')

###################################################################-TRAILERS-######################################################################################
def trailers(inpf, outpf):
	print ('Trying to create the Trailers file', outpf, '\n')
	tfile=open(outpf, 'w')
	head='{"type":"avl_resource","version":"b4","mu":0,"trailers":'
	tail='}'
	ps=[]												#trailer data array
	wb=xlrd.open_workbook(inpf)
	sheet=wb.sheet_by_index(0)
	un = [sheet.row_values(rownum) for rownum in range(1,sheet.nrows)]
	for i in range(len(un)):							#cycle xls file
		p={}
		name=str(un[i][0]).replace('.0','')				#trailer name
		code=str(un[i][1]).split('.')[0]				#trailer code
		dscr=str(un[i][2])								#trailer description
		if str(un[i][3]).split('.')[0]=="1":			#trailer exclusive flag
			e="6"										#exclusive ON
		else:
			e="2"										#eclusive OFF
		jp={}
		cust=list(un[i][4:])
		if len(cust)%2!=0:
			cust.append('')
		j=len(cust)
		while j>0:
			if len(cust[0])==0:
				cust=cust[2:]
				j-=2
			else:
				jp[cust[0]]=str(cust[1]).replace('.0','')	#custom field name:custom field value
				cust=cust[2:]
				j-=2
		jpf=str(jp)										#formatted custom fields 
		p={"n":str(name),"c":str(code),"ds":str(dscr),"f":e,"jp":jpf}					#main parameters dictionary: Name, code, time
		ps.append(p)
	output=head+str(ps).replace("'",'"')+tail											#form the result string, but there is an issue with key "jp". It will have the quoters like "jp":'{data}'. Solved below.
	print(output.replace('"{','{').replace('}"','}').replace('O"',"O'").replace("O',",'O",').replace('L"E',"L'E").replace("NULL',",'NULL",').replace("NULL'}",'NULL"}'),file=tfile) 	#O'Connel, L'Estrange, but allow "NULL"
	print (outpf, ' created!')



#Program start
main(ch,sfl,ofl)
