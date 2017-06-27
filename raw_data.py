import os.path
import sys

import matplotlib.pyplot as plt
import numpy as np
from scipy import io, signal
from scipy.interpolate import interp1d


def load_spectra(file_name, n):
    """
    Load binary data into matrix.
    Reshaping it and multiplying with constant 540.
    """
    if os.path.isfile(file_name):
        f = open(file_name, "r")
        # Load file from binary file
        a = np.fromfile(f, np.uint16, sep="")
        # Reshape to matrix dimensions
        a = np.reshape(a, (n, np.size(a) // n), order='F')
        a = np.dot(a, 540)
        return a
    else:
        print("Error loading file.")
        return -1


def load_offset_chirp():
    """Load published matlab variables."""
    a = io.loadmat(os.getcwd() + "/offset_chirp.mat")
    return a


def remove_detector_offset(spectra, offset):
    """Remove detector offset from signal"""
    for c in range(0, np.shape(spectra)[1]):
        spectra[:, c] = spectra[:, c] - np.transpose(offset)
    return spectra


def apodization(spectra):
    """Apply hann windows for fft apllication."""
    spectra_shape = np.shape(spectra)
    for c in range(0, spectra_shape[1]):
        spectra[:, c] = np.multiply(spectra[:, c], signal.hann(1024))
    return spectra


def remove_dc(spectra):
    """Remove mean value over all ascans from every ascan."""
    for i in range(0, np.shape(spectra)[0]):
        spectra[i, :] = spectra[i, :] - np.mean(spectra[i, :])
    return spectra

def de_chirp(spectra, chirp):
    for i in range(0, np.shape(spectra)[1]):
        f = interp1d(spectra[:, i], chirp)
        spectra[:, i] = f(spectra[:, i])
    return spectra

def main():
    raw_matrix = load_spectra(sys.argv[1], 2 * 512)
    matlab_array = load_offset_chirp()
    sliced_matrix = raw_matrix[:, 0:5000]
    removed_offset_matrix = remove_detector_offset(sliced_matrix, matlab_array['Offset'])
    removed_dc_matrix = remove_dc(removed_offset_matrix)
    apodizated_matrix = apodization(removed_dc_matrix)
    de_chirped_matrix = de_chirp(apodizated_matrix, np.transpose(matlab_array['Chirp']))

    plt.figure(), plt.plot(de_chirped_matrix[:, 1])
    plt.figure(), plt.imshow(de_chirped_matrix)



if __name__ == "__main__":
    main()
    # Really important for showing of plot.
    plt.show(block=True)
