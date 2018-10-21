#!/bin/bash

fileItemString=$(cat  dir.txt |tr "\n" " ")
a=0
gg="/home/pi/dir.txt"
  while IFS= read -r line
    do   
	fileItemString[$a]="$line"
        echo ${fileItemString[$a]}
        let a+=1    
    done <"$gg"



for fileItem in ${fileItemString[@]} 
do
randstr=$(cat /dev/urandom | tr -cd '0-9' | head -c 10)
temp="/home/pi/src/"
temp+=$fileItem
dest="$1"
dest+="/"
dest+="$randstr"
cp "$temp" "$dest" 
done

exit 0