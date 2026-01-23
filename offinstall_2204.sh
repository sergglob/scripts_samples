#!/bin/bash

#clearing additional sources
rm /etc/apt/sources.list.d/* 
#and cached packets
rm `find /var/lib/apt/lists/ -type f`
#and original sources list
cat /dev/null > /etc/apt/sources.list

#detecting distro and replacing source with right ones just in case
DISTRO=$(cat /etc/debian_version | cut -c 1)
if [ ${DISTRO} == 1 ]
then
	DISTRO10=$(cat /etc/debian_version | cut -c 2)
		if [ ${DISTRO10} == 0 ]
		then
			echo "Debian 10 detected"
			echo -e "deb http://deb.debian.org/debian/ buster main contrib non-free\ndeb-src http://deb.debian.org/debian/ buster  main contrib non-free\ndeb http://deb.debian.org/debian/ buster-updates main contrib non-free\ndeb-src http://deb.debian.org/debian/ buster-updates main contrib non-free\ndeb http://security.debian.org/debian-security/ buster/updates main contrib non-free\ndeb-src http://security.debian.org/debian-security/ buster/updates main contrib non-free\ndeb http://http.debian.net/debian scretch-backports main\ndeb-src http://http.debian.net/debian scretch-backports main" > /etc/apt/sources.list
		elif [ ${DISTRO10} == 1 ]
		then
			echo "Debian 11 detected"
			echo -e "deb http://deb.debian.org/debian/ bullseye main contrib non-free\ndeb-src http://deb.debian.org/debian/ bullseye  main contrib non-free\ndeb http://deb.debian.org/debian/ bullseye-updates main contrib non-free\ndeb-src http://deb.debian.org/debian/ bullseye-updates main contrib non-free\ndeb http://security.debian.org/debian-security/ bullseye-security main contrib non-free\ndeb-src http://security.debian.org/debian-security/ bullseye-security main contrib non-free" > /etc/apt/sources.list
		fi
elif [ ${DISTRO} == 9 ]
then
	echo "Debian 9 detected"
	echo -e "deb http://deb.debian.org/debian/ stretch main contrib non-free\ndeb-src http://deb.debian.org/debian/ stretch main contrib non-free\ndeb http://deb.debian.org/debian/ stretch-updates main contrib non-free\ndeb-src http://deb.debian.org/debian/ stretch-updates main contrib non-free\ndeb http://security.debian.org/debian-security/ stretch/updates main contrib non-free\ndeb-src http://security.debian.org/debian-security/ stretch/updates main contrib non-free\ndeb http://http.debian.net/debian scretch-backports main\ndeb-src http://http.debian.net/debian scretch-backports main" > /etc/apt/sources.list
elif [ ${DISTRO} == 8 ]
then
	echo "Debian 8 detected"
	echo -e "deb http://deb.debian.org/debian/ oldstable main contrib non-free\ndeb-src http://deb.debian.org/debian/ oldstable main contrib non-free\ndeb http://deb.debian.org/debian-security oldstable/updates main\ndeb-src http://deb.debian.org/debian-security oldstable/updates main" > /etc/apt/sources.list
else
	echo "Unknown Debian in /etc/debian_version, exiting"
	exit -1
fi

#update sources and install software
apt-get -qq --allow-releaseinfo-change update
apt-get install -y openssh-server htop dstat nginx ntp sudo tmux fail2ban unzip unrar gdb rsync screen libgomp1 wget p7zip-full pigz curl

#install nodejs for c18 - it doesn't contain this package
if [ ${DISTRO} == 8 ]
then
	apt-get install -y nodejs npm
fi

#correct date is important
dpkg-reconfigure tzdata
service ntp restart

#create a main user
groupadd wialon
useradd -u 1070 -m -g wialon -G dialout wialon
echo "wialon:wialon" | chpasswd

#check for the folder
if [ ! -d /home/wialon/ ]
then
	mkdir /home/wialon/
	chown -R wialon /home/wialon
fi

#create installation folder
mkdir /install/
cd /install/

#download and unpack Wialon Local .iso
if [ ${DISTRO} == 1 ]
then
		if [ ${DISTRO10} == 0 ]
		then
			ISO_FILENAME="wialon_local_2104.iso"
			wget  https://distro.gurtam.com/local/$ISO_FILENAME --no-check-certificate
		elif [ ${DISTRO10} == 1 ]
		then
			ISO_FILENAME="wialon_local_2204.iso"
			wget  https://distro.gurtam.com/local/$ISO_FILENAME --no-check-certificate
		fi
elif [ ${DISTRO} == 9 ]
then
	ISO_FILENAME="wialon_local_1904.iso"
	wget  https://distro.gurtam.com/local/$ISO_FILENAME --no-check-certificate
elif [ ${DISTRO} == 8 ]
then
	ISO_FILENAME="wialon_local_c18.iso"
	wget  https://distro.gurtam.com/local/$ISO_FILENAME --no-check-certificate
fi
7z x $ISO_FILENAME
cp -R /install/ext/* /install/

#finish the installation
chmod +x postinstall.sh
./postinstall.sh

service wlocal restart
sleep 1
nginx -s reload

exit 0

