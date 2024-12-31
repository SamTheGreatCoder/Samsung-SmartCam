#!/bin/sh

IWL_HOME=/mnt/custom/iwatch

echo $(date +%F-%T) " - Uninstalling Firmware" >> /tmp/logs/iwl.firmware.log

uninstall_fw(){
        if [ -e "$IWL_HOME/firmware/iwatch/current/manifest" ]; then
            rm -Rf $IWL_HOME/*
            sync
        fi
}

echo $(date +%F-%T) " - Uninstalling current stack" >> /tmp/logs/iwl.firmware.log

if [ -d "$IWL_HOME/firmware/iwatch/current" ]; then
    $IWL_HOME/scripts/iwl_stop.sh
	uninstall_fw
    /work/custom/iwatch/install.sh
    $IWL_HOME/scripts/start.sh &
else
  echo $(date +%F-%T) " - Uninstaller has not detected an active stack" >> /tmp/logs/iwl.firmware.log  
fi


echo $(date +%F-%T) " - Uninstall Complete" >> /tmp/logs/iwl.firmware.log
