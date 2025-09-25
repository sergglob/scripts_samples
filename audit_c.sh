#!/bin/bash
#cat  /etc/profile
#cat /home/issp/.ssh/authorized_keys
#cat /etc/audit/auditd.conf | grep log_format
#cat /usr/lib/systemd/system/auditd.service | grep RefuseManualStop
#or
##cat /lib/systemd/system/auditd.service | grep RefuseManualStop
#cat /etc/rsyslog.conf | grep "local5"
#cat /etc/rsyslog.d/50-becloud.conf
#service auditd status
#service rsyslog status

os_info () {
#echo `curl ifconfig.me`
echo `cat  /etc/os-release`
echo "-----"
echo `hostnamectl`
echo "-----"
}
profile () {
    l=$(cat /etc/profile|grep "Loggining script")
    if [ -z $l ]
    then
    echo "   #####Loggining script
   IP=\$(who am i|awk '{print \$5}'| sed 's/[(,)]//g')
   logger -p user.crit -t \"bash \$LOGNAME \$\$\" User \$LOGNAME logged from \$IP
   PREF=\"user_log\"
   function h2log
   {
	   declare CMD
	   declare _PWD
	   CMD=\$(history 1)
	   CMD=\$(echo \$CMD| awk '{print substr(\$0,length(\$1)+2)}')
	   _PWD=\$(pwd)
	   if [ \"\$CMD\" != \"\$pCMD\" ]; then
   	   logger -p user.crit -t bash -i -- \"\${PREF} : SESSION=\$\$ : \${IP} : \${USER} : \${_PWD} : \${CMD}\"
  	   fi
 	    pCMD=\$CMD
    }
    trap h2log DEBUG || EXIT
   #########" >> /etc/profile
    else
    echo "${YE}Logging script already applied! Skipping ...${NO}"
    fi
}

local5 () {
    if [ -f /etc/rsyslog.d/50-default.conf ]
    then
    echo "${BL}Adding local5.none into 50-default.conf${NO}"
    z=$(cat /etc/rsyslog.d/50-default.conf | grep "\-/var/log/messages")
    x=$(cat /etc/rsyslog.d/50-default.conf | grep "\-/var/log/syslog")
    zz=$(echo $z|sed 's/ //g' | sed 's|-\/var/log/messages||')
    xx=$(echo $x|sed 's/ //g' | sed 's|-\/var/log/syslog||')
    zzz=$zz";local5.none"
    xxx=$xx";local5.none"
    sed -i s/${zz}/${zzz}/ /etc/rsyslog.d/50-default.conf
    sed -i s/${xx}/${xxx}/ /etc/rsyslog.d/50-default.conf
#
    a=$(cat /etc/rsyslog.d/50-default.conf | grep "/var/log/messages")
    b=$(cat /etc/rsyslog.d/50-default.conf | grep "/var/log/syslog")
    aa=$(echo $a|sed 's/ //g' | sed 's|/var/log/messages||')
    bb=$(echo $b|sed 's/ //g' | sed 's|/var/log/syslog||')
    aaa=$aa";local5.none"
    bbb=$bb";local5.none"
    sed -i s/${aa}/${aaa}/ /etc/rsyslog.d/50-default.conf
    sed -i s/${bb}/${bbb}/ /etc/rsyslog.d/50-default.conf
    else
    echo "${BL}Adding local5.none into rsyslog.conf${NO}"
    z=$(cat /etc/rsyslog.conf | grep "\-/var/log/messages")
    x=$(cat /etc/rsyslog.conf | grep "\-/var/log/syslog")
    zz=$(echo $z|sed 's/ //g' | sed 's|-\/var/log/messages||')
    xx=$(echo $x|sed 's/ //g' | sed 's|-\/var/log/syslog||')
    zzz=$zz";local5.none"
    xxx=$xx";local5.none"
    sed -i s/${zz}/${zzz}/ /etc/rsyslog.conf
    sed -i s/${xx}/${xxx}/ /etc/rsyslog.conf
#
    a=$(cat /etc/rsyslog.conf | grep "/var/log/messages")
    b=$(cat /etc/rsyslog.conf | grep "/var/log/syslog")
    aa=$(echo $a|sed 's/ //g' | sed 's|/var/log/messages||')
    bb=$(echo $b|sed 's/ //g' | sed 's|/var/log/syslog||')
    aaa=$aa";local5.none"
    bbb=$bb";local5.none"
    sed -i s/${aa}/${aaa}/ /etc/rsyslog.conf
    sed -i s/${bb}/${bbb}/ /etc/rsyslog.conf
    fi
}
oib () {
if [ -f /home/issp/.ssh/authorized_keys ]
then
    echo "${YE}issp ssh key exists! Skipping...${NO}"
else
    #centos
    useradd -m -G wheel,root -s /bin/bash issp || true
    echo "${BL}Adding ISSP user into wheel group${NO}"
    sed -i 's/^%wheel/#&/' /etc/sudoers || true
    echo '%wheel ALL=(ALL) NOPASSWD: ALL' >> /etc/sudoers || true

    #ubuntu/debian
    sudo useradd -m -G sudo,root -s /bin/bash issp || true
    echo "${BL}Adding ISSP user into sudo group${NO}"
    sed -i 's/^%sudo/#&/' /etc/sudoers || true
    echo '%sudo ALL=(ALL) NOPASSWD: ALL' >> /etc/sudoers || true

    #import OIB ssh key
    mkdir -p /home/issp/.ssh
    chmod 700 /home/issp/.ssh
    echo "${BL}Inserting ISSP ssh key${NO}"
    echo 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQC+68S1fyM07r/CQv6nr8YgpO/Bikk7B8pNGsoZvfgjTNaLXXO07ipQ56YD/+uKx72DbLAbZP9P73auUPm++zJWYMza4wGtEUEzzGhc8GtUH0TJGONbgomo95V1uyNj1DA7eR+BS+NsRTfvaaBiKf8KEL0Y9bp4BX28il9JgNexmZ4am+gwO4PwYAct4+WXVJoVioNVDQmd17MZ1RSZzAeqLcwQXWsxGwqui2YgogJKotMU1Q0P2AtKGM0PN4dY20Dg0m+GYccF2uEGBUyK1L/32m87As/ymN9s+VMXgSAoRIqVmoAbJVNvL7gOPrmsDi8ngSpzYmam3H4Ky5lYzrvj+XKrH1kWk1Nh84McYIFFdUzSp5LWyQHjPG1bjNbRFDXSPbyjIO+VVnb/cyNw97ZjTySwJdAOw70cOq17KsaefnNoU+pqdqvMkMVfcDDE8jh5ga059lMETZfQZyH7WHmHS4emCxc+qS6Lya49yfmoGDOfERBMI8/+Ofni4eDLX6wHABcZJvcPPlffrUpxFWi94l1VI7nVMn2Ei6Ob4JHhesyeL9QWPemnKMMjzEc1ByphreLVcrLCFE8uYZJkqK0sv6mKRCCPTUXzAANt1e7Ju6TI7L/VKntuH9r9XbODnRrc4DBKQzPLAZUxos0wyARMhvURbsB6Wf/36x3OYwy2fQ== issp' >> /home/issp/.ssh/authorized_keys
    chmod 600 /home/issp/.ssh/authorized_keys
    chown -R issp:issp /home/issp/.ssh

    #aliases
    echo "${BL}Adding aliases into ISSP bashrc${NO}"
    bash -c "cat << 'EOF' >> /home/issp/.bashrc
    alias netstat='sudo netstat'
    alias nginx='sudo nginx'
    alias grep='sudo grep'
    alias xargs='sudo xargs'
    alias netstat='sudo ss'
    EOF"
    sudo -u issp bash -c "source /home/issp/.bashrc"
fi
}

audit () {
    if [ -f /etc/rsyslog.conf ]
    then
    echo "${YE}rsyslog.conf exists! Skipping installation ...${NO}"
    else
    apt update || true
    yum update || true
    apt-get install rsyslog -y || true
    yum install rsyslog -y || true
    systemctl enable rsyslog
    systemctl start rsyslog
    fi
    if [ -f /etc/audit/auditd.conf ]
    then
    echo "${YE}auditd.conf exists! Skipping app installation...${NO}"
    echo "${BL}Configuring auditd service${NO}"
    aud_rules
    aud_conf
    elif [ -f /etc/audit/audit.conf ]
    then
    echo "${YE}audit.conf exists! Skipping app installation...${NO}"
    echo "${BL}Configuring audit service${NO}"
    aud_rules
    aud_conf
    else
    yum update || true
    yum install audit -y || true
    apt update || true
    apt install auditd -y || true
    echo "${BL}Configuring audit service${NO}"
    aud_rules
    aud_conf
    echo "${BL}Configuring rsyslog 50-becloud.conf${NO}"
    fi    
    if [ -f /etc/rsyslog.d/50-becloud.conf ]
    then
    echo "${YE}50-becloud.conf exists! Skipping...${NO}"
    else
    echo "${BL}Switching RefuseManualStop=no${NO}"
    sed -i 's/RefuseManualStop=yes/RefuseManualStop=no/' /usr/lib/systemd/system/auditd.service
    sed -i 's/RefuseManualStop=yes/RefuseManualStop=no/' /lib/systemd/system/auditd.service
    sleep 3
    systemctl daemon-reload
    sleep 3
    systemctl restart auditd.service
    echo "${BL}Switching back RefuseManualStop=yes${NO}"
    sed -i 's/RefuseManualStop=no/RefuseManualStop=yes/' /usr/lib/systemd/system/auditd.service
    sed -i 's/RefuseManualStop=yes/RefuseManualStop=yes/' /lib/systemd/system/auditd.service
    sleep 3
    systemctl daemon-reload
    rsys_mod
    local5
    echo "${BL}Adding syslog02.g-cloud.by:514 into rsyslog.conf${NO}"
    echo "*.* @syslog02.g-cloud.by:514" >> /etc/rsyslog.conf
    echo "${BL}Forming 50-becloud.conf${NO}"
    echo "input(type=\"imfile\"
    file=\"/var/log/audit/audit.log\"
    Facility=\"local5\"
    tag=\"audit:\"
    reopenOnTruncate=\"on\"
    )" > /etc/rsyslog.d/50-becloud.conf
    if [ -d /var/www/httpd-logs/ ]
    then
    echo "${GR}httpd-logs folder - found!${NO}"
    echo "${GR}Probably ISP system, adding syslog user to default www-root group${NO}"
    usermod -a -G www-root syslog
    for file in /var/www/httpd-logs/*log; do
    filename=$(basename "$file" | sed -e 's/\.log//g')
    echo "input(type=\"imfile\"
    file=\"$file\"
    Facility=\"local5\"
    tag=\"$filename:\"
    reopenOnTruncate=\"on\"
    )" >> /etc/rsyslog.d/50-becloud.conf
    done
    else
    echo "${YE}no folder - httpd-logs${NO}"
    fi
    if [ -d /var/log/httpd/ ]
    then
    echo "${GR}httpd folder - found!${NO}"
    echo "input(type=\"imfile\"
    file=\"/var/log/httpd/*log\"
    Facility=\"local5\"
    tag=\"web-httpd:\"
    reopenOnTruncate=\"on\"
    )" >> /etc/rsyslog.d/50-becloud.conf
    else
    echo "${YE}no folder - httpd${NO}"
    fi
    if [ -d /var/log/apache2/ ]
    then
    echo "${GR}apache2 folder - found!${NO}"
    echo "input(type=\"imfile\"
    file=\"/var/log/apache2/*log\"
    Facility=\"local5\"
    tag=\"web-apache:\"
    reopenOnTruncate=\"on\"
    )" >> /etc/rsyslog.d/50-becloud.conf
    else
    echo "${YE}no folder - apache2${NO}"
    fi
    if [ -d /var/log/nginx/ ]
    then
    echo "${GR}nginx folder - found!${NO}"
    echo "input(type=\"imfile\"
    file=\"/var/log/nginx/*log\"
    Facility=\"local5\"
    tag=\"web-nginx:\"
    reopenOnTruncate=\"on\"
    )" >> /etc/rsyslog.d/50-becloud.conf 
    else
    echo "${YE}no folder - nginx${NO}"
    fi
    sleep 3
    service rsyslog stop
    sleep 3
    service rsyslog start
    fi
}
aud_conf () {
    echo "${BL}Switching auditd.conf log_format=ENRICHED${NO}"
    if [ -f /etc/audit/auditd.conf ]
    then
    sed -i 's/log_format = RAW/log_format = ENRICHED/' /etc/audit/auditd.conf
    elif [ -f /etc/audit/audit.conf ]
    then
    sed -i 's/log_format = RAW/log_format = ENRICHED/' /etc/audit/audit.conf
    else
    echo "${YE}/etc/audit/audit*config not found!${NO}"
    fi
}
rsys_mod () {
    echo "${BL}Adding imfile mode into rsyslog.conf${NO}"
    c=$(cat /etc/rsyslog.conf|grep \"| head -1)
    if [ -z $c ]
    then
    sed -i 's/#### MODULES ####/#### MODULES ####\n$ModLoad imfile/' /etc/rsyslog.conf
    else
    sed -i 's/#### MODULES ####/#### MODULES ####\nmodule(load="imfile")/' /etc/rsyslog.conf
    fi
}

report () {
echo "${GR}1) Checking /etc/profile${NO}"
echo "${YE}(ok if Loggining script record found)${NO}"
cat  /etc/profile | grep -i "Loggining script"
echo ""
echo "${GR}2) Checking issp user key (ok if file found)${NO}"
ls /home/issp/.ssh/authorized_keys
echo ""
echo "${GR}3) Checking auditd.conf file ${NO}"
echo "${YE}(ok if file found, ok if log_format record found)${NO}"
ls /etc/audit/auditd.conf
cat /etc/audit/auditd.conf | grep log_format
echo ""
echo "${GR}4) Checking auditd.service file and record RefuseManualStop expected${NO}"
echo "${YE}(but can be missing due to the specific audit version), checking audit rules${NO}"
if [ -f /etc/audit/auditd.conf ]
then
ls /lib/systemd/system/auditd.service
cat /lib/systemd/system/auditd.service | grep RefuseManualStop
else
ls /usr/lib/systemd/system/auditd.service
cat /usr/lib/systemd/system/auditd.service | grep RefuseManualStop
fi
echo "auditctl -l status (bad if No rules, try move /etc/audit/audit.rules into /etc/audit/audit.d/ or into /etc/audit/rules.d/ ):"
echo "-----"
auditctl -l | head -1
echo ""
echo "${GR}5) Checking rsyslog.conf local5 records and 50-becloud.conf${NO}"
echo "${YE}(ok if local5.none records found)${NO}"
echo ""
echo "rsyslog.conf:"
cat /etc/rsyslog.conf | grep "local5"
echo "50-default.conf:"
cat /etc/rsyslog.d/50-default.conf | grep "local5"
echo "-----"
cat /etc/rsyslog.d/50-becloud.conf
echo ""
echo "${GR}6) Checking audit service status and errors${NO}"
echo "${YE}(augenrules[XXXX]: failure 1 can be ignored, PAY ATTENTION on service running time to be sure it was restarted)${NO}"
echo "${YE}In case of other error - try to back auditd.conf log_format=RAW (ENRICHED not supported issue)${NO}"
echo "-----"
sleep 3
service auditd status | grep -i Active
echo "checking errors"
echo "-----"
sleep 3
service auditd status | grep -i erro
sleep 3
service auditd status | grep -i fail
echo ""
echo "${GR}7) Checking rsyslog service status and errors ${NO}"
echo "${YE}(omfwd: error can be ignored / autofix in a minute, log file access forbidden - chmod 664 for log files and restart rsyslog)${NO}"
echo "${YE}PAY ATTENTION on service running time to be sure it was restarted${NO}"
echo "${YE}on Ubuntu + ISP manager you can also try to add syslog to ISP user's sites group':  usermod -a -G <site_user_group> syslog${NO}"
echo "-----"
sleep 3
service rsyslog restart
sleep 7
service rsyslog status | grep -i Active
echo "checking errors"
echo "-----"
sleep 3
service rsyslog status | grep -i erro
sleep 3
service rsyslog status | grep -i fail
sleep 3
echo ""
echo "${GR}8) Checking logs data availability${NO}"
for i in $(cat /etc/rsyslog.d/50-becloud.conf | grep file| grep -v imfile| awk -F '"' '{print $2}')
do
echo "---$i---"
tail -n 3 $i
echo ""
done
echo ""
}
aud_rules () {
if [ -f /etc/audit/rules.d/becloud.rules ]
then
echo "${YE}becloud.rules exists! Skipping...${NO}"
else
echo "-D
-b 8192
-f 1
-i
-w /var/log/audit/ -p wra -k auditlog
-w /var/audit/ -p wra -k auditlog
-w /etc/audit/ -p wa -k auditconfig
-w /etc/libaudit.conf -p wa -k auditconfig
-w /etc/audisp/ -p wa -k audispconfig
-w /sbin/auditctl -p x -k audittools
-w /sbin/auditd -p x -k audittools
-w /usr/sbin/auditd -p x -k audittools
-w /usr/sbin/augenrules -p x -k audittools
-a always,exit -F path=/usr/sbin/ausearch -F perm=x -k audittools
-a always,exit -F path=/usr/sbin/aureport -F perm=x -k audittools
-a always,exit -F path=/usr/sbin/aulast -F perm=x -k audittools
-a always,exit -F path=/usr/sbin/aulastlogin -F perm=x -k audittools
-a always,exit -F path=/usr/sbin/auvirt -F perm=x -k audittools
-a never,exclude -F uid=zabbix 
-a never,exclude -F auid=4294967295
-a never,exclude -F msgtype=CWD
-a never,user -F subj_type=crond_t
-a never,exit -F subj_type=crond_t
-w /sbin/shutdown -p x -k power
-w /sbin/poweroff -p x -k power
-w /sbin/reboot -p x -k power
-w /sbin/halt -p x -k power
-w /usr/bin/dpkg -p x -k software_mgmt
-w /usr/bin/apt -p x -k software_mgmt
-w /usr/bin/apt-add-repository -p x -k software_mgmt
-w /usr/bin/apt-get -p x -k software_mgmt
-w /usr/bin/aptitude -p x -k software_mgmt
-w /usr/bin/wajig -p x -k software_mgmt
-w /usr/bin/snap -p x -k software_mgmt
-w /usr/bin/rpm -p x -k software_mgmt
-w /usr/bin/yum -p x -k software_mgmt
-w /usr/bin/dnf -p x -k software_mgmt
-w /sbin/yast -p x -k software_mgmt
-w /sbin/yast2 -p x -k software_mgmt
-w /bin/rpm -p x -k software_mgmt
-w /usr/bin/zypper -k software_mgmt
-a always,exit -F arch=b64 -S open -F dir=/etc -F success=0 -k unauthedfileaccess
-a always,exit -F arch=b64 -S open -F dir=/bin -F success=0 -k unauthedfileaccess
-a always,exit -F arch=b64 -S open -F dir=/sbin -F success=0 -k unauthedfileaccess
-a always,exit -F arch=b64 -S open -F dir=/usr/bin -F success=0 -k unauthedfileaccess
-a always,exit -F arch=b64 -S open -F dir=/usr/sbin -F success=0 -k unauthedfileaccess
-a always,exit -F arch=b64 -S open -F dir=/var -F success=0 -k unauthedfileaccess
-a always,exit -F arch=b64 -S open -F dir=/home -F success=0 -k unauthedfileaccess
-a always,exit -F arch=b64 -S open -F dir=/srv -F success=0 -k unauthedfileaccess
-w /var/run/utmp -p wa -k session
-w /var/log/btmp -p wa -k session
-w /var/log/wtmp -p wa -k session
-w /bin/su -p x -k priv_esc
-w /usr/bin/sudo -p x -k priv_esc
-w /etc/sudoers -p wa -k priv_esc
-w /etc/sudoers.d/ -p wa -k priv_esc
-w /etc/group -p wa -k accounts
-w /etc/passwd -p wa -k accounts
-w /etc/gshadow -k accounts
-w /etc/shadow -k accounts
-w /etc/security/opasswd -k accounts
-w /usr/bin/passwd -p x -k passwd
-w /usr/sbin/groupadd -p x -k group_modification
-w /usr/sbin/groupmod -p x -k group_modification
-w /usr/sbin/addgroup -p x -k group_modification
-w /usr/sbin/useradd -p x -k user_modification
-w /usr/sbin/userdel -p x -k user_modification
-w /usr/sbin/usermod -p x -k user_modification
-w /usr/sbin/adduser -p x -k user_modification
-w /etc/cron.allow -p wa -k cron
-w /etc/cron.deny -p wa -k cron
-w /etc/cron.d/ -p wa -k cron
-w /etc/cron.daily/ -p wa -k cron
-w /etc/cron.hourly/ -p wa -k cron
-w /etc/cron.monthly/ -p wa -k cron
-w /etc/cron.weekly/ -p wa -k cron
-w /etc/crontab -p wa -k cron
-w /var/spool/cron/ -p wa -k cron
-w /usr/bin/crontab -p x -k cron
-w /bin/systemctl -p x -k systemd
-w /etc/systemd/ -p wa -k systemd
-w /usr/lib/systemd -p wa -k systemd
-a always,exit -F path=/usr/sbin/service -F perm=x -k service
-w /usr/bin/service -p x -k service
-w /etc/ssh/sshd_config -k sshd
-w /etc/ssh/sshd_config.d -k sshd
-a always,exit -F arch=b64 -S sethostname -S setdomainname -k network
-w /etc/hostname -p wa -k network
-w /etc/hosts -p wa -k network
-w /etc/network/ -p wa -k network
-w /etc/NetworkManager/ -p wa -k network
-w /etc/sysconfig/network -p wa -k network
-w /sbin/iptables -p x -k network
-w /sbin/ip6tables -p x -k network
-w /sbin/ifconfig -p x -k network
-w /usr/sbin/arptables -p x -k network
-w /usr/sbin/ebtables -p x -k network
-w /sbin/xtables-nft-multi -p x -k network
-w /usr/sbin/nft -p x -k network
-w /usr/sbin/tcpdump -p x -k network
-w /usr/sbin/traceroute -p x -k network
-w /usr/sbin/ufw -p x -k network
-w /etc/netplan/ -p wa -k network
-w /usr/sbin/netplan -p x -k network
-w /sbin/ip -p x -k network
-w /usr/sbin/ufw -p x -k ufw
-w /usr/sbin/nft -p x -k nftables
-w /etc/sysctl.conf -p wa -k sysctl
-w /etc/sysctl.d -p wa -k sysctl
-w /usr/sbin/stunnel -p x -k stunnel
-w /usr/bin/stunnel -p x -k stunnel
-w /etc/inittab -p wa -k init
-w /etc/init.d/ -p wa -k init
-w /etc/init/ -p wa -k init
-a always,exit -F perm=x -F auid!=-1 -F path=/sbin/insmod -k modules
-a always,exit -F perm=x -F auid!=-1 -F path=/sbin/modprobe -k modules
-a always,exit -F perm=x -F auid!=-1 -F path=/sbin/rmmod -k modules
-a always,exit -F arch=b64 -S finit_module -S init_module -S delete_module -F auid!=-1 -k modules
-w /etc/modprobe.conf -p wa -k modprobe
-w /etc/modprobe.d -p wa -k modprobe
-a always,exit -F arch=b64 -S kexec_load -k kexec
-w /etc/localtime -p wa -k localtime
-w /usr/sbin/setenforce -p x -k selinux
-w /usr/sbin/sestatus -p x -k selinux
-w /usr/bin/chcon -p x -k selinux
-w /usr/sbin/restorecon -p x -k selinux
-w /etc/selinux/ -p wa -k selinux
-w /sbin/apparmor_parser -p x -k apparmor
-w /usr/sbin/aa-status -p x -k apparmor
-w /usr/sbin/aa-enforce -p x -k apparmor
-w /usr/sbin/aa-complain -p x -k apparmor
-w /etc/apparmor/ -p wa -k apparmor
-w /etc/apparmor.d/ -p wa -k apparmor
-w /etc/pam.d/ -p wa -k pam
-w /etc/security/limits.conf -p wa  -k pam
-w /etc/security/limits.d -p wa  -k pam
-w /etc/security/pam_env.conf -p wa -k pam
-w /etc/security/namespace.conf -p wa -k pam
-w /etc/security/namespace.d -p wa -k pam
-w /etc/security/namespace.init -p wa -k pam
-a always,exit -F arch=b64 -S chmod  -F auid>=1000 -F auid!=-1 -k perm_mod
-a always,exit -F arch=b64 -S chown -F auid>=1000 -F auid!=-1 -k perm_mod
-a always,exit -F arch=b64 -S fchmod -F auid>=1000 -F auid!=-1 -k perm_mod
-a always,exit -F arch=b64 -S fchmodat -F auid>=1000 -F auid!=-1 -k perm_mod
-a always,exit -F arch=b64 -S fchown -F auid>=1000 -F auid!=-1 -k perm_mod
-a always,exit -F arch=b64 -S fchownat -F auid>=1000 -F auid!=-1 -k perm_mod
-a always,exit -F arch=b64 -S fremovexattr -F auid>=1000 -F auid!=-1 -k perm_mod
-a always,exit -F arch=b64 -S fsetxattr -F auid>=1000 -F auid!=-1 -k perm_mod
-a always,exit -F arch=b64 -S lchown -F auid>=1000 -F auid!=-1 -k perm_mod
-a always,exit -F arch=b64 -S lremovexattr -F auid>=1000 -F auid!=-1 -k perm_mod
-a always,exit -F arch=b64 -S lsetxattr -F auid>=1000 -F auid!=-1 -k perm_mod
-a always,exit -F arch=b64 -S removexattr -F auid>=1000 -F auid!=-1 -k perm_mod
-a always,exit -F arch=b64 -S setxattr -F auid>=1000 -F auid!=-1 -k perm_mod
-w /usr/bin/python3 -p x -k python
-w /usr/bin/python -p x -k python
-w /bin/python3 -p x -k python
-w /bin/python -p x -k python
-w /usr/bin/whoami -p x -k whoami
-w /usr/bin/id -p x -k id
-w /bin/hostname -p x -k hostname
-w /bin/uname -p x -k uname
-w /etc/issue -p r -k issue
-w /etc/hostname -p r -k hostname
-w /root/.ssh -p wa -k rootkey
-w /usr/bin/grep -p x -k string_search
-w /usr/bin/egrep -p x -k string_search
-w /usr/bin/ugrep -p x -k string_search
-w /bin/bash -p x -k susp_shell
-w /bin/dash -p x -k susp_shell
-w /bin/busybox -p x -k susp_shell
-w /bin/zsh -p x -k susp_shell
-w /bin/sh -p x -k susp_shell
-w /bin/ksh -p x -k susp_shell
-a always,exit -F arch=b32 -S all -k 32bit_start
-w /usr/bin/wget -p x -k susp_activity
-w /usr/bin/curl -p x -k susp_activity
-w /usr/bin/base64 -p x -k susp_activity
-w /bin/nc -p x -k susp_activity
-w /bin/netcat -p x -k susp_activity
-w /usr/bin/ncat -p x -k susp_activity
-w /usr/bin/ss -p x -k susp_activity
-w /usr/bin/netstat -p x -k susp_activity
-w /usr/bin/ssh -p x -k susp_activity
-w /usr/bin/scp -p x -k susp_activity
-w /usr/bin/sftp -p x -k susp_activity
-w /usr/bin/ftp -p x -k susp_activity
-w /usr/bin/socat -p x -k susp_activity
-w /usr/bin/wireshark -p x -k susp_activity
-w /usr/bin/tshark -p x -k susp_activity
-w /usr/bin/rawshark -p x -k susp_activity
-w /usr/bin/rdesktop -p x -k susp_activity
-w /usr/local/bin/rdesktop -p x -k susp_activity
-w /usr/bin/wlfreerdp -p x -k susp_activity
-w /usr/bin/xfreerdp -p x -k susp_activity
-w /usr/local/bin/xfreerdp -p x -k susp_activity
-w /usr/bin/nmap -p x -k susp_activity" > /etc/audit/rules.d/becloud.rules
fi
}
NO='\033[0m'
BL='\033[0;34m'
RE='\033[0;31m'
GR='\033[0;32m'
YE='\033[1;33m'
profile
oib
audit
echo "${GR}-----------------------Summary results-----------------------${NO}"
os_info
report
echo "##################################"
echo "# Configure 93.125.20.158 on EDGE "
echo "##################################"
echo "${GR}-----------------------End report-----------------------${NO}"

