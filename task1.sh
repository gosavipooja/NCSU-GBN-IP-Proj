#!/bin/sh
s_ip='127.0.0.1'
s_port=7735
filenm='../UT/in.txt'

p='0.0'
N=10
MSS=1024

src=$1

if [[ -n "$src" ]]; then
	echo "Please provide script location as argument"
fi

python $src $s_ip $s_port $filenm $N $MSS 
