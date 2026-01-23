#!/bin/bash
#ssh tunnel script by Sergei Novikov
echo "To open the SSH tunel you must work under the 'root' user or have rights to open custom ports"
menu () {
echo "Select the operation:"
echo "1 - enter the ports/network separately"
echo "2 - connect by the full tunnel command string (ssh -f -N -L local_port:local_network:connection_port user@external_network -p ssh_port)"
echo "0 - close ssh tunel and exit"
echo "###CTRL + C to exit the script###"
read -s -n 1 choice
case $choice in 
	1) manual;;
	2) echo "HAHAHA, You do not need this script then*); Back to the menu"; sleep 3; menu;;
	0) killer;;
	*) echo "Wrong input!"; menu;;
esac
}

manual () {
echo -e "Enter the SSH user name\n"
read ssh_name
echo -e "Enter the SSH server address/IP\n"
read ssh_ip
echo -e "Enter the SSH custom connection port, default 22\n"
read ssh_port
echo -e "Enter the custom connection port, 80 for the WL admin panel, 8024 CMS site, 8025 WEB site\n"
read site_port
echo -e "Enter the local server address/ip\n"
read local_ip
echo -e "Enter the proxy port on your PC, 500X (X = 1, 2, 3, etc) recommended\n"
read proxy_port
echo -e "Establishing the tunnel\n"
echo -e "Trying 'ssh -f -N -L $proxy_port:$local_ip:$site_port $ssh_name@$ssh_ip -p $ssh_port'"
ssh -f -N -L $proxy_port:$local_ip:$site_port $ssh_name@$ssh_ip -p $ssh_port
echo -e "If the tunnel process present - all is fine\n"
netstat -pnlt | grep ":$proxy_port"
echo -e "\n"
echo -e "#################"
echo -e "The site should be available on 127.0.0.1:$proxy_port"
echo -e "#################"
echo -e "Press any key to back to the menu\n"
read -s -n 1 anykey
menu
}
killer () {
echo -e "Checking the process. If will be fond - you should kill it forcibly"
ps -aux | grep "$proxy_port" | grep "ssh"
tun_pid=`ps -aux | grep "$proxy_port" | grep "ssh" | awk '{ print $2 }'`
echo -e "The ssh tunnel PIDs found: $tun_pid"
echo -e "Kill the tunnel now (Y/y) or later(anykey)?\n"
read -s -n 1 now
case $now in 
	y|Y|н|Н) echo -e "Confirm the PID to kill $tun_pid\n"; read tun_pid_conf; kill  $tun_pid_conf; echo -e "The process  $tun_pid_conf should be killed! Back to the menu\n"; menu;;
	*) echo -e "Back to menu"; menu;;
esac	
}
menu


