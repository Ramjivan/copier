for d in $(find /mnt/c/SoorsagarRamdwara -maxdepth 1 -type d)
do
  #Do something, the directory is accessible with $d:
  find -name "* *" -type f | rename 's/ /_/g'
  echo $d
done >output_file

