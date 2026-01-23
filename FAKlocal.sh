#!/bin/bash
#Developed by Sergey Novikov (nose)
nettest () {
testipport () {
	timeout 1 bash -c "cat < /dev/null > /dev/tcp/$1/$2"
	if [ $? != 0 ]
	then
		echo -e "${RED}Cannot establish connection with $1:$2 - $3 ${NORMAL}"
		tput sgr0
	else
		echo -e "${GREEN}Connection to $1:$2 successful - $3 ${NORMAL}"
		tput sgr0
	fi
}
testipport lic.gurtam.com 31176 "License server"
testipport local-api.wialon.com 443 "Module server"
testipport lic.gurtam.com 18711 "LBS server"
testipport lic.gurtam.com 18712 "Modile push server"
testipport lic.gurtam.com 18611 "Gurtam Maps service"
testipport lic.gurtam.com 18612 "Gurtam Maps service"
testipport lic.gurtam.com 18613 "Gurtam Maps service"
testipport lic.gurtam.com 18616 "Gurtam Maps service" 
testipport app-local.wialon.com 443 "Gurtam Apps service"
}
###########################################################################################################
wlcheck () {
echo -e "${BLUE}###########################################################################################################"
echo -e "${YELLOW}Starting the full check test. The log will be stored into the ${RED}'$homedir/wl_check.log'"
echo -e "${YELLOW}Starting license server access check"
tput sgr0
nettest
echo -e "${BLUE}###########################################################################################################"
echo -e "${YELLOW}Free space check. At least ${RED}30Gb ${YELLOW}free space in the mounted particion where /home/wialon/wlocal directoy placed."
echo -e "At least ${RED}100Mb ${YELLOW}free space in a root/boot particion '/'"
tput sgr0
df -Th
echo -e "${BLUE}###########################################################################################################"
echo -e "${YELLOW}RAM usage check. At least ${RED}1Gb${YELLOW} free RAM, the rest can be cached" 
tput sgr0
free -h
echo -e "${BLUE}###########################################################################################################"
echo -e "${YELLOW}Nginx syntax check"
tput sgr0
nginx -t
echo -e "${BLUE}###########################################################################################################"
echo -e "${YELLOW}Wialon local processes check. There should be adf and node processes running from wialon user"
tput sgr0
ps aux | grep adf | grep -v "grep"
ps aux | grep node | grep -v "grep"
echo -e "${BLUE}###########################################################################################################"
echo -e "${YELLOW}Checking the wialon logs on errors"
echo -e "Reading trace.log"
tput sgr0
cat /home/wialon/wlocal/logs/trace.log | grep -i "error"
echo -e "${YELLOW}Reading trace.log.1"
tput sgr0
cat /home/wialon/wlocal/logs/trace.log.1 | grep -i "error"
echo -e "${YELLOW}Reading lcm.log"
tput sgr0
cat /home/wialon/wlocal/logs/lcm/lcm.log | grep -i "error"
echo -e "${YELLOW}Reading lcm.log.1"
tput sgr0
cat /home/wialon/wlocal/logs/lcm/lcm.log.1 | grep -i "error"
echo -e "${BLUE}###########################################################################################################"
echo -e "${RED}Note!!! The lcm.log.1 may contain the old errors which are not binded with the current time issue."
echo -e "Analyse and depend on it only if there was no errors in lcm.log"
echo -e "${BLUE}###########################################################################################################"
echo -e "${YELLOW}Back to the menu"
tput sgr0
menu
}
###########################################################################################################
nginx_restart () {
nginx -s reload
service nginx status
echo -e "${YELLOW}Back to the menu"
tput sgr0
menu
}
###########################################################################################################
wl_restart () {
echo -e "${YELLOW}The additional log will be saved into $homedir/wl_restart.log"
echo -e "1 - restart service"
echo -e "2 - start adf_script"
echo -e "0 - back to the menu"
tput sgr0
read -s -n 1 rest_sel
case $rest_sel in 
	1) service wlocal restart; menu;;
	2) /home/wialon/wlocal/adf_script start; menu;;
	0) menu;;
	*) echo -e "${RED}Incorrect selection, back to the restart menu"; tput sgr0; wl_restart;;
esac
}
###########################################################################################################

menu () {
echo -e "${BLUE}###########################################################################################################"
echo -e "${RED}The script recommended to run under the root user${NORMAL}"
echo -e "${YELLOW}1 - Complex Wialon Local check."
echo -e "2 - Restart nginx, if the nginx config files are fine, Wialon Local works according to the logs and processes, but the sites admin/web are not loading"
echo -e "3 - Forced Wialon local restart, if there is no running adf or nodejs wialon process"
echo -e "0 - Quit script"
echo -e "Select the operation"
echo -e "${BLUE}###########################################################################################################"
tput sgr0
read -s -n 1 sel
case $sel in
	1) wlcheck | tee $homedir/wl_check.log
	echo -e "${GREEN}Test completed! Back to the menu"; tput sgr0; menu;;
	2) nginx_restart;;
	3) wl_restart | tee $homedir/wl_restart.log;;
	0) exit;;
	*) echo -e "${RED}Incorrect selection, back to the menu";tput sgr0; menu;;
esac
}
homedir=`cd ~; pwd`
BLUE='\033[0;34m'         # BLUE
YELLOW='\033[0;33m'       # Yellow
RED='\033[0;31m'         #  ${RED}
GREEN='\033[0;32m'      #  ${GREEN}
NORMAL='\033[0m'      #  ${NORMAL}
menu 

