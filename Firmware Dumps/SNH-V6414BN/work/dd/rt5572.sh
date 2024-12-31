#!/bin/sh

# callsyntax: $0 $1=OP $2=MAC_ADDRESS

OP=$1
MAC_ADDRESS=$2
MANUFACTURER="mediatek"
DRIVER_NAME="rt5572"
DRIVER_PATH="/work/dd/$MANUFACTURER"
DATA_NAME="rt5572.dat"
DATA_PATH="$DRIVER_PATH/$DATA_NAME"
LOG_PREFIX="$DRIVER_NAME:"
NOTIFY_PATH="/tmp/$MANUFACTURER/$DRIVER_NAME"
MODULE_EXIST="$(lsmod | grep rtutil5572sta | grep rtnet5572sta | grep rt5572sta)"

start() {
    if [ "$MODULE_EXIST" = "" ]; then
        if [ "$MAC_ADDRESS" = "" ]; then
            ifconfig eth0 up
            MAC_ADDRESS="$(ifconfig eth0 | grep HWaddr | awk '{print $5}')"
        fi

        if [ ! -f $DATA_PATH ]; then
            cp "/work/dd/rt5572/$DATA_NAME" $DATA_PATH
            if [ "$MAC_ADDRESS" != "" ]; then
                echo "MacAddress=$MAC_ADDRESS" >> $DATA_PATH
            fi
        fi

        insmod $DRIVER_PATH/rtutil5572sta.ko
        insmod $DRIVER_PATH/rt5572sta.ko
        insmod $DRIVER_PATH/rtnet5572sta.ko
        STA_INTERFACE="$(iwconfig 2> /dev/null | grep 'Ralink STA' | awk '{print $1}')"
        if [ "$STA_INTERFACE" != "" ]; then
            ifconfig $STA_INTERFACE up

            # p2p interface is depended by wlan0 interface
            P2P_INTERFACE="$(iwconfig 2> /dev/null | grep 'Ralink P2P' | awk '{print $1}')"
            ifconfig $P2P_INTERFACE up

            # modinfo rt2870sta | grep version
            echo -e "\033[32m$LOG_PREFIX info($STA_INTERFACE/$P2P_INTERFACE, $MAC_ADDRESS)\033[0m"

            if [ "$STA_INTERFACE" != "" -a "$P2P_INTERFACE" != "" ]; then
                iwconfig 2> /dev/null
                network_notifier $NOTIFY_PATH "started"
            fi
        fi
    fi

    if [ "$STA_INTERFACE" == "" -o "$P2P_INTERFACE" == "" ]; then
        [ -n "$DEBUG" ] && echo -e "\033[31m$LOG_PREFIX failed\033[0m"
        network_notifier $NOTIFY_PATH "failed"
    fi
}

stop() {
    if [ "$MODULE_EXIST" != "" ]; then
        rmmod rtnet5572sta
        rmmod rt5572sta
        rmmod rtutil5572sta
    fi

    [ -n "$DEBUG" ] && echo -e "\033[32m$LOG_PREFIX stopped\033[0m"
    network_notifier $NOTIFY_PATH "stopped"
}

status() {
    if [ "$MODULE_EXIST" != "" ]; then
        [ -n "$DEBUG" ] && echo -e "\033[33m$LOG_PREFIX running\033[0m"
        network_notifier $NOTIFY_PATH "started"
    else
        [ -n "$DEBUG" ] && echo -e "\033[33m$LOG_PREFIX not running\033[0m"
        network_notifier $NOTIFY_PATH "failed"
    fi
}

case $OP in
    start|stop|status)
        $OP
        ;;
    *)
        echo -e "Usage: $0 [start|stop|status] [mac_address]"
        exit 1
        ;;
esac

exit $?
