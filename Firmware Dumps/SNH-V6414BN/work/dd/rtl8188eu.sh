#!/bin/sh

# callsyntax: $0 $1=OP $2=MAC_ADDRESS

OP=$1
MAC_ADDRESS=$2
DRIVER_NAME="rtl8188eu"
DRIVER_PATH="/work/dd"
MODULE_CFG80211_PATH="/lib/modules/3.10.73/kernel/net/wireless"
MODULE_MAC80211_PATH="/lib/modules/3.10.73/kernel/net/mac80211"
LOG_PREFIX="$DRIVER_NAME:"
NOTIFY_PATH="/tmp/$DRIVER_NAME"
STA_INTERFACE="wlan0"
P2P_INTERFACE="wlan1"
CHECK_LSMOD="$(lsmod | grep -e 8188eu)"
CHECK_IFCONFIG="$(ifconfig 2> /dev/null | grep -e $STA_INTERFACE -e $P2P_INTERFACE)"
CHECK_IWCONFIG="$(iwconfig 2> /dev/null | grep 'IEEE')"

load() {
    STATUS="LOADING"
    echo -e "\033[33m$LOG_PREFIX 1. check interface and device\033[0m"
    if [ "$CHECK_LSMOD" = "" -a "$CHECK_IFCONFIG" = "" ]; then
        if [ "$MAC_ADDRESS" = "" ]; then
            ifconfig eth0 up
            MAC_ADDRESS="$(ifconfig eth0 | grep HWaddr | awk '{print $5}')"
        fi

        echo -e "\033[33m$LOG_PREFIX 2. enable usb\033[0m"
        # gpio2_5 (WIFI_EN)
        # himm_mask 0x200F002C 0xfffffff0 0x0
        # himm_mask 0x20160400 0xffffffdf 0x20
        # himm_mask 0x201603fc 0xffffffdf 0x00
        amba_debug -w 0xe8010028 -d 0x20
        amba_debug -w 0xe8010000 -d 0x20

        echo -e "\033[33m$LOG_PREFIX 3. insmod modules\033[0m"
	pwd
	# insmod $MODULE_CFG80211_PATH/cfg80211.ko
	# insmod $MODULE_MAC80211_PATH/mac80211.ko
    insmod $DRIVER_PATH/8188eu.ko rtw_initmac=$MAC_ADDRESS
	sleep 5
        CHECK_IWCONFIG="$(iwconfig 2> /dev/null | grep 'IEEE')"
        if [ "$CHECK_IWCONFIG" != "" ]; then
            echo -e "\033[33m$LOG_PREFIX 4. ifconfig up\033[0m"
            ifconfig $STA_INTERFACE up
            ifconfig $OTHER_INTERFACE up
            CHECK_IFCONFIG="$(ifconfig 2> /dev/null | grep -e $STA_INTERFACE -e $P2P_INTERFACE)"
            if [ "$CHECK_IFCONFIG" = "" ]; then
                STATUS="FAILED"
            else
                # modinfo rt2870sta | grep version
                # VERSION="$(cat /proc/net/rtl819xC/ver_info)"
                STA_MAC="$(ifconfig $STA_INTERFACE | grep HWaddr | awk '{print $5}')"
                P2P_MAC="$(ifconfig $P2P_INTERFACE | grep HWaddr | awk '{print $5}')"
                echo -e "\033[32m$LOG_PREFIX 5. info($STA_INTERFACE: $STA_MAC / $P2P_INTERFACE: $P2P_MAC)\033[0m"
                iwconfig 2> /dev/null
                # ifconfig $STA_INTERFACE down
                # ifconfig $OTHER_INTERFACE down
                network_notifier $NOTIFY_PATH "loaded"
                STATUS="LOADED"
            fi
        fi
    fi

    if [ "$STATUS" != "LOADED" ]; then
        echo -e "\033[31m$LOG_PREFIX failed\033[0m"
        network_notifier $NOTIFY_PATH "failed"
    fi
}

unload() {
    # [driver issue]
    # http://www.cianmcgovern.com/getting-the-edimax-ew-7811un-working-on-linux/
    # http://e2e.ti.com/support/embedded/linux/f/354/t/91728.aspx
    # http://e2e.ti.com/support/embedded/linux/f/354/t/180021.aspx
    echo -e "\033[33m$LOG_PREFIX 1. rmmod modules\033[0m"
    if [ "$CHECK_LSMOD" != "" ]; then
        amba_debug -w 0xe8010028 -d 0x20
        amba_debug -w 0xe8010000 -d 0x0
        rmmod 8188eu
        sleep 1
    fi

    echo -e "\033[32m$LOG_PREFIX unloaded\033[0m"
    network_notifier $NOTIFY_PATH "unloaded"
}

status() {
    if [ "$CHECK_LSMOD" != "" -a "$CHECK_IWCONFIG" != "" ]; then
        echo -e "\033[33m$LOG_PREFIX running\033[0m"
    else
        echo -e "\033[33m$LOG_PREFIX not running\033[0m"
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
