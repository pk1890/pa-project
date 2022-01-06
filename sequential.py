import numpy as np
from common import generateStars, dist

G = 6.6743015E-11

def calculate_accelerations(stars):
    acc = []
    for i in range(len(stars)):
        star = stars[i]
        acc.append(G*sum([stars[j][0]/(dist(star, stars[j])**3)*(star[1:] - stars[j][1:])
                for j in range(len(stars)) if not i == j]))

    return np.array(acc)

# print(calculate_accelerations(np.array([np.array([1, 0, 0, 0]), np.array([1, 10, 2, 2])])))

stars = generateStars(5)
print(stars)
print(calculate_accelerations(stars))