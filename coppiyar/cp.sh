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



for fileItemString in ${fileItemString[@]} 
do
temp="SRC/"
temp+=$fileItemString
cp -r "$temp" "$1" 
done

exit 0