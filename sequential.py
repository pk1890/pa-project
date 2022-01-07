import numpy as np
from common import generateStars, calculate_single_force
from pprint import pprint

def calculate_forces(stars):
    forces = np.zeros((len(stars), 3))
    for i in range(len(stars)):
        star = stars[i]
        forces[i] = sum([calculate_single_force(star, stars[j])
                for j in range(len(stars)) if not i == j])

    return forces


# print(calculate_forces(np.array([np.array([1, 0, 0, 0]), np.array([1, 10, 2, 2])])))

# from timeit import default_timer as timer

# stars = generateStars(1000)
# start=timer()
# forces = calculate_forces(stars)
# end = timer()
# print(end-start)
# # print_stars(stars, forces)
