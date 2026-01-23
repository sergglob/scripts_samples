#!/bin/bash
#dbf python lbraty, python v3
#script to search the DBF files by name, to add the new column and its value

echo "Enter the filename to search: "
read flnm						#Filename to search
echo "Enter the place where to search: "
read dsear						#Folder to search
echo "Enter the column name to add (should be like <Intersect N(5,0)> or <City C(100)>: "
read c1							#Column to add
cc=`echo $c1 | tr a-z A-Z | cut -d ' ' -f1` 		#Get part of the column name for DBF.WRITE() function
echo "Enter the column data: "
read r1
echo "#####################################################################################################"
echo "Searching '$flnm' in  '$dsear' to add column  '$c1' with data  '$r1'"
echo "Press any key to continue if everything is fine, or CTRL+C to abort"
echo "#####################################################################################################"
read -s -n1 a

##############
crtf () {						#creating a pyhon script
echo "#!/usr/bin/python3.6" >> tmp.py
echo "#Developed by Novikov Sergey (nose)" >> tmp.py
echo "import dbf, os" >> tmp.py
echo "flnm = '$flnm'					#Filename to search"  >> tmp.py
echo "dsear = '$dsear'					#Folder to search" >> tmp.py
echo "c1='$c1'						#Column to add" >> tmp.py
echo "r1 ='$r1'						#Column value to add" >> tmp.py
####################
echo "def find_files(filename, search_path):			#filename, folder where to search the file" >> tmp.py
echo "	result = []					#blank list of files" >> tmp.py
# Walking top-down from the root
echo "	for root, dir, files in os.walk(search_path):"  >> tmp.py
echo "		if filename in files:" >> tmp.py
echo "			result.append(os.path.join(root, filename))" >> tmp.py
echo "	return result" >> tmp.py
#
echo "lst=find_files(flnm,dsear)				#list of files found" >> tmp.py

####################
echo "def addt(f,c,r):					#file, column, row" >> tmp.py
echo "	db = dbf.Table(f)				#open file to append column\value" >> tmp.py
echo "	db.open()" >> tmp.py
echo "	with db:" >> tmp.py
echo "		db.add_fields(c)			#add column name" >> tmp.py
echo "	if len(str(r))!=0:" >> tmp.py
echo "		for i in db:" >> tmp.py
echo "			dbf.write(i, $cc=str(r))	#add column value" >> tmp.py
echo "	db.close()" >> tmp.py
####################

##MAIN CYCLE##
echo "for i in range(len(lst)):" >> tmp.py
echo "	print('----------------------------------------------')" >> tmp.py
echo "	print('Replacing: ', lst[i])" >> tmp.py
echo "	try:" >> tmp.py
echo "		addt(lst[i], c1, r1)" >> tmp.py
echo "	except:" >> tmp.py
echo "		print('Already has such field')" >> tmp.py
echo "		pass" >> tmp.py
echo "	print('----------------------------------------------')" >> tmp.py

}
crtf
chmod u+x tmp.py
./tmp.py						#executing temp python script
echo "Deleting the temporary files and $flnm _backup" 
rm tmp.py						#remove temp python script
find $dsear -name "*_backup.dbf" -delete
echo "print('Script work copleted!')"
