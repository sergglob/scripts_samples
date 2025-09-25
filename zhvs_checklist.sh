#!/bin/bash
crt_main () {
    echo -e "${BL}This is a checklist app for SHVS creation task.${NO}"
    echo -e "Please specify the task with Tech Support Service? ${RE}n${NO}(no=default), ${RE}y${NO}(yes)"
    read -n1 -s ts
    case $ts in
        'y')
        echo -e "${BL}Creating instance with Tech support${NO}"
        crt_env
        crt_vm
        ts_vm
        crt_back
        ts_back
        crt_tenant
        prnt_rep
        task
        ;;
        'n'|'')
        echo -e "${BL}Creating default instance${NO}"
        crt_env
        crt_vm
        crt_back
        crt_tenant
        prnt_rep
        task
        ;;
        *) 
        echo -e "${RE}Wrong input!${NO}"
        crt_main
        ;;
    esac
}

crt_vdc () {
    read -p "Enter the VM CPU core number: " cpu_n
    read -p "CPU core frequency GHz: " cpu_f
    cpu_a=`echo $cpu_n*$cpu_f | bc`
    read -p "RAM GB: " ram
    read -p "SSD GB: " ssd
    space=`echo $ram+$ssd | bc`
    read -p "Enter the client's access IPs: " allowed_ips
    echo -e "|-------------------- ${BL}The $ucn""_vdc params${NO} -------------------|"
    echo "|CPU frequency ($cpu_n cores by $cpu_f GHz) | $cpu_a GHz"
    echo "|RAM / SSD / RAM+SSD for VAPP         | $ram GB / $ssd GB / VDC storage $space GB"
    echo "|Allowed IPS: $allowed_ips"
    echo "|------------------------------------------------------------------------|"
}

crt_env () {
    echo -e "${BL}Follow the next list.${NO}"
    echo -e '---\n'
    read -p "Enter organization UCN vs shvs/_2 prefix, like shvs_123456789: " ucn
    echo -e '---\n'
    echo -e "${GR}1/8.${NO} Create VDC $ucn""_vdc . Press enter."
    read vdc
    echo "Registered: $ucn""_vdc"
    crt_vdc                         #VDC resources
    echo ''
    echo -e '---\n'
    echo -e "${GR}2/8.${NO} Create vapp $ucn""_vapp . Press enter."
    read vapp
    echo "Registered: $ucn""_vapp"
    echo ''
    echo -e '---\n'    
    echo -e "${GR}3/8.${NO} Create EDGE $ucn""_edge , input the external main IP: "
    read edge_ip
    echo "Registered: $ucn""_edge vs IP $edge_ip"
    echo "---------- EDGE hints -----------"
    echo "beCloud IPset: 93.125.20.142 185.32.224.178 93.125.20.158"
    echo "ISP manager IPset: 212.109.222.0/24 92.223.90.225/32 144.76.174.134/32"
    echo "TS only.Guacamole IP: 93.125.23.150"
    echo ""
    echo "Configure NAT (DNAT/SNAT or REFlexive: VM white-gray IP)"
    echo "Configure ipsets beCloud (any), client (ssh/ftp), in and out (80/443) for VM traffic  firewall rules "
    echo "---------------------------------"
    echo ""
    echo -e '---\n'
    echo -e "${GR}4/8.${NO} Create NETwork $ucn""_net , input VM gateway IP: "
    read gtw_ip
    echo "Registered: $ucn""_net and gateway IP $gtw_ip"
}
crt_vm () {
    echo -e '---\n'
    echo -e "${GR}5/8.${NO} Create VM. Input VM number, like 1 for vm01 (currently 10 and above will show vm010): "
    read vm
    echo ''
    echo "Registered: $ucn""_vm0$vm"
    echo ''
    echo "Enter VM OS brand and version: "
    read vm_os
    read -p "Enter VM gray IP: " gray_ip
#    echo ""
    read -p "Enter user password: " passwu
    read -p "Enter root password: " passwr
    echo ""
    read -r -p "Type ISP manager version, if installing: " isp
    echo ""
    echo "Install ISP panel: https://www.ispmanager.ru/docs/ispmanager/ustanovka "
    echo "Network config hint, nameservers: 93.125.22.110 93.125.22.108 8.8.8.8"
    echo ""
    echo -e "Add our ssh key in ~/.ssh/authorized_keys. Register ${RE}y${NO}/yes or ${RE}n${NO}/no."
    echo "###beCloud support"
    echo "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQC21m3nHQweM5iwipK67bnB0T+gDsvMi1HzJYPS8uY8W/WkYpaolnTs6luAl2pEI3RXMt0kcPHq2Ff0tNYWhGAgViA4WnqRijl8erJBQ2g5jexBkPC5LosFMlJBday40PM7tqZ1ka+2ccywsFeCzh1+NUYCw9TToDhszvMoZqa8neC8DS5LbGEOsMhpWP+TXw+Vo3os64BwXg6tiBsXLX8qSNuagj5gRrGaVzHmD8BbE5L24sK+oIaRzAqytOwbFAcFL4NqOHxCTrrQ93uGNV4W0Jum4PijtFSaJiACUpjYd06yZT7pOcLV17fi//e13JAwqdf7xGERiGLjL3X8iiGSOnToJPs1FYepuOnmfXkCvhHCG2J6GoMKYBKC00ISaNSTSE8kZLsLixtfie/izCi8sVHJ8hu2fsUKYczPokFsvU6qujqTtmNCKsF6yIzf6rvseFTrBkZqEQTzlJuumNjFNqvV0zEqaSKUISIBe49RcGpq00TsLWhAPkeektGxdpc= becloud_itrp2025"
    read -n1 ssh
    echo ''
    echo -e "Install open-vm-tools. Register ${RE}y${NO}/yes or ${RE}n${NO}/no."
    read -n1 ovm
    echo ''
    echo -e "Stop VM. Unmount installation image. Register ${RE}y${NO}/yes or ${RE}n${NO}/no."
    read -n1 im
    echo ''
    echo -e "Stop VM. Activate hot add CPU/RAM.  Register ${RE}y${NO}/yes or ${RE}n${NO}/no."
    read -n1 hot
    echo ''
    echo -e "Configure VM audit.  Register ${RE}y${NO}/yes or ${RE}n${NO}/no."
    echo "ssh root@$edge_ip  'sh -s' < audit_c.sh  | tee $edge_ip.txt"
    read -n1 aud
    echo ''
}


