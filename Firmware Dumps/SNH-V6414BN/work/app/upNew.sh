#!/bin/bash

echo ------------- START UPGRADE SNH-V6414BN --------------

cp /work/app/upgrade_noti /tmp/daemon/upgrade_noti

ALL=$*

RETVAL=`ps -a | grep upgrade_noti | /usr/bin/awk 'NR%2==1' | /usr/bin/awk '{print $4}'`
echo $RETVAL

if [ "$RETVAL" != "/tmp/daemon/upgrade_noti" ]; then
  /tmp/daemon/upgrade_noti $ALL &
fi

echo -------------  FINISH ----------------------------------
