#!/bin/sh

IWL_HOME=/mnt/custom/iwatch
TMP_DIR=/tmp/iwlinstaller.$(date +%s)

echo $(date +%F-%T) " - install.sh - Installing iWatchLife stack..." >> /tmp/logs/iwl.firmware.log

mkdir $TMP_DIR
tar -zxvf $1 -C $TMP_DIR 2>&1 > /dev/null
chmod a+x $TMP_DIR/install.sh
$TMP_DIR/install.sh >> /tmp/logs/iwl.firmware.log
echo $(date +%F-%T) " - install.sh - Cleaning up install files..." >> /tmp/logs/iwl.firmware.log
rm -Rf $TMP_DIR
rm $1
 
echo $(date +%F-%T) " - install.sh - Complete" >> /tmp/logs/iwl.firmware.log
