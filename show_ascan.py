import os.path
import sys

import matplotlib.pyplot as plt
import numpy as np
from skimage import filters, feature


def load_data():
    """Load binary data into scaled matrix."""
    file_name = sys.argv[1]
    if os.path.isfile(file_name):
        f = open(file_name, "r")
        # Load file from binary file
        a = np.fromfile(f, np.float32, sep="")
        # Reshape to matrix dimensions
        a = np.reshape(a, (512, np.size(a) // 512), order='F')
        a = scale_interval_zero_one(a)
        return a
    else:
        print("Error loading file.")
        return -1


def scale_interval_zero_one(matrix):
    """Scale matrix values down to interval [0, 1]."""
    matrix = np.array(matrix)
    min_v = np.min(matrix)
    max_v = np.max(matrix)
    quotient = 1.0 / (max_v - min_v)
    return matrix * quotient


def remove_second_column(matrix):
    """Remove every second column of the matrix."""
    new_matrix = np.empty((np.shape(matrix)[0], np.shape(matrix)[1] // 2))
    for i in range(0, np.shape(matrix)[1]):
        if i % 2 == 0:
            new_matrix[:, (i - 1) // 2] = matrix[:, i]
    return new_matrix


def find_peaks(matrix):
    """Find peaks from matrix."""
    min_width = 800
    max_width = 1300

    med_matrix = filters.median(scale_interval_zero_one(matrix), np.ones([5, 5]))
    plt.figure(), plt.imshow(med_matrix)
    canny_matrix = feature.canny(med_matrix, sigma=1)
    plt.figure(), plt.imshow(canny_matrix)
    skin_layer = canny_matrix[85:120, :]
    plt.figure(), plt.imshow(skin_layer)

    peaks = []
    peak_at_temp = 0
    max_value = 0

    # Find first peak
    skin_layer_shape = np.shape(skin_layer)
    for c in range(0, 800):
        for a in range(0, skin_layer_shape[0]):
            if skin_layer[a, c] and a > max_value:
                max_value = a
                peak_at_temp = c
    peak_at = peak_at_temp
    peaks.append(peak_at)

    # Find following peaks
    while peak_at + max_width < skin_layer_shape[1]:
        max_value = 0
        temp_matrix = skin_layer[:, peak_at + min_width: peak_at + max_width]
        for c in range(0, np.shape(temp_matrix)[1]):
            for a in range(0, skin_layer_shape[0]):
                if skin_layer[a, c] and a > max_value:
                    max_value = a
                    peak_at_temp = c
        peak_at = peak_at + min_width + peak_at_temp
        peaks.append(peak_at)
    print("Found peaks: " + str(peaks))
    return peaks


def main():
    raw_matrix = load_data()
    sliced_matrix = raw_matrix[:, 0:5000]
    plt.figure(), plt.imshow(sliced_matrix)
    peaks = find_peaks(sliced_matrix)


if __name__ == "__main__":
    main()
    # Really important for showing of plot.
    plt.show(block=True)
