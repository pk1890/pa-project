import numpy as np
import random

def generateStar():
    mass = (random.random()*10000)+1000
    x, y, z= random.random()*100, random.random()*100, random.random()*100
    return np.array([mass, x, y, z])

def generateStars(N: int):
    return np.array([generateStar() for i in range(N)])

def dist(star1, star2):
    return np.sqrt(sum(map(lambda x: (x[0]+x[1])**2, zip(star1[1:], star2[1:]))))