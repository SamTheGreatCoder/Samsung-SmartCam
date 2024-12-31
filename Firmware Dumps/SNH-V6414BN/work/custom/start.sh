#!/bin/sh

if [ ! -d $CUSTOM_WEB_HOME ]; then
    if [ -e $CUSTOM_WEB_HOME ]; then
        rm $CUSTOM_WEB_HOME -rf
    fi
    mkdir $CUSTOM_WEB_HOME
fi
$CUSTOM_MNT_POINT/iwatch/start.sh &

