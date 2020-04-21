#!/bin/bash


for number_request in 100 1000 3000 5000 10000;
do
	#Starting time counting
	START=$(date +%s)
		for count_request in $(seq $number_request);
		do
			curl 10.0.0.11:9000 #making request
		done    
    END=$(date +%s)
    #Ending time counting
    Time_Resquest=$(($END - $START)) 
    echo "Time $Time_Resquest for $count_request" >> results1.txt
done 