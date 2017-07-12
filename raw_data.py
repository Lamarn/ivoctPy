import os.path
import sys

import matplotlib.pyplot as plt
import numpy as np
from scipy import io, signal, fft
from scipy.interpolate import interp1d


def load_spectra(file_name, n):
    """
    Load binary data into matrix.
    Reshape and multiply with constant 540.
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


def remove_dc(spectra):
    """Remove mean value over all ascans from every ascan."""
    for i in range(0, np.shape(spectra)[0]):
        spectra[i, :] = spectra[i, :] - np.mean(spectra[i, :])


def apodization(spectra):
    """Apply hann window for fft apllication."""
    spectra_shape = np.shape(spectra)
    for c in range(0, spectra_shape[1]):
        spectra[:, c] = np.multiply(spectra[:, c], signal.hann(1024))


def de_chirp(spectra, chirp):
    """Interpolate ascans to chirp positions."""
    for i in range(0, np.shape(spectra)[1]):
        f = interp1d(chirp, spectra[:, i])
        spectra[:, i] = f(range(0, 1024))


def fourier_transform(spectra):
    """Apply fft, take the abs and compress with log."""
    for i in range(0, np.shape(spectra)[1]):
        spectra[:, i] = np.abs(fft(np.transpose(spectra[:, i])))
        spectra[:, i] = apply_log(spectra[:, i])


def apply_log(x):
    """Helper function for fourier_transform."""
    return 20 * np.log(x)


def main():
    """Main procedure"""
    raw_matrix = load_spectra(sys.argv[1], 2 * 512)
    matlab_array = load_offset_chirp()
    sliced_matrix = raw_matrix[:, 0:5000]
    plt.figure(), plt.imshow(sliced_matrix)

    remove_detector_offset(sliced_matrix, matlab_array['Offset'])
    remove_dc(sliced_matrix)
    apodization(sliced_matrix)
    de_chirp(sliced_matrix, np.squeeze(matlab_array['Chirp']))
    fourier_transform(sliced_matrix)

    processed_matrix = sliced_matrix[0:512, :]

    # plt.figure(), plt.plot(signal.hann(1024))
    plt.figure(), plt.plot(processed_matrix[:, 1:20])
    plt.figure(), plt.imshow(processed_matrix)


if __name__ == "__main__":
    main()
    # Really important for showing of plot.
    plt.show(block=True)
