#!/bin/bash
read -p "INT: " int
read -p "ORG: " org
read -p "PERSON: " psn
read -p "PHONE: " phn
read -p "EMAIL: " eml
read -p "PASSWORD: " pwd
read -s -n1 -p "If all OK - press any key to send"
echo ""
curl -k --location "https://smsgate.becloud.by/send_sms_message_with_token/" --header "Token: apikey Ainga8yo@raezahwuu-hieK" --form "client_name=$org" --form "phone_numbers=$phn" --form "contact_person=$psn" --form "content=Добрый день! Почтовый ящик $eml разблокирован. Высылаем в Ваш адрес реквизиты доступа. Просьба не сообщать пароль посторонним лицами и изменить при первом подключении. Пароль к почтовому ящику: $pwd" --form "comments=Внутренняя задача $int"
