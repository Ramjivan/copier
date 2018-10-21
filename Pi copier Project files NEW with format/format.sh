#!/bin/bash

#getting all mount points and storing to mpoints.txt
df -B1 | grep -vE '^Filesystem|tmpfs|cdrom' | awk '{ print $1 }'|tail -n +3 > mpoints.txt

#now getting all drives in an array usb

a=0
mountpoints="/home/pi/mpoints.txt"
  while IFS= read -r line
    do  
	usb[$a]="$line"
        a=$((i+1))    
    done <"$mountpoints"

#looping through usb array
i=0

for d in ${usb[@]} 
do
#umount the drive
umount "$d"
sudo -u pi mkfs.vfat "$d" -n SANTVANI
udisksctl mount --block-device "$d"
let i+=1
done


