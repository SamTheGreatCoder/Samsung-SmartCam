#!/bin/sh
sleep 5                         
                               
if [ -f /root/nfs ]; then
ifconfig eth0 192.168.10.175 up
sleep 1 
mount -t nfs -o nolock 192.168.10.179:/home/hive21/Dev/wr4.0/nfsroot/ambas2_2015.06.25/work /work
sleep 1                                                                                       
fi                                                                                            
                                                                                              
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
                         
if [ -f /root/autorun ]; then
cd /work/app                 
sleep 1                      
./system_exec &          
sleep 3                  
./mainServer &  
fi    

