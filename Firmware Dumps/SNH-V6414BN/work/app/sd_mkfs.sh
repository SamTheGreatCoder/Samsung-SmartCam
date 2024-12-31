#!/bin/sh


if [ "$1" == "VFAT" ]
then
	echo "---------- mkfs.vfat --------"
	mkfs.vfat /dev/mmcblk0p1; touch /tmp/mkfs_done

elif [ "$1" == "EXT4" ]
then
	echo "---------- mkfs.ext4 --------"
	mkfs.ext4 -O ^huge_file /dev/mmcblk0p1 -v -b 1024; touch /tmp/mkfs_done

else
	echo "Unknow SD filesystem"
fi

echo "### SD card mkfs finish ###"


