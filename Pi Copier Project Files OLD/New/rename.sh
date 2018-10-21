#!/usr/bin/bash

IFS='
'
echo "Enter starting point"
read start


function rp() {

    local array=(`ls -1`)

    for i in ${array[@]}
    do
        temp=""
        templen="${#start}"
        if [ $templen -eq "1" ]
        then
        temp+="000"
        fi
        if [ $templen -eq "2" ]
        then
        temp+="00"
        fi
        if [ $templen -eq "3" ]
        then
        temp+="0"
        fi
        temp+=$start
        temp+=".mp3"
        mv $i $temp
        let start+=1
    done
}
 
darray=(`ls -1`)

for d in ${darray[@]}
do
cd $d
find -name "* *" -type f | rename 's/ /_/g'
rp
cd ..
done


