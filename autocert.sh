#!/bin/bash
#Novikov Sergei, tech support department, Gurtam company
clear
echo "This programm allows to check the SSL certificates and keys"
echo "The supported certificates are *.crt, *.p12, *.pfx, *.csr"

###########################################################################
#Certificates and key parh function
cert_path () {
work_dir=`pwd`
echo "Specify the KEY name, use absolute path if the KEY is not placed in the same directory as the script is"
echo "For example '$work_dir/key_name.key'"
read key_name
echo "Specify the CERTIFICATE name, use absolute path if the CERTIFICATE is not placed in the same directory as the script is"
read cert_name
}

###########################################################################
cert_path_recheck () {
echo "Your KEY name is $key_name"
echo "Your CERTIFICATE name $cert_name"
echo "Press any key, if the KEY name or the CERTIFICATE name is not correct."
echo "Press 'Enter' or 'Space' bar, or do nothing fot hte next 5 sec, if everything is fine" 
read -t 5 -n 1 -s key_cert_name_check
if [ -z "$key_cert_name_check" ]
	then echo "The KEY and the CERTIFICATE names are correct, proceeding..."
	else echo "The WRONG KEY name or CERTIFICATE name"
	echo "Enter the KEY and CERTIFICATE names again"
	cert_path
fi
}
#############################################################################
#Certificate check menu
cert_menu () {
echo "Specify the certificate check process"
echo "1 - CRT certificate check"
echo "2 - PKCS12 (P12, PFX) certificate check"
echo "3 - CSR certificate check"
echo "0 - Abort all, back to menu"
read -n 1 -s cert_check
case $cert_check in
	0) exit;;
	1) clear
	openssl x509 -in $cert_name -text -noout
	md5_ssl=`openssl x509 -noout -modulus -in $cert_name 2> /dev/null | openssl md5`;;
	2) clear
	openssl pkcs12 -info -in $cert_name
	md5_ssl=`openssl x509 -noout -modulus -in $cert_name 2> /dev/null | openssl md5`;;
	3) clear
	openssl req -text -noout -verify -in $cert_name
	md5_ssl=`openssl req -noout -modulus -in $cert_name | openssl md5`;;
esac
}

#################################################################################
key_menu () {
echo "Checking key"
openssl rsa -in $key_name -check 1> /dev/null
md5_key=`openssl rsa -noout -modulus -in $key_name 2> /dev/null | openssl md5`
}

#################################################################################
md5_sums () {
echo "KEY= $md5_key"
echo "CER= $md5_ssl"
#if [ "$md5_key"=="$md5_ssl" ]
#	then
#	echo "The md5 sum is equal"
#Starting XCA application
	xca_app
#	else
#	echo "The md5 sum is NOT equal"
#fi
}

#################################################################################
xca_app () {
echo "Starting XCA application"
if [ -f "/usr/bin/xca" ]
	then
	/usr/bin/xca
	else
	echo "You have no XCA app installed on your PC. Contact your system administrator"
fi
}
#################################################################################
#################################################################################
#Main SSL script body
cert_path
cert_path_recheck
cert_menu
key_menu
md5_sums
