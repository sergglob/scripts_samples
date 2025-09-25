#!/bin/bash
#Developed by Siarhei Novikau
dvp="/var/log/dovecot"
> $dvp/dovepass.found
while read line
do
i=$(echo $line | awk -F ':/var' '{print$2}' |  awk -F ':' '{print$1}')        #mailbox workdir path
if [ -n "$i" ]
then
a=$(grep -cF "$i:" /etc/dovecot/dovecot.passwd)         #count mailbox path found
if [[ "$a" -ne "0" && "$a" -ne "1" ]]
then
echo $line >> $dvp/dovepass.found
fi
fi
done < /etc/dovecot/dovecot.passwd
echo "------------------- $(date) --------------------" >> $dvp/dovepass_found.log
cat $dvp/dovepass.found >> $dvp/dovepass_found.log
echo "---------------------------------------------------------------------" >> $dvp/dovepass_found.log
#if [ -s dovepass.found ]
#then
#mail -s "Dovecot pass file violation!!!" dmitry.lazuko@becloud.by < $dvp/dovepass.found
#fi
#rm -f dovepass.found   
