#!/bin/bash

fileItemString=$(cat  dir.txt |tr "\n" " ")

files=($fileItemString)


for file in ${files[@]} 
do
dir="SRC/"
dir+=$file
cp -r "$dir" "$1" 
done

exit 0