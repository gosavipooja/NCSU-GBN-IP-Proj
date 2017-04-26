#!/bin/bash
s_ip='152.7.99.61'
s_port=7735
filenm='../UT/in.txt'

p='0.05'
N=64
MSS_arr=( 100 200 300 400 500 600 700 800 900 1000 )

src='GBNtx.py'

tid=1


for MSS in ${MSS_arr[*]};
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

 
