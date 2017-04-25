#!/bin/sh
s_ip='152.7.99.61'
s_port=7735
filenm='../UT/in.txt'

p='0.05'
N_arr=(1 2 4 8 16 32 64 128 256 512 1024)
MSS=500

src=$1

if [[ -n "$src" ]]; then
	echo "Please provide script location as argument"
	#exit 0
fi

for N in ${N_arr[*]};
do
	for i in `seq 1 5`;
	do
		N=10
		python $src $s_ip $s_port $filenm $N $MSS
		echo "N=$N Iter=$i"
		exit 0
	done
done

 
