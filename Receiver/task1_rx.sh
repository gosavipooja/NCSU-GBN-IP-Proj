#!/bin/bash
p=0.05

for i in `seq 1 50`;
do
	python GBNrx.py 7735 out.txt $p
	echo " Done ID=$i"
	echo " Diff = "
	diff out.txt ../UT/in.txt
	sleep 5

done
