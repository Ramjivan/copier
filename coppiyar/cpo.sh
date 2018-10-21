#!/bin/bash

fileItemString=$(cat  dir.txt |tr "\n" " ")

dir=($fileItemString)


for dir in ${dir[@]} 
do
temp="SRC/"
temp+=$dir
cp -r "$temp" "$1" 
done

exit 0