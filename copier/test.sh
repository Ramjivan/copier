#!/bin/bash


cd "SANT VANEE 47"
echo | ls > /home/pi/dir.txt
cd ..

fileItemString=$(cat  dir.txt |tr "\n" " ")

dir=($fileItemString)

for i in ${dir[@]}
do
echo "$i"
done

exit 0
