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

i=0
for d in ${usb[@]} 
do
cp -r "SANT VANEE 47/." "$d" &
pIdArray[i]=$!
let i+=1
done
echo "runing" > status.txt
echo "copy started LED status blinking"

python blink.py &
blinkProcessID=$!

for i in ${pIdArray[@]}
do
wait $i
done
kill $blinkProcessID
echo "ready" > status.txt 
echo "Copy completed"
python ab.py
#shutdown -r now

exit 0