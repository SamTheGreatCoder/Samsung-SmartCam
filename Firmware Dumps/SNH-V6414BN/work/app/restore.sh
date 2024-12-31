#!/bin/sh
echo "Run Restore..."

if [ -e /mnt/custom/iwatch/scripts/restore.sh ]; then
  /mnt/custom/iwatch/scripts/restore.sh &
fi

