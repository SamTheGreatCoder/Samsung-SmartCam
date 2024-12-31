#!/bin/sh

IFNAME=$1
STATUS=$2
NOTIFY_PATH="/tmp/hostapd/hostapd_cli/action/$IFNAME"

network_notifier $NOTIFY_PATH $STATUS
exit 0
