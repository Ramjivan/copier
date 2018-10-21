#!/bin/bash

IFS='
'

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


echo "runing" > status.txt
echo "copy is about to start LED status blinking"


cd "SANT VANEE 47"
darray=(`ls -1`)
cd ..

python blink.py &
blinkProcessID=$!


for d in ${darray[@]} 
do
	i=0
	for usb in ${usb[@]} 
	do 
		sdir="SANT VANEE 47/"
		sdir+=$d
		cp -r "$sdir" "$usb" &
		pIdArray[i]=$!
		let i+=1
	done
	
	
	
	
	for i in ${pIdArray[@]}
	do
		wait $i
	done

done

kill $blinkProcessID

echo "ready" > status.txt 
echo "Copy completed"
python ab.py
#shutdown -r now

exit 0