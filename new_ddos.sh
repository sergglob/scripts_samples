#!/bin/bash
#Developed by Sergey Novikov
#Script for searching possible DDoS in current/today logs on SVH
req () {
#    read -p "Enter the time mark for search (like 9:22): " tm
    tm=$(date +%H:%m)
#    reqf="req_$(date +"%H-%M-%S_%d%m%y").txt"
    sitesf="sites_$(date +"%H-%M-%S_%d%m%y").txt"
    echo "__________________________________________________________________________________________" | tee -a /tmp/$reqf /tmp/$sitesf
    for i in $(ls /var/www/httpd-logs/| grep access);do echo $i; grep "$tm" /var/www/httpd-logs/$i| wc -l;done >> sites.tmp
    sed -i ':a;N;$!ba;s/.log\n/.log /g' sites.tmp
    hd="10" #top search results == 10
    cat sites.tmp | sort -k2 -nr | head -n $hd  | tee -a /tmp/$reqf /tmp/$sitesf
    echo "__________________________________________________________________________________________" | tee -a /tmp/$reqf /tmp/$sitesf
    rm sites.tmp
    echo "" | tee -a /tmp/$reqf
}

crec () {	#custom time ddos search
    read -p "Enter the time mark for search (like 9:22): " tm
#    tm=$(date +%H:%m)
#    reqf="req_$(date +"%H-%M-%S_%d%m%y").txt"
    sitesf="sites_$(date +"%H-%M-%S_%d%m%y").txt"
    echo "__________________________________________________________________________________________" | tee -a /tmp/$reqf /tmp/$sitesf
    for i in $(ls /var/www/httpd-logs/| grep access);do echo $i; grep "$tm" /var/www/httpd-logs/$i| wc -l;done >> sites.tmp
    sed -i ':a;N;$!ba;s/.log\n/.log /g' sites.tmp
    hd="10" #top search results == 10
    cat sites.tmp | sort -k2 -nr | head -n $hd  | tee -a /tmp/$reqf /tmp/$sitesf
    echo "__________________________________________________________________________________________" | tee -a /tmp/$reqf /tmp/$sitesf
    rm sites.tmp
    echo "" | tee -a /tmp/$reqf
}

log () {
    cat  /tmp/$sitesf
    echo "#######################################" | tee -a /tmp/$reqf
    read -p "Enter the site log name: " site
    echo "#######################################" | tee -a /tmp/$reqf
    echo "##### $site #####" | tee -a /tmp/$reqf
    lt
}

lt () {
    read -p "___Time search (like 10: or 12:1), [Q/q] for quit: " t
    if [[ $t == "q" || $t == "Q" ]]
    then
    echo "Results file - /tmp/$reqf"
    st
    else
    echo "------ at $t ------" >> /tmp/$reqf
    cat  /var/www/httpd-logs/$site | grep "$t" |awk '{print$1}' | sort -n | uniq -c | sort -nr | head -n $tip > ips.tmp
    cat ips.tmp | tee -a /tmp/$reqf
    rm ips.tmp
    echo "----------------------------------------------" | tee -a /tmp/$reqf
    echo "Report results: /tmp/$reqf"
    lt
    fi
}

st () {
    echo "________________________________________ $(date) ________________________________________" | tee -a /tmp/$reqf
    echo "[S/s] select site for ip search"
    echo "[R/r] search ddos for the specific time (not current time)"
    echo "[D/d] docker stats"
    echo "[H/h] apache/nginx total requests and memory"
    echo "[P/p] php users' process count and list"
    echo "[K/k] kill mysql user process"
    echo "[RESTRICT/UNRESTRICT] by Belarus zone"
    echo "[Q/q] for quit"
    read -p "__________________________Enter the search key: " tm
    tip="10"    #Number of the TOP IPs access site == 10
    case $tm in
	"q"|"Q") echo "Results file - /tmp/$reqf"; exit 0;;
	"d"|"D") docker stats --no-stream | tee -a /tmp/$reqf; st;;
	"h"|"H") proxy | tee -a /tmp/$reqf;st;;
        "p"|"P") php | tee -a  /tmp/$reqf; st;;
	"k"|"k") kill;st;;
	"RESTRICT") sed -i "s/#include belips_restrict.conf;/include belips_restrict.conf;/" /etc/nginx/tuning.conf;nginx -t && nginx -s reload; st;;
	"UNRESTRICT") sed -i "s/include belips_restrict.conf;/#include belips_restrict.conf;/" /etc/nginx/tuning.conf; nginx -t && nginx -s reload; st;;
	"s"|"S")log;;
	"r"|"R")crec;st;;
    *) echo "Wrong key!";st
    esac
}

proxy () {
echo "--- httpd:"
service httpd status | grep "Total\|Memory"
echo "--- nginx:"
service nginx status | grep "Tasks\|Memory"
}

php () {
echo "PHP: $(ps ax o user:16,pid,pcpu,pmem,cmd | grep user | grep -c php)"
echo "php-cgi: $(ps ax o user:16,pid,pcpu,pmem,cmd | grep user | grep -c php-cgi)"
echo "lsphp: $(ps ax o user:16,pid,pcpu,pmem,cmd | grep user | grep -c lsphp)"
echo "Top 5 users:"
ps ax o user:16,cmd | grep user | grep php | awk '{print $1}' | sort | uniq -c | sort -nr | head -n 5
echo "--------------------------------------- mytop -------------------------------------------"
mytop -b | grep user | awk '{print$3}' |sort | uniq -c | sort -nr | head -n 5	#show mytop utility process list
echo "--------------------------------------- db threads -------------------------------------------"
echo "native:: $(mysql -s -e "SHOW STATUS LIKE 'Threads_connected';")"
for c in $(docker container ls | grep -v IMAGE | awk '{print$1}')
do
    echo "$(docker container ls | grep $c | awk '{print$2}'):: $(docker exec -ti $c mysql -s -e "SHOW STATUS LIKE 'Threads_connected';" | grep -v Value)"
done
}

kill () {
	read -p "__________________________Enter the user to kill, [Q/q] to abort: " kl
	case $kl in
	"q"|"Q") st;;
	*) for proc in $(mysql -e "show processlist;" | grep $kl | awk '{print$1}');do mysql -e "kill $proc;"; echo "$kl: killed proc $proc" | tee -a /tmp/$reqf; done;st;;
	esac
}

echo "POSSIBLE DDOS CHECK"
echo "This script developed to analyse top sites by requests in a timestamp, and top ips by requests toward the site, resources load"
reqf="req_$(date +"%H-%M-%S_%d%m%y").txt"
req
st
