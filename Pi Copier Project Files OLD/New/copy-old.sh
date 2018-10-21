#!/bin/bash

#get all flesh drives in an array
media="/media/pi"
echo $(ls $media > drives.txt)

a=0
drives="/home/pi/drives.txt"
  while IFS= read -r line
    do   
	temp="$media"
	temp+="/"
	temp+="$line"
	usb[$a]=$temp
        echo ${usb[$a]}
        let a+=1    
    done <"$drives"

#tLen=${#usb[@]}
for d in ${usb[@]} #(( d=0; i<${tLen}; d++ ));
do
cp -r "SANT VANEE 47" "$d" &
done
echo "runing" > status.txt
echo "copy started LED status blinking"
wait
echo "ready" > status.txt 
echo "Copy completed"
shutdown -r now

exit 0