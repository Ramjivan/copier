#!/usr/bin/bash

IFS='
'

function rp() {

local array=(`ls -1`)

for i in ${array[@]}
do
temp="/mnt/f/"
temp+=$i
mv $i $temp
let start+=1
done
}
 
darray=(`ls -1`)

for d in ${darray[@]}
do
cd $d
rp
cd ..
done


