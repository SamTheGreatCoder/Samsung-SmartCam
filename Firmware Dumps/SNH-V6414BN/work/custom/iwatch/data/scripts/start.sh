#!/bin/sh

export IWL_HOME=/mnt/custom/iwatch

mkdir -p /tmp/logs

CREDS=`cat /tmp/daemon/cfg/lighttpd.user`

if [ -e "$IWL_HOME/scripts/iwl_start.sh" ] && [ "$CREDS" != "admin:" ]; then
   $IWL_HOME/scripts/iwl_start.sh &
elif [ -e "$IWL_HOME/bin/qr_daemon" ]; then
   $IWL_HOME/bin/qr_daemon -usrpwd $CREDS -fps 1 -camera_make Samsung -dim 640x360 -camera_model 6414 -activate_only > /dev/null 2>&1  &
fi
