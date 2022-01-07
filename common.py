import numpy as np
import random

G = 6.6743015E-11

def print_stars(stars, acc):
    for star, a in zip(stars, acc):
        print("""====
        mass: %s
        coords: %s
        acceleration: %s""" % (star[0], star[1:], a))

def calculate_single_acceleration(star1, star2):
    return G*star2[0]/(dist(star1, star2)**3)*(star1[1:] - star2[1:])

def generateStar():
    mass = (random.random()*10000)+1000
    x, y, z= random.random()*100, random.random()*100, random.random()*100
    return np.array([mass, x, y, z])

def makeStar(mass, x, y, z):
    return np.array([mass, x, y, z])


def generateStars(N: int):
    return np.array([(generateStar()) for i in range(N)])

def dist(star1, star2):
    return np.sqrt(sum(map(lambda x: (x[0]+x[1])**2, zip(star1[1:], star2[1:]))))