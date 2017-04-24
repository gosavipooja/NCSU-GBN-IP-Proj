#!/bin/bash
s_ip='152.7.99.61'
s_port=7735
filenm='../UT/in.txt'

p='0.05'
N_arr=( 1 2 4 8 16 32 64 128 256 512 1024 )
MSS=500

src='GBNtx.py'

tid=1


for N in ${N_arr[*]};
do
	for i in `seq 1 5`;
	do
		#N=10
		python $src $s_ip $s_port $filenm $N $MSS
		echo "ID=$tid N=$N Iter=$i"
		tid=`expr $tid + 1`
		sleep 10
		#exit 0
	done
exit 0
done

 
