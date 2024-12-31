#!/bin/sh
                               
ifconfig eth0 192.168.10.175 up
#mount -t nfs -o nolock 192.168.10.179:/home/hive21/Dev/wr4.0/nfsroot/ambas2_2015.06.25/work /work
                                                                                              
amba_debug -w 0xe8010018 -d 0x2d800
amba_debug -w 0xe8010004 -d 0x774  
amba_debug -w 0xe8010028 -d 0x64   
amba_debug -w 0xe8010000 -d 0x64   
amba_debug -r 0xe8010000;        
                                
if [ ! -d /mnt/mmcblk0p1 ] ; then
  mkdir -p /mnt/mmcblk0          
  mkdir -p /mnt/mmcblk0p1        
fi                               
sleep 1

# mtd9 mount
#ubiattach /dev/ubi_ctrl -m 9
#ubimkvol /dev/ubi1 -N usr_a -m
#mount -t ubifs ubi1_0 /work
#sleep 1
                         
if [ -r /work/app/mainServer ]; then
   cd /work/app
   ./system_exec &
   ./mainServer &
   exit
fi

umount /work/
mount -t nfs -o nolock 192.168.10.179:/tftpboot/s2lm33_bsp_image /work
sleep 1

if [ ! -r /work/work ]; then
  echo "/work/work does not exist" 
  exit
fi

echo "flash_eraseall /dev/mtd9" 
flash_eraseall /dev/mtd9

echo "nandwrite /dev/mtd9 /work/work" 
nandwrite /dev/mtd9 /work/work

reboot

