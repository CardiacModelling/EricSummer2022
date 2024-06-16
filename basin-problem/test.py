import basin
import numpy as np

arrows = [
    '↓',
    '↘',
    '→',
    '↗',
    '↑',
    '↖',
    '←',
    '↙',
    "@",  # (ab)using index -1 here
]


def run_algorithm(h):
    print("The input height array:")
    print(h)

    # calculate the list of maxima and the steepest neighbour for each point
    maxima, sn = basin.find_maxima(h)
    print("The coordinates of the local maxima:")
    print(maxima)
    print("The steepest neighbour of each point:")
    print(sn)

    print("which can be drawn as:")
    for x in sn:
        for y in x:
            print(arrows[y], end=" ")
        print()

    label, path_sum = basin.find_basins(h, sn, maxima)
    print("The b.o.a. of each point:")
    print(label)

    print("The sum of all paths for each b.o.a.:")
    print(path_sum)

    print()


run_algorithm(np.array([
    [4, 2, 2, 2, 2, 4],
    [1, 2, 2, 2, 2, 2],
    [5, 2, 2, 3, 3, 3],
    [1, 1, 2, 3, 4, 3],
    [1, 1, 2, 3, 4, 3],
]))


run_algorithm(np.array([
    [2, 2, 2, 2, 2, 2,],
    [2, 2, 2, 2, 2, 2,],
    [2, 2, 2, 2, 2, 2,],
    [2, 2, 2, 2, 2, 2,],
    [2, 2, 2, 2, 2, 2,],
    [2, 2, 2, 2, 2, 2,],
]))