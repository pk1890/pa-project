#!/usr/bin/env python3

import mpi4py
mpi4py.rc.recv_mprobe = False

from mpi4py import MPI
import socket
import sys
import numpy as np
import math
from common import calculate_single_force, generateStars, makeStar, calculate_accelerations
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
    
    forces = np.zeros((len(local_stars), 3))
    passed_forces = np.zeros((len(local_stars), 3))

    buffer = local_stars.copy()
    
    # calculate local stars
    for i in range(len(local_stars)):
        star = local_stars[i]
        forces[i] = sum([calculate_single_force(star, local_stars[j])
                for j in range(len(local_stars)) if not i == j])

    receiver_thread = (thread_id + 1) % num_threads
    source_thread = (thread_id - 1) % num_threads

    # ring execution
    repetitions = num_threads // 2
    for i in range(repetitions):
        comm.Isend([buffer, MPI.FLOAT], dest=receiver_thread)
        comm.Isend([passed_forces, MPI.FLOAT], dest=receiver_thread)

        comm.Recv([buffer, MPI.FLOAT], source=source_thread)
        comm.Recv([passed_forces, MPI.FLOAT], source=source_thread)

        for k in range(len(local_stars)):
            star = local_stars[k]
            addition_forces = sum([calculate_single_force(star, buffer[j])
                    for j in range(len(buffer))])
            forces[k] += addition_forces
            if not (i == repetitions-1 and num_threads%2 == 0):
                passed_forces[k] -= addition_forces

    comm.Isend([passed_forces, MPI.FLOAT], dest=((thread_id-repetitions)%num_threads))
    comm.Recv([passed_forces, MPI.FLOAT], source=((thread_id+repetitions)%num_threads))

    for i in range(len(local_stars)):
        forces[i] += passed_forces[i]

    comm.Barrier()
    comm.Isend([forces, MPI.FLOAT], dest=0)

    comm.Barrier()
    if thread_id == 0:
        result = None
        for i in range(num_threads):
            buffer =  np.zeros((len(local_stars), 3))
            comm.Recv([buffer, MPI.FLOAT], source=i)
            
            if result is None:
                result = buffer.copy()
            else:
                result = np.concatenate((result, buffer))

        return result


    


if len(sys.argv) == 1:
    global_stars = np.array([
        makeStar(2000, 1, 1, 1),
        makeStar(3000, 2, 3, 5),
        makeStar(4000, 5, 4, 1),
        makeStar(1000, 1, 2, 3),
    ])

    parallel_forces = calculate_parallel(global_stars=global_stars)

    comm.Barrier()

    if thread_id == 0:
        from sequential import calculate_forces

        print('---------------------\nSEQUENTIAL:', flush = True)
        pprint(calculate_accelerations(global_stars, calculate_forces(global_stars)))
        print('---------------------\nPARALLEL:', flush = True)
        pprint(calculate_accelerations(global_stars, parallel_forces))


else:
    N=int(sys.argv[1])

    from timeit import default_timer as timer

    global_stars = generateStars(N)
    if thread_id == 0:
        start = timer()
    calculate_parallel(global_stars=global_stars)
    if thread_id == 0:
        end = timer()
        print(end-start)