crt_back () {
    echo -e '---\n'
    echo -e "${GR}6/8.${NO} Create the backup $ucn""_vm0$vm"
    echo "Rule: store 31 day, run once a week, preferable Fri, Sut, Sun at 18-22 o'clock range'"
    echo -e "Open ${BL}https://cloud.becloud.by/tenant/Hosting/${NO} or ${BL}https://cloud.becloud.by/tenant/Hosting_2/${NO} accordingly"
    echo -e "Have you launched the backup manually? Register ${RE}y${NO}/yes or ${RE}n${NO}/no."
    read -n1 nt_launched
    echo ''
    echo -e "Notify veeam admin about the : $ucn""_vm0$vm"" job. Register ${RE}y${NO}/yes or ${RE}n${NO}/no." 
    read -n1 nt_veeam
    echo ''
}

crt_tenant () {
    echo -e '---\n'
    echo -e "${GR}7/8.${NO} Create the service record on tenant."
    u=`echo $ucn | sed 's/.*_//'`
    echo -e "Open ${BL}https://tenant2.g-cloud.by/client/tmp/?name=$u${NO}"
    echo "VDC on DSP_GOV $ucn""_vdc"
    echo "VM name: $ucn""_vm0$vm"
    echo "VM CPU number: $cpu_n"
    echo "VM RAM in MB: `echo $ram*1024 | bc`"
    echo "user password:" $passwu
    echo "root password:" $passwr
    echo "VM SSD in GB: $ssd"
    echo "Public IP: $edge_ip"
    echo "Gray IP: $gray_ip"
    echo "ISP manager: $isp"
    echo -e "Register tenant info ${RE}y${NO}/yes or ${RE}n${NO}/no."
    read -n1 ten
    echo ''
}

