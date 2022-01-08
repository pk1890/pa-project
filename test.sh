#!/bin/bash -l


#SBATCH --nodes 1
#SBATCH --ntasks 8
#SBATCH --time=01:00:00
#SBATCH --partition=plgrid-testing

# module load plgrid/tools/python-intel/3.6.5 2>/dev/null

test_iterations=5
thread_nums=(8 7 6 5 4 3 2 1)
problem_sizes=(840 1680)

report_file=report_half_ring_3.csv

echo "thread_num;problem_size;time" >> $report_file
for i in $(seq 1 $test_iterations); do
    for thread_num in "${thread_nums[@]}"; do
        for problem_size in "${problem_sizes[@]}"; do
            command="mpirun -np $thread_num ./parallel_ring_2.py $problem_size"
            echo $command
            time=$($command)
            printf "%d;%d;%lf\n" $thread_num $problem_size $time >> $report_file
        done
    done
done