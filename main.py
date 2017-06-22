import sys
import numpy as np
from skimage import filters, feature
import matplotlib.pyplot as plt


def load_data():
    """Load binary data into float vector."""
    file_name = sys.argv[1]
    f = open(file_name, "r")
    if f == -1:
        print("Error loading file.")
        return -1
    else:
        a = np.fromfile(f, np.float32, sep="")
        return a


def scale_interval_zero_one(matrix):
    """Scale matrix values down to interval [0,1]."""
    matrix = np.array(matrix)
    min_v = np.min(matrix)
    max_v = np.max(matrix)
    quotient = 1.0 / (max_v - min_v)
    return matrix * quotient


def remove_second_column(matrix):
    """Remove every second column of the matrix, because it is not used."""
    new_matrix = np.empty((np.shape(matrix)[0], np.shape(matrix)[1] // 2))
    for i in range(0, np.shape(matrix)[1]):
        if i % 2 == 0:
            new_matrix[:, (i - 1) // 2] = matrix[:, i]
    return new_matrix


def main():
    raw_vector = load_data()
    raw_matrix = np.reshape(raw_vector, (512, np.size(raw_vector) // 512), order='F')
    sliced_matrix = raw_matrix[:, 0:10000]
    med_matrix = filters.median(scale_interval_zero_one(sliced_matrix), np.ones([5, 5]))
    canny_matrix = feature.canny(med_matrix, sigma=1)
    print(feature.peak_local_max(canny_matrix[85:120, :]))
    plt.imshow(canny_matrix[85:120, 0:2500])


if __name__ == "__main__":
    main()
    # Really important for showing of plot.
    plt.show(block=True)
