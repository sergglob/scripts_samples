#!/bin/bash

menu () {
clear
echo "This script will create the android app certificate or/and show you SHA1 string."
echo "1 - Create certificate"
echo "2 - Show SHA1"
echo "3 - Register ANDROID PUSH notifications"
echo "4 - Register IOS PUSH notifications (Demo)"
echo "5 - Delete PUSH signatures"
echo "0 - Exit"
read -n 1 -s choise
case $choise in
	0) exit;;
	1) create_cert;;
	2) show_sha1;;
	3) android_push;;
	4) ios_push;;
	5) push_delete;;
	*) menu;;
esac
}
##################################################
create_cert () {
store_dir=`cd ~/Downloads | pwd`
echo " You will be asked about:
What is your first and last name?
What is the name of your organizational unit?
What is the name of your organization?
What is the name of your City or Locality?
What is the name of your State or Province?
What is the two-letter country code for this unit?"

echo "Enter the company identifier"
read company_name
echo "The certificate will be stored $store_dir"
echo "By default we use the keystore password '123456'"
sleep 3
keytool -genkey -v -keystore ~/Downloads/key_$company_name -alias $company_name -keyalg RSA -keysize 2048 -validity 10000
back_to_menu
}
##################################################
show_sha1 () {
echo "Set the direct path to the certificate"
echo "Or just tupe the certificate name, if it was placed in the same directory as a script"
echo "The name may be 'key_$company_name'"
read cert_path
sha1=`keytool -keystore $cert_path -list -v | grep 'SHA1'` 2>/dev/null
echo $sha1
back_to_menu
}
##################################################
android_push () {
echo "Enter the bundle name (e.g. "com.wialon.wialonapp")"
read bundle_name
echo "Enter the Google cloud messaging Key (from firebase)"
read firebase_key
#curl="/usr/bin/curl -X POST 'http://mg-2.sig.gurtam.local:9004/app?data=\{\"name\":\"$bundle_name\",\"provider\":\"gcm\",\"key\":\"$firebase_key\",\"certificate\":\"\"\}'"
#echo $curl
#$curl
dat="/app?data=\{\"name\":\"$bundle_name\",\"provider\":\"gcm\",\"key\":\"$firebase_key\",\"certificate\":\"\"\}"

curl -X POST 'http://mg-2.sig.gurtam.local:9004'$dat

back_to_menu
}
##################################################
back_to_menu () {
echo "Press any key to back to the menu"
read -s -n 1 anykey
menu
}
##################################################
push_delete () {
echo "Find the signature ID on the site by the app bundle name (e.g. "com.wialon.wialonapp")"
/usr/bin/google-chrome http://mg-2.sig.gurtam.local:9004/apps
sleep 5
echo "Enter the ID to delete"
read del_id
del_dat="id=$del_id"
echo "$del_id is correct? Press 'c' to cansel, any other key to proceed"
read -n 1 -s corr
case $corr in
	"c"|"C"|"с"|"С") echo "Mission aborted!";back_to_menu;;
	*) curl -X DELETE -F $del_dat 'http://mg-2.sig.gurtam.local:9004/app';back_to_menu;;
esac
}
##################################################
ios_push () {
echo "Enter the app bundle (e.g. "com.wialon.wialonapp")"
read bundle_push_name
echo "Enter the production key absolute path, or place the 'prod_key.pem' (default name) in the same directory as a script (then just specify the key name)"
read prod_key
echo "Enter the production certificate absolute path, or place the 'prod_cer.pem' (default name) in the same directoryas a script (then just specify the certificate name)"
read prod_cer
dat_push="/app?data=\{\"name\":\"$bundle_push_name\",\"provider\":\"apns\",\"key\":\"$prod_key\",\"certificate\":\"$prod_cer\"\}"
curl -F "prod_key=@prod_key.pem" -F "prod_cer=@prod_cer.pem" -X POST 'http://mg-2.sig.gurtam.local:9004'$dat_push
back_to_menu
}

menu
