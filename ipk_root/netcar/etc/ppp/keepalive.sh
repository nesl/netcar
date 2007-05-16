#!/bin/sh
#
# /etc/ppp/keepalive.sh
#
# Test periodically the connection and restart it if the connection is down
#
# Please set DNS_PROVIDER and add this line to cron :
# */5 * * * * root /etc/ppp/keepalive.sh
#
#this is nesl.ee.ucla.edu
DNS_PROVIDER="128.97.92.177"

ppp_restart()
{
echo "PPP Connection down ... restarting pppd ..." | logger -t keepalive
killall pppd > /dev/null 2>&1
rm -rf /var/run/ppp0.pid > /dev/null 2>&1
sleep 10
pppd call gprs > /var/log/pppd.log 2>&1 &
}

if [ -f /var/run/ppp0.pid ] ; then
ping -c 4 $DNS_PROVIDER 2>&1 | grep "0 packets" > /dev/null && ppp_restart
else
ppp_restart
fi

