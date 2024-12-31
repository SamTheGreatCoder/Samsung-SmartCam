#!/bin/sh

IFNAME=$1
STATUS=$2
NOTIFY_PATH="/tmp/wpa_supplicant/wpa_cli/action/$IFNAME"

case "$STATUS" in
    WPS-SUCCESS)
        cp /tmp/wpa_supplicant/$IFNAME.conf /mnt/setting
        sync
        ;;
esac

network_notifier $NOTIFY_PATH $STATUS
exit 0
