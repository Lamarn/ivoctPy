import os.path
import sys

import matplotlib.pyplot as plt
import numpy as np
from scipy import io, signal


# from skimage import filters, feature


def load_spectra(file_name, n):
    """Load binary data into scaled matrix."""
    if os.path.isfile(file_name):
        f = open(file_name, "r")
        # Load file from binary file
        a = np.fromfile(f, np.uint16, sep="")
        # Reshape to matrix dimensions
        a = np.reshape(a, (n, np.size(a) // n), order='F')
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


def load_offset_chirp():
    # a = io.loadmat(sys.argv[0].replace(str.split(sys.argv[0])[0], ""))
    a = io.loadmat("/home/levper/git/ivoctPy/offset_chirp.mat")
    return a


def remove_detector_offset(spectra, offset):
    for c in range(0, np.shape(spectra)[1]):
        for i in range(0, np.shape(spectra)[0]):
            spectra[i, c] = np.subtract(spectra[i, c], offset[i])
        print(spectra[:, c])
    plt.imshow(spectra)
    return spectra


def apodization(spectra):
    spectra_shape = np.shape(spectra)
    for c in range(0, spectra_shape[1]):
        for i in range(0,spectra_shape[0]):
            spectra[i, c] = np.multiply(spectra[i, c], signal.hann(spectra_shape[0])[i])
        print(spectra[:, c])
    return spectra


def main():
    raw_matrix = load_spectra(sys.argv[1], 2 * 512)
    matlab_array = load_offset_chirp()
    sliced_matrix = raw_matrix[:, 0:5000]
    r_offset_matrix = remove_detector_offset(sliced_matrix, matlab_array['Offset'])
    # apodizated_matrix = apodization(r_offset_matrix)
    plt.figure(), plt.imshow(r_offset_matrix)


if __name__ == "__main__":
    main()
    # Really important for showing of plot.
    plt.show(block=True)
