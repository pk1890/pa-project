#!/usr/bin/env python3

from mpi4py import MPI
import socket
import sys
import numpy as np
import math
from common import calculate_single_acceleration, generateStars, print_stars, makeStar
from pprint import pprint

comm = MPI.COMM_WORLD
num_threads = comm.Get_size()
thread_id = comm.Get_rank()

def calculate_parallel(*, local_size = 3, global_stars = None):
    if global_stars is None:
        local_stars = generateStars(local_size)
    else:
        coeff = int(math.ceil(len(global_stars)/num_threads))
        local_stars = global_stars[thread_id*coeff:(thread_id+1)*coeff]

    buffer = [x[0] for x in local_stars]
    moving_aggr = [x[0] for x in local_stars]
    
    # calculate local stars
    for i in range(len(local_stars)):
        star = local_stars[i]
        local_stars[i][1] = sum([calculate_single_acceleration(star, local_stars[j])
                for j in range(len(local_stars)) if not i == j])

    receiver_thread = (thread_id + 1) % num_threads
    source_thread = (thread_id - 1) % num_threads

    # ring execution
    for i in range(1, int(num_threads/2)):
        comm.isend(buffer, dest=receiver_thread)
        buffer = comm.recv(source=source_thread)

        for i in range(len(local_stars)):
            star = local_stars[i]
            local_stars[i][1] += sum([calculate_single_acceleration(star, (buffer[j], None))
                    for j in range(len(buffer))])
            
    comm.Barrier()
    comm.isend(local_stars, dest=0)

    if thread_id == 0:
        result = []
        for i in range(num_threads):
            buffer = comm.recv()
            result.append(buffer)

        return result


    
# global_stars = np.array([
#     makeStar(2000, 1, 1, 1),
#     makeStar(3000, 2, 3, 5),
#     makeStar(4000, 5, 4, 1),
#     makeStar(1000, 1, 2, 3),
# ])

# calculate_parallel(global_stars=global_stars)
# print('', flush = True)
# comm.Barrier()

# if thread_id == 0:
#     from sequential import calculate_accelerations

#     print('---------------------\nSEQUENTIAL:', flush = True)
#     print_stars(calculate_accelerations(global_stars))



N=int(sys.argv[1])

from timeit import default_timer as timer

global_stars = generateStars(N)
if thread_id == 0:
    start = timer()
calculate_parallel(global_stars=global_stars)
# comm.Barrier()
if thread_id == 0:
    end = timer()
    print(end-start)
