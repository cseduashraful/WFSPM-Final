#!/bin/bash

array=( 0.009 )
#array=( 0.06 0.05 )
algo=( wfspm )
data="data/large.txt"
weight="data/weight_large_normal.txt"


for a in "${algo[@]}"
do
        for i in "${array[@]}"
        do
                echo "$data $weight $a $i"
                python main.py -d $data -w $weight -a $a -t $i >> run_log.txt
        done
done
