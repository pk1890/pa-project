import numpy as np
import random

G = 6.6743015E-11

def print_stars(stars):
    for star in stars:
        print("""====
        mass: %s
        coords: %s
        acceleration: %s""" % (star[0][0], star[0][1:], star[1]))

def calculate_single_acceleration(s1, s2):
    star1 = s1[0]
    star2 = s2[0]
    return G*star2[0]/(dist(star1, star2)**3)*(star1[1:] - star2[1:])

def generateStar():
    mass = (random.random()*10000)+1000
    x, y, z= random.random()*100, random.random()*100, random.random()*100
    return np.array([mass, x, y, z]), np.zeros(3)

def makeStar(mass, x, y, z):
    return np.array([mass, x, y, z]), np.zeros(3)


def generateStars(N: int):
    return np.array([(generateStar()) for i in range(N)])

def dist(star1, star2):
    return np.sqrt(sum(map(lambda x: (x[0]+x[1])**2, zip(star1[1:], star2[1:]))))