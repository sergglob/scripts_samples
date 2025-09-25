#!/bin/bash
NO='\033[0m'
BL='\033[0;34m'
RE='\033[0;31m'
GR='\033[0;32m'
YE='\033[1;33m'
read -p "Enter the S3 group name: " gn
read -p "Enter the dedicated storage in GB: " size
password=$(tr -dc 'A-Z' < /dev/urandom | head -c 2;tr -dc '0-9' < /dev/urandom | head -c 2;tr -dc '!?%=' < /dev/urandom | head -c 2;tr -dc 'a-z' < /dev/urandom | head -c 2;tr -dc '0-9' < /dev/urandom | head -c 2)
kib=$(echo "$size*976562.5" | bc)
echo "##########################################################################################"
echo -e "Open ${BL}https://s3-minsk.becloud.by:8443/Cloudian/login.htm${NO} as admin group"
echo -e "Users & Groups - Manage Groups - New Group: ${GR}$gn${NO}"
echo -e "Users & Groups - Manage Groups - Search for a Group by Name: ${GR}$gn${NO}"
echo -e "ACTIONS / Group QoS - Storage Quota (KiB) / High Limit: ${YE}$kib${NO}"
echo "---"
echo "Users & Groups - Manage Users - New user"
echo -e "User ID: ${GR}$gn""_admin${NO}"
echo -e "User Type: ${GR}Group Admin${NO}"
echo -e "Group Name: ${GR}$gn${NO}"
echo -e "Password: ${RE}$password${NO}"
echo "------------------------------------------------------------------------------------------"
echo "Уважаемый клиент
Вам предоставлен доступ к управлению объектным хранилищем:
https://s3-minsk.becloud.by:8443/Cloudian/login.htm
group: $gn
user: $gn""_admin
passwd: $password
Storage Quota $size GB: $kib KiB
Руководство пользователя во вложении."
echo "##########################################################################################"



