#!/bin/bash -l

test_iterations=5
thread_nums=(12 11 10 9 8 7 6 5 4 3 2 1)
problem_sizes=(60 120 180 240 300)
problems_iterations=100

report_file=report2.csv

echo "thread_num;problem_size;time" >> $report_file
for i in $(seq 1 $test_iterations); do
    for thread_num in "${thread_nums[@]}"; do
        for problem_size in "${problem_sizes[@]}"; do
            command="mpirun -np $thread_num ./parallel_ring.py $problem_size"
            echo $command
            time=$($command)
            printf "%d;%d;%lf\n" $thread_num $problem_size $time >> $report_file
        done
    done
done