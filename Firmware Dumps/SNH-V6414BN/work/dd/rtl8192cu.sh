#!/bin/sh

# callsyntax: $0 $1=OP $2=MAC_ADDRESS

OP=$1
MAC_ADDRESS=$2
DRIVER_NAME="rtl8192cu"
DRIVER_PATH="/work/dd/$DRIVER_NAME"
LOG_PREFIX="$DRIVER_NAME:"
NOTIFY_PATH="/tmp/$DRIVER_NAME"
MODULE_EXIST="$(lsmod | grep 8192cu)"

load() {
    if [ "$MODULE_EXIST" = "" ]; then
        if [ "$MAC_ADDRESS" = "" ]; then
            ifconfig eth0 up
            MAC_ADDRESS="$(ifconfig eth0 | grep HWaddr | awk '{print $5}')"
        fi

        insmod $DRIVER_PATH/8192cu.ko rtw_initmac=$MAC_ADDRESS
        if [ "$(iwconfig 2> /dev/null | grep 'REALTEK')" != "" ]; then
            STA_INTERFACE="wlan0"
            echo "sta=$STA_INTERFACE" > $DRIVER_PATH/interface
            ifconfig $STA_INTERFACE up

            OTHER_INTERFACE="wlan1"
            echo "other=$OTHER_INTERFACE" >> $DRIVER_PATH/interface
            ifconfig $OTHER_INTERFACE up

            # modinfo rt2870sta | grep version
            VERSION="$(cat /proc/net/rtl819xC/ver_info)"
            STA_MAC="$(ifconfig $STA_INTERFACE | grep HWaddr | awk '{print $5}')"
            OTHER_MAC="$(ifconfig $OTHER_INTERFACE | grep HWaddr | awk '{print $5}')"
            echo -e "\033[32m$LOG_PREFIX info($VERSION, $STA_INTERFACE: $STA_MAC / $OTHER_INTERFACE: $OTHER_MAC)\033[0m"

            if [ "$STA_INTERFACE" != "" -a "$OTHER_INTERFACE" != "" ]; then
                iwconfig 2> /dev/null
                network_notifier $NOTIFY_PATH "loaded"
            fi
        fi
    fi

    if [ "$STA_INTERFACE" == "" -o "$OTHER_INTERFACE" == "" ]; then
        [ -n "$DEBUG" ] && echo -e "\033[31m$LOG_PREFIX failed\033[0m"
        network_notifier $NOTIFY_PATH "failed"
    fi
}

unload() {
    # [driver issue]
    # http://www.cianmcgovern.com/getting-the-edimax-ew-7811un-working-on-linux/
    # http://e2e.ti.com/support/embedded/linux/f/354/t/91728.aspx
    # http://e2e.ti.com/support/embedded/linux/f/354/t/180021.aspx
    if [ "$MODULE_EXIST" != "" ]; then
        rmmod 8192cu
        sleep 1
    fi

    [ -n "$DEBUG" ] && echo -e "\033[32m$LOG_PREFIX unloadped\033[0m"
    network_notifier $NOTIFY_PATH "unloaded"
}

status() {
    if [ "$MODULE_EXIST" != "" ]; then
        [ -n "$DEBUG" ] && echo -e "\033[33m$LOG_PREFIX running\033[0m"
        network_notifier $NOTIFY_PATH "loaded"
    else
        [ -n "$DEBUG" ] && echo -e "\033[33m$LOG_PREFIX not running\033[0m"
        network_notifier $NOTIFY_PATH "failed"
    fi
}

case $OP in
    load|unload|status)
        $OP
        ;;
    *)
        echo -e "Usage: $0 [load|unload|status] [mac_address]"
        exit 1
        ;;
esac

exit $?
