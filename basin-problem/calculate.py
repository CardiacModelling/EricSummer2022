import basin
import nevis
import numpy as np


def find_labels(h):
    maxima, sn = basin.find_maxima(h)
    label, path_sum = basin.find_basins(h, sn, maxima)
    return label, maxima, path_sum


if __name__ == '__main__':
    data = nevis.gb()

    print("Run this script twice to avoid memory overflow: \n"
          "1) In the first run calculate label, maxima, path_sum; \n"
          "2) In the second run load them and then calculate areas.")

    run_num = input("First or second run? [1/2]: ")
    if run_num == '2':
        label = np.load('res/label.npy')
        maxima = np.load('res/maxima.npy')
        area = basin.count_basin_area(label, len(maxima), data, False)
        np.save('res/area-with-sea.npy', area)
    elif run_num == '1':
        label, maxima, path_sum = find_labels(data)
        np.save('res/maxima.npy', maxima)
        np.save('res/label.npy', label)
        np.save('res/path_sum.npy', path_sum)
    else:
        raise RuntimeError("Invalid input!")

    print("Done!")
