#!/bin/sh
INTERFACE="eth0"
PID="$(ps | grep udhcpc | grep $INTERFACE | grep -v $0 | awk '{print $1}')"
kill -9 `cat /tmp/udhcpc_runner.pid` $PID
echo $$ > /tmp/udhcpc_runner.pid
echo "ifconfig eth0 $1 netmask $2 up; route del default; route add default gw $3" > /usr/share/udhcpc/sample.leasefail

chmod +x /usr/share/udhcpc/sample.leasefail

while [ "a" = "a" ];
do
    /sbin/udhcpc -i $INTERFACE -f
done