prnt_rep () {
    echo -e '---\n'
    echo -e "${GR}8/8.${NO} Send email/SMS to client."
    echo -e "--------------------------------------- ${BL}Message to client${NO} ----------------------------------------------------"
    echo -e "Уважаемый пользователь, вам предоставлен доступ к услуге «Защищённый хостинг на виртуальном сервере». \n
    Конфигурация сервера $ucn""_vm0$vm: $cpu_n CPU с частотой $cpu_f, $ram GB RAM, $ssd GB HDD, OS $vm_os. \n
    Адрес сервера: $edge_ip \n
    Открытые порты для мира: 80, 443. \n
    Открытые порты для авторизованных IP: 21, 22. \n
    Доступ к серверу осуществляется по SSH с авторизованных IP-адресов: \n
    $allowed_ips\n
    Логин: user \n
    Пароль: $passwu\n
    Привилегии root (su или sudo su): \n
    Пароль: $passwr\n
    Установлена панель ISP Manager, версия: $isp\n
    Доступ к панели ISP для разрешенных IP: http://$edge_ip:1500 под root"
    
    echo "--------------------------------------------------------------------------------------------------------------"
    echo -e "Register ${RE}y${NO}/yes or ${RE}n${NO}/no."
    read -n1 rep
}

ts_vm () {
    echo -e "Install Zabbix, hint: zabbix server / active server IP: 195.50.9.227. Register ${RE}y${NO}/yes or ${RE}n${NO}/no."
    read -n1 zab
    echo ''
}

ts_back () {
    echo -e "Create TS task $ucn""_vm0$vm""_TS . Register ${RE}y${NO}/yes or ${RE}n${NO}/no."
    echo "Rule: store 4 copies, run each day"
    echo -e "Have you launched the TS backup manually? Register ${RE}y${NO}/yes or ${RE}n${NO}/no."
    read -n1 ts_launched
    echo ''
    echo -e "Notify veeam admin about the : $ucn""_vm0$vm""_TS job. Register ${RE}y${NO}/yes or ${RE}n${NO}/no." 
    read -n1 ts_veeam
    echo ''
}

task () {
    echo "###############################################################################################"
    echo -e "${BL}Task summary.${NO} Created items:"
    echo "|---------------------------------------------------------|"
    echo -e "| ${GR}Infrastructure${NO} -----------------------------------------|"
    echo "| VDC: $ucn""_vdc |"
    echo -e "| VAPP: $ucn""_vapp, hot add activated: ${RE}$hot${NO}, image unmounted: ${RE}$im${NO} |"
    echo "| EDGE: $ucn""_edge, public IP: $edge_ip |"
    echo "| NET: $ucn""_net, CIDR: $gtw_ip |"
    echo -e "| ${GR}$ucn""_vm0$vm  params${NO} --------------------------------|"
    echo "| CPU frequency ($cpu_n cores by $cpu_f GHz): $cpu_a GHz |"
    echo "| RAM $ram GB, SSD $ssd GB |"
    echo "| Gray IP: $gray_ip |"
    echo -e "| OS version: ${RE}$vm_os${NO} |"
    echo -e "| ISP manager installed: ${RE}$isp${NO} |"
    echo -e "| SSH key added: ${RE}$ssh${NO}, OVM tools installed: ${RE}$ovm${NO} |"
    echo -e "| TS task. Zabbix installed: ${RE}$zab${NO} |"
    echo -e "| ${GR}Backup params${NO} ------------------------------------------|"
    echo -e "| Backup task $ucn""_vm0$vm launched: ${RE}$nt_launched${NO}, veeam specialist notified: ${RE}$nt_veeam${NO} |"
    echo -e "| TS Backup task $ucn""_vm0$vm""_TS launched: ${RE}$ts_launched${NO}, veeam specialist notified: ${RE}$ts_veeam${NO} |"
    echo -e "| VM audit configured: ${RE}$aud${NO} |"
    echo -e "| ${GR}Tenant params and client informing${NO} ----------------------|"
    echo -e "| Service record on tenant created: ${RE}$ten${NO} |"
    echo -e "| Email/SMS sent to client: ${RE}$rep${NO} |"
    echo "|---------------------------------------------------------|"
    echo "###############################################################################################"
    echo -e "${RE}Skript work completed!${NO}"
}
NO='\033[0m'
BL='\033[0;34m'
RE='\033[0;31m'
GR='\033[0;32m'
crt_main | tee /home/serg/Downloads/`date +"%m-%d-%H:%M"`.zhvs
