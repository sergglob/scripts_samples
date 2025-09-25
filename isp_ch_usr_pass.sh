#!/bin/bash
#Generate and set new password for the ISP users from list
#Developed by Sergey Novikov, L2_itrp
#to run the script path the users' list file: bash isp_ch_usr_pass.sh <users_list_file>
#the users_list_file should contain IPS users - each user on separate newline

body () {
    if [ -f /usr/bin/pwgen ]
    then
        echo "pwgen present! Trying to generate and change passwords"
        while read username
            do
            ch_pswd
            done < $fl #passing the users' list file
    else
        echo "pwgen utility is absent. It need for generating password, recheck if it present in environment (which pwgen)"
        echo "If pwgen binary placed not in /usr/bin/pwgen - you can fix the path in this script to relaunch"
        exit
    fi
}

ch_pswd () {
    passwd=`pwgen -s 16 1`
#/usr/local/mgr5/sbin/mgrctl -m ispmgr user.edit name=user10111 level=user sok=ok passwd="Ha#evKSeU{Y5i_)" elid=user10111
    echo "Trying change password for $username --- $passwd"| tee -a changed_passwords.txt    
    /usr/local/mgr5/sbin/mgrctl -m ispmgr user.edit name=$username level=user sok=ok passwd=$passwd elid=$username | tee -a changed_passwords.txt
}

if [ $# -eq 0 ]    
then
    echo "Pass the users' file when running the script"
    echo "Sample: bash isp_ch_usr_pass.sh users.txt"
    exit
elif [ $# -eq 1 ]
then
    echo "Trying processing the file: $1"
    fl=$1
    body
else
    echo "It seems you passed to many variables: $@"
    echo "Restart the script with single variable - users list file"
    exit
fi

