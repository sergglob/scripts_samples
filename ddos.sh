#!/bin/bash
#Developed by Sergey Novikov
#Script for searching possible DDoS in current/today logs on SVH
req () {
    read -p "Enter the time mark for search (like 9:22): " tm
    reqf="req_$(date +"%H-%M-%S_%d%m%y").txt"
    echo "__________________________________________________________________________________________" > $reqf
    for i in $(ls /var/www/httpd-logs/| grep access);do echo $i; grep "$tm" /var/www/httpd-logs/$i| wc -l;done >> sites.tmp
    sed -i ':a;N;$!ba;s/.log\n/.log /g' sites.tmp
    read -p "Number of TOP access sites to display: " hd
    cat sites.tmp | sort -k2 -nr | head -n $hd  | tee -a $reqf
    echo "__________________________________________________________________________________________" >> $reqf
    rm sites.tmp
    echo ""
    read -p "Enter the site log name: " site
    echo "##### $site #####" >> $reqf
}
st () {
    read -p "Enter the time search (like 10: or 12:12): " tm
    read -p "Number of the TOP IPs access site $site: " tip
echo "------ at $tm ------" >> $reqf
    cat  /var/www/httpd-logs/$site | grep "$tm" |awk '{print$1}' | sort -n | uniq -c | sort -nr | head -n $tip > ips.tmp
    cat ips.tmp | tee -a $reqf
    rm ips.tmp
    rtr
}
rtr () {
    read -s -n 1 -p "Repeat $site search for TOP IPs for another timestamp (y/Y)? " ch
    case $ch in 
	y) st;;
	Y) st;;
	*) cat $reqf
    esac
}



echo "This script developed to analyse top sites by requests in a timestamp, and top ips by requests toward the site"
req
st
echo "Results file - $(pwd)/$reqf"
