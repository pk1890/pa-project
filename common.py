import numpy as np
import random
from mpi4py import MPI

G = 6.6743015E-11

def calculate_single_force(star1, star2):
    return G/(dist(star1, star2)**3)*(star1[1:] - star2[1:])

def calculate_accelerations(stars, forces):
    accelerations = np.zeros((len(stars), 3))
    for i in range(len(stars)):
        accelerations[i] = forces[i] / stars[i][0]
    return accelerations
    

def generateStar():
    mass = (random.random()*10000)+1000
    x, y, z= random.random()*1000, random.random()*1000, random.random()*1000
    return np.array([mass, x, y, z])

def makeStar(mass, x, y, z):
    return np.array([mass, x, y, z])


def generateStars(N: int):
    return np.array([(generateStar()) for i in range(N)])

def generateStarsParallel(N: int):
    comm = MPI.COMM_WORLD
    thread_id = comm.Get_rank()

    stars = np.zeros((N, 4))
    if thread_id == 0:
        stars = generateStars(N)
    comm.Bcast([stars, MPI.FLOAT], root=0)
    return stars

def dist(star1, star2):
    return np.sqrt(sum(map(lambda x: (x[0]-x[1])**2, zip(star1[1:], star2[1:])))+ 1e-20)