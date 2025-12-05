#Developed by Siarhei Novikau
#The script  search the duplicate files by content by checking md5sum
menu () {
if [ $count -ne '1' ]
then
	echo "Run script with directory path for search"
	echo "./dupmail.sh /var/www/mail/"
else
	search
	remove
fi
}

search () {
#Find all files, make a list
find -type f -exec md5sum {} \;  >> /tmp/found_files_$d
#find duplicates in file (single input md5sum for each dublicate)
for i in $(cat /tmp/found_files_$d | sort | awk '{print$1}'| uniq -d)
do
cat /tmp/found_files_$d  | grep $i
echo "---"
done >> /tmp/found_dupls_$d
}

remove () {
for i in $(cat /tmp/found_files_$d | sort | awk '{print$1}'| uniq -d)
do
cat /tmp/found_files_$d  | grep $i > /tmp/found_del_$d       #list of all duplicates found with the path to the file for each iteration/unique dublicate
cat /tmp/found_del_$d | tail -n +2 >> /tmp/found_removed_$d  #list removed files (except the first input dublicate from the list, all the rest - for deletion)
for j in $(cat /tmp/found_del_$d | tail -n +2 | awk '{print $2}')
do
	zip /tmp/found_del_$d.zip $j                             #zip the dublicate file
	rm -rf $j                                                #remove dublicate
done
done
rm /tmp/found_del_$d
echo "/tmp/found_files_$d --- all files found in a directory $dir"
echo "/tmp/found_dupls_$d --- all dublicate files found in $dir"
echo "/tmp/found_removed_$d --- removed files, backup copy in found_del_$d.zip"
}

d=$(date +%H%M%d%m)
count=$#
dir=$1
cd $dir
menu

