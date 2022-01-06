import numpy as np
from common import generateStars, dist, calculate_single_acceleration, print_stars
from pprint import pprint

def calculate_accelerations(stars):
    for i in range(len(stars)):
        star = stars[i]
        stars[i][1] = sum([calculate_single_acceleration(star, stars[j])
                for j in range(len(stars)) if not i == j])

    return stars

# print(calculate_accelerations(np.array([np.array([1, 0, 0, 0]), np.array([1, 10, 2, 2])])))

stars = generateStars(5)
calculate_accelerations(stars)
print_stars(stars)
