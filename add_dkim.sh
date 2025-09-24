#!/bin/bash
get_dom_without_dkim () {
echo '--------------------- getting domains list without DKIM --------------------------'
#get domains list without DKIM enabled
echo "-----### $(date) ###-----" >> domains_old
cat domains >> domains_old
rm -f gcloud_dkim send_dkim not_found dkim.zip #remove old files
/usr/local/mgr5/sbin/mgrctl -m ispmgr emaildomain | grep -v "dkim=" | awk -F 'name=' '{print$2}' | awk -F ' ' '{print$1}' > domains
}

enable_dkim() {
#enabling DKIM for the domains found
echo '--------------------- enabling DKIM for the domains found --------------------------'
while read line
do
echo "Enabling DKIM for $line"
/usr/local/mgr5/sbin/mgrctl -m ispmgr emaildomain.edit dkim=on dkim_keylen=2048 elid=$line sok=ok
done < domains
}
#DEPRECATED!!!! collecting DKIM records from /etc/exim/ssl
#while read line
#do
#cat /etc/exim/ssl/$line | tee -a gcloud_dkim
#done < domains

rep_dkim() {
#collecting DKIM records
echo '--------------------- collecting DKIM records for the domains found --------------------------'
while read line
do
dom=$(/usr/local/mgr5/sbin/mgrctl -m ispmgr domain.record elid=$line | grep "rkey=dkim._domainkey" | awk -F ' rkey_name' '{print$1}')
dkim=$(echo $dom | awk -F ' TXT ' '{print$2}')
nslookup -type=ns $line | grep "g-cloud.by" > ns_check
if [ ! -s "ns_check" ]
then
    echo "$line NOT on our NS"
    echo "nslookup -type=ns $line"
    nslookup -type=ns $line | grep "server can't find" > not_check
    if [ ! -s "not_check" ]
    then
    echo "---------------------------------------------------------------------- $line --------------------------------------------------------------------" | tee -a send_dkim
    echo $(nslookup -type=ns $line) | tee -a send_dkim
    echo "===========================================" | tee -a send_dkim
    echo "Добрый день.

Для повышения безопасности электронных отправлений на всех почтовых доменах услуги услуги «Электронная почта. Light» осуществляется проверка DKIM-записи (DomainKeys Identified Mail). Данная проверка позволяет проверить, что домен отправителя подлинный и почтовые сообщения приходят именно от него. Это стандарт защиты электронной почты и метод обнаружения подделки электронных писем.


При получении уведомления в теме письма о нарушении подлинности отправителя (DKIM), необходимо на удаленном почтовом сервере создать DKIM-запись и разместить ее в доменной зоне.

Тип DNS записи: TXT
Имя: dkim._domainkey.$line.
Запись: $dkim
TTL: 3600


При невозможности создать DKIM-запись на сервере отправителя, рекомендуем создать в личном кабинете Общества запрос и указать ip-адрес сервера для добавления его в исключение проверки DKIM.

Также просьба проверить наличие DMARC и SPF DNS-записей:

Тип DNS записи: TXT
Имя:  $line.
Запись: v=spf1 include:_spf.g-cloud.by +a +mx -all
TTL: 3600

Тип DNS записи: TXT
Имя:  _dmarc.$line.
Запись: v=DMARC1; p=reject; aspf=s
TTL: 3600

Обращаем ваше внимание, что для работы почтовых отправлений, может присутствовать только одна  SPF DNS-запись.
Если для вашего доменного имени имеется несколько записей данного типа, просьба удалить все другие записи, оставив только запись:

Тип DNS записи: TXT
Имя:  $line.
Запись: v=spf1 include:_spf.g-cloud.by +a +mx -all
TTL: 3600" >> send_dkim
    echo "################################################################################################################################################" | tee -a send_dkim
###
    else
    echo "$line NOT FOUND!" | tee -a "not_found"
    fi
else
    echo "$line on our NS, add DKIM: "
    echo "---------------------------------------------------------------------- $line --------------------------------------------------------------------" | tee -a gcloud_dkim
    echo "Тип DNS записи: TXT
    Имя: dkim._domainkey.$line.
    Запись: $dkim
    TTL: 3600" >> gcloud_dkim
fi
done < domains
echo "========================================================================================================="
echo "gcloud_dkim - contains domain dkims on our NS, add dkims for the domains on https://ns1.g-cloud.by:1501/"
echo "send_dkim - contains EMAIL body to send for users, whose domain records not on our NS"
echo "not_found - contains domains without records"
echo "dkim.zip - archive gcloud_dkim, send_dkim"
echo "========================================================================================================="
}

get_dom_without_dkim
enable_dkim
rep_dkim
zip -r dkim.zip gcloud_dkim send_dkim
rm -f not_check ns_check # clear trash
