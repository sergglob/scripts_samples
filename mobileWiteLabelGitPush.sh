#!/bin/bash
#Developed by Novikov Sergei, tech support department, Gurtam company

clear

#################################################################################################
pre_design () {

clear
echo "This script was created to authomatize the git push process for the sites personalisation"

#Getting current user name, date
local usr=$USER
local d=$(date)
#absolute path /home/GURTAM/$usr
echo "The default skins folder /home/GURTAM/$usr/skins"
echo "The default logos folder /home/GURTAM/$usr/Downloads"
echo "The script will replace the old logos as well, if there are present the old logos in the directory"

#Requesting the new skin folder name, creating the log file (you can change the default logs directory)
echo "Enter the new skin folder name"
read new_skin
echo "Creating the log file"
touch ~/Downloads/$new_skin.log

#comment description
descr="Applying $new_skin logos by $usr"

#Entering the SKINS folder (you may change the path according to your directories tree). Synchronising the SKINS folder with last GIT updates.

cd ~/skins
echo "Wait till the git pull completed"
git pull > ~/Downloads/$new_skin.log

}

#################################################################################################

lite_design () {

echo "Creating directory for the wialon lite skin"
			mkdir -p ~/skins/master/$new_skin/lite >> ~/Downloads/$new_skin.log
			echo "Copying logos"
			if [ ! -f ~/skins/master/$new_skin/lite/favicon.ico ]
				then 
					mv ~/Downloads/favicon.ico ~/skins/master/$new_skin/lite/favicon.ico >> ~/Downloads/$new_skin.log
				else
					mv  ~/skins/master/$new_skin/lite/favicon.ico ~/skins/master/$new_skin/lite/favicon_old >> ~/Downloads/$new_skin.log
					mv ~/Downloads/favicon.ico ~/skins/master/$new_skin/lite/favicon.ico >> ~/Downloads/$new_skin.log
			fi
			if [ ! -f ~/skins/master/$new_skin/lite/top-logo.png ]
				then 
					mv ~/Downloads/top-logo.png ~/skins/master/$new_skin/lite/top-logo.png >> ~/Downloads/$new_skin.log
				else
					mv  ~/skins/master/$new_skin/lite/top-logo.png ~/skins/master/$new_skin/lite/top-logo_old >> ~/Downloads/$new_skin.log
					mv ~/Downloads/top-logo.png ~/skins/master/$new_skin/lite/top-logo.png >> ~/Downloads/$new_skin.log
			fi
			if [ ! -f ~/skins/master/$new_skin/lite/login-logo.png ]
				then 
					mv ~/Downloads/login-logo.png ~/skins/master/$new_skin/lite/login-logo.png >> ~/Downloads/$new_skin.log
				else
					mv  ~/skins/master/$new_skin/lite/login-logo.png ~/skins/master/$new_skin/lite/login-logo_old >> ~/Downloads/$new_skin.log
					mv ~/Downloads/login-logo.png ~/skins/master/$new_skin/lite/login-logo.png >> ~/Downloads/$new_skin.log
			fi
#Adding files to GIT
			echo "Adding files to GIT"

			git add ~/skins/master/$new_skin/lite/favicon.ico >> ~/Downloads/$new_skin.log 2>/dev/null
			git add ~/skins/master/$new_skin/lite/top-logo.png >> ~/Downloads/$new_skin.log 2>/dev/null
			git add ~/skins/master/$new_skin/lite/login-logo.png >> ~/Downloads/$new_skin.log 2>/dev/null

git_commit
log_process
sleep 15
menu

}

##################################################################################################

