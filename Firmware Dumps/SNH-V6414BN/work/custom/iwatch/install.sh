#!/bin/sh

INSTALL_DIR=`dirname $0`
VERSION=`cat $INSTALL_DIR/base.ver`
IWL_HOME=/mnt/custom/iwatch
mkdir -p /tmp/logs/
LOG_FILE=/tmp/logs/iwl.firmware.log
execute_install=0

echo $(date +%F-%T) " - Installing Base Firmware $VERSION" >> $LOG_FILE

uninstall_fw(){
        if [ -e "$IWL_HOME/firmware/base/current/manifest" ]; then
            while read item; do
                        file=$(echo $item | cut -f1 -d':')
                        directory=$(echo $item | cut -f2 -d':')
                        link_file=$(echo $item | cut -f3 -d':')
                        if [ -n "$file" ]; then
                                echo $(date +%F-%T) " - Unlinking file $file to $directory/$link_file" >> $LOG_FILE
                                rm -f $IWL_HOME/$directory/$link_file
                        fi
            done < $IWL_HOME/firmware/base/current/manifest
        fi
}

install_fw(){
    while read item; do
                file=$(echo $item | cut -f1 -d':')
                directory=$(echo $item | cut -f2 -d':')
                link_file=$(echo $item | cut -f3 -d':')
                if [ -n "$file" ]; then
                        echo $(date +%F-%T) " - Linking file $file to $directory/$link_file" >> $LOG_FILE
                        ln -sf $IWL_HOME/firmware/base/$VERSION/$directory/$file $IWL_HOME/$directory/$link_file
                fi
    done < $IWL_HOME/firmware/base/$VERSION/manifest
}


check_ver () {
    VER1=`echo "$1" | awk -F. '{ printf("%d%d%d%d\n", $1,$2,$3,$4); }';`
    VER2=`echo "$2" | awk -F. '{ printf("%d%d%d%d\n", $1,$2,$3,$4); }';`
    if [ "$VER2" -gt "$VER1" ]; then
       return 1
    else
       return 0
    fi
}

verify_manifest(){
        if [ -e "$IWL_HOME/firmware/base/current/manifest" ]; then
            while read item; do
                    file=$(echo $item | cut -f1 -d':')
                    directory=$(echo $item | cut -f2 -d':')
                    link_file=$(echo $item | cut -f3 -d':')
                    if [ ! -e $IWL_HOME/$directory/$link_file ]; then
                            return 0
                    fi
            done < $IWL_HOME/firmware/base/current/manifest
            return 1
        else
            return 0
        fi
}

# verify integrity of current firmware
if [ -d $IWL_HOME/firmware/base/current ]; then
   echo $(date +%F-%T) " - Firmware exists....verifying manifest" >> $LOG_FILE
   verify_manifest
   manifest_chk=$?

   if [ $manifest_chk -eq 0 ]; then
        echo $(date +%F-%T) " - Manifest corruption detected - reinstall required" >> $LOG_FILE
        execute_install=1
    else
      if [ -e "$IWL_HOME/conf/base.ver" ]; then
        OLDVERSION=$(cat "$IWL_HOME/conf/base.ver")
        check_ver "$OLDVERSION" "$VERSION"
        version_chk=$? 
        if [ $version_chk -eq 1 ]; then
            echo $(date +%F-%T) " - Firmware [ $OLDVERSION ] requies update .... initiating installation" >>  $LOG_FILE
            execute_install=1   
        fi
      else
        echo $(date +%F-%T) " - Firmware corruption detected - reinstall required" >> $LOG_FILE             
        execute_install=1          
      fi      
   fi
else
    execute_install=1
fi

# install if required
if [ $execute_install -eq 1 ]; then
    echo $(date +%F-%T) " - Shutting down daemons" >> $LOG_FILE

    if [ -e "$IWL_HOME/conf/base.ver" ]; then
        OLDVERSION=$(cat "$IWL_HOME/conf/base.ver")
    fi


    killall -9 qr_daemon > /dev/null 2>&1

    echo $(date +%F-%T) " - Uninstalling previous version" >> $LOG_FILE
    if [ -d "$IWL_HOME/firmware/base/current" ]; then
        uninstall_fw
        rm -Rf $IWL_HOME/firmware/base/current/
    fi

    echo $(date +%F-%T) " - Making iWatchLife directories" >> $LOG_FILE
    mkdir -p $IWL_HOME/bin
    mkdir -p $IWL_HOME/lib
    mkdir -p $IWL_HOME/audio
    mkdir -p $IWL_HOME/web/admin
    mkdir -p $IWL_HOME/web/api
    mkdir -p $IWL_HOME/scripts
    mkdir -p $IWL_HOME/include/php/camera
    mkdir -p $IWL_HOME/firmware/base/$VERSION
    mkdir -p $IWL_HOME/firmware/iwatch
    mkdir -p $IWL_HOME/conf

    echo $(date +%F-%T) " - Copy Firmware to Flash" >> $LOG_FILE
    cp -Rf $INSTALL_DIR/data/* $IWL_HOME/firmware/base/$VERSION/
    cp -f $INSTALL_DIR/manifest $IWL_HOME/firmware/base/$VERSION/
    ln -sf $IWL_HOME/firmware/base/$VERSION/ $IWL_HOME/firmware/base/current

    echo $(date +%F-%T) " - Linking firmware" >> $LOG_FILE
    install_fw

    echo $VERSION > $IWL_HOME/conf/base.ver
    cp -f $INSTALL_DIR/iwatch-lighttpd.conf $IWL_HOME
    chmod 777 $IWL_HOME/iwatch-lighttpd.conf

    echo $(date +%F-%T) " - Finalizing Installation...." >> $LOG_FILE
    chmod 777 -R $IWL_HOME/scripts/*
    chmod 777 -R $IWL_HOME/bin/*

    if [ ! -z $OLDVERSION ] && [ -d "$IWL_HOME/firmware/base/current" ] && [ "$OLDVERSION" != "$VERSION" ]; then
        if [ -d "$IWL_HOME/firmware/base/$OLDVERSION" ]; then
                echo $(date +%F-%T) " - Removing previous version..$OLDVERSION.." >> $LOG_FILE
                rm -Rf $IWL_HOME/firmware/base/$OLDVERSION
        fi
    fi
    sync
else
    echo $(date +%F-%T) " - Update not required at this time" >> $LOG_FILE
fi

echo $(date +%F-%T) " - Update Complete" >> $LOG_FILE

