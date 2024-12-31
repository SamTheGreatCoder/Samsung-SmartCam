#!/bin/sh

[ -n "$1" ] || { echo "Error: should be called from udhcpc"; exit 1; }

NETMASK=""
[ -n "$subnet" ] && NETMASK="netmask $subnet"
#BROADCAST="broadcast +"
BROADCAST=""
[ -n "$broadcast" ] && BROADCAST="broadcast $broadcast"

SCRIPT_NAME="udhcpc"
NOTIFY_PATH="/tmp/$SCRIPT_NAME/$interface"
LOG_PREFIX="$SCRIPT_NAME($interface):"

[ -f /tmp/$SCRIPT_NAME/running ] || { echo -e "\033[31m$LOG_PREFIX failed(not running)\033[0m"; exit 1; }

case "$1" in
    deconfig)
        echo -e "\033[33m$LOG_PREFIX setting ip_address 0.0.0.0\033[0m"
        ifconfig $interface 0.0.0.0 2> /dev/null
        ;;

    renew|bound)
        echo -e "\033[32m$LOG_PREFIX $1 (lease time: $lease s)\033[0m"
        echo -e "\033[32m$LOG_PREFIX adding ip_address $ip\033[0m"
        ifconfig $interface $ip $NETMASK $BROADCAST

        if [ -n "$router" ] ; then
            while route del default gw 0.0.0.0 dev $interface ; do
                :
            done

            metric=0
            for i in $router ; do
                echo -e "\033[32m$LOG_PREFIX adding gateway $i\033[0m"
                route add default gw $i dev $interface metric $((metric++))
            done
        fi

        RESOLV_CONF="/etc/resolv.conf"
        echo -n > $RESOLV_CONF-$$
        [ -n "$domain" ] && echo "search $domain" >> $RESOLV_CONF-$$
        for i in $dns ; do
            echo -e "\033[32m$LOG_PREFIX adding nameserver $i\033[0m"
            echo "nameserver $i" >> $RESOLV_CONF-$$
        done
        mv $RESOLV_CONF-$$ $RESOLV_CONF

        ifconfig $interface
        network_notifier $NOTIFY_PATH "started"
        ;;

    *)
        echo -e "\033[31m$LOG_PREFIX failed($1 - $message)\033[0m"
        network_notifier $NOTIFY_PATH "failed"
        ;;
esac
exit 0