master_design () {

#Creating the new skin folder and inner directories
echo "The logos should be named correctly: logo_bg.png, logo.png, favicon.ico, favicon.gif"
echo "Creating image directories"
mkdir ~/skins/master/$new_skin >> ~/Downloads/$new_skin.log
mkdir ~/skins/master/$new_skin/images >> ~/Downloads/$new_skin.log
mkdir ~/skins/master/$new_skin/images/login >> ~/Downloads/$new_skin.log
mkdir ~/skins/master/$new_skin/images/logo >> ~/Downloads/$new_skin.log

#Copying the new logos and favicon from the default foulder into the new folders, change the path to the default folder if necessary and use the correct logos names.
echo "Copying logos"
if [ ! -f ~/skins/master/$new_skin/images/favicon.ico ]
	then 
		mv ~/Downloads/favicon.ico ~/skins/master/$new_skin/images/favicon.ico >> ~/Downloads/$new_skin.log 2>/dev/null
		mv ~/Downloads/favicon.gif ~/skins/master/$new_skin/images/favicon.ico 2>/dev/null 
	else
		mv  ~/skins/master/$new_skin/images/favicon.ico ~/skins/master/$new_skin/images/favicon_old >> ~/Downloads/$new_skin.log
		mv ~/Downloads/favicon.ico ~/skins/master/$new_skin/images/favicon.ico >> ~/Downloads/$new_skin.log
		mv ~/Downloads/favicon.gif ~/skins/master/$new_skin/images/favicon.ico 2>/dev/null 
fi

if [ ! -f ~/skins/master/$new_skin/images/login/logo_bg.png ]
	then 
		mv ~/Downloads/logo_bg.png ~/skins/master/$new_skin/images/login/logo_bg.png >> ~/Downloads/$new_skin.log
	else
		mv  ~/skins/master/$new_skin/images/login/logo_bg.png ~/skins/master/$new_skin/images/login/logo_bg_old >> ~/Downloads/$new_skin.log
		mv ~/Downloads/logo_bg.png ~/skins/master/$new_skin/images/login/logo_bg.png >> ~/Downloads/$new_skin.log
fi

if [ ! -f ~/skins/master/$new_skin/images/logo/logo.png ]
	then 
		mv ~/Downloads/logo.png ~/skins/master/$new_skin/images/logo/logo.png >> ~/Downloads/$new_skin.log
	else
		mv  ~/skins/master/$new_skin/images/logo/logo.png ~/skins/master/$new_skin/images/logo/logo_old >> ~/Downloads/$new_skin.log
		mv ~/Downloads/logo.png ~/skins/master/$new_skin/images/logo/logo.png >> ~/Downloads/$new_skin.log
fi

#Adding files to GIT
echo "Adding files to GIT"
 
git add ~/skins/master/$new_skin/images/favicon.ico >> ~/Downloads/$new_skin.log 2>/dev/null
git add ~/skins/master/$new_skin/images/login/logo_bg.png >> ~/Downloads/$new_skin.log 2>/dev/null
git add ~/skins/master/$new_skin/images/logo/logo.png >> ~/Downloads/$new_skin.log 2>/dev/null

git_commit
log_process
sleep 15
menu

}

##################################################################################################
##################################################################################################
#Check certificate and key for SSL function
cert_check () {
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
	0) menu;;
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
if [ "$md5_key"=="$md5_ssl" ]
	then
	echo "The md5 sum is equal"
#Starting XCA application
	xca_app
	else
	echo "The md5 sum is NOT equal"
fi
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
sleep 10
start
}

##################################################################################################
#Creating text menu
menu () {
clear
echo -e "Select the required operation\n"
echo -e "0 - Exit program\n"
echo -e "1 - Master site personalisation\n"
echo -e "2 - Lite site personalisation\n"
echo -e "3 - RSA key and certificate check"

read -n 1 -s yourchoose

case $yourchoose in
		0) exit;;
		1)
				echo "Starting master branch site personalisation"
				pre_design
				master_design;;
		2)
				echo "Starting lite branch site personalisation"
				pre_design
				lite_design;;
		3)
				echo "Starting RSA key and certificate check"
				cert_check;;
		*) echo "Input error!. Back to menu"
				start;;
	
esac
}

##################################################################################################
#Commiting to GIT function
git_commit () {
#Commiting the changes, getting the commit status and pushing files to GIT
echo "Committing changes"
git commit -m "$descr" >> ~/Downloads/$new_skin.log
git status >> ~/Downloads/$new_skin.log
git push origin master >> ~/Downloads/$new_skin.log

echo "Script work is completed! Check the log file for more details."
/usr/bin/google-chrome http://update-wdc.gurtam.net/
}

##################################################################################################
#Processing the personalisation log function

log_process () {
# Read or/and save log file.
echo "Show log file (y)? Any other key to exit."
read -n1 -t10 conf
if [ $conf == "y" ]
	then 
		cat ~/Downloads/$new_skin.log
	else
		echo ""
fi

echo "Save log file (y)? Any other key to exit."
read -n1 -t10 conf
if [ $conf == "y" ]
	then 
		echo "Log file saved!"
	else
		rm ~/Downloads/$new_skin.log
fi
}

##################################################################################################
start () {
echo "Wait.."
sleep 1
clear
menu
}
start
menu

