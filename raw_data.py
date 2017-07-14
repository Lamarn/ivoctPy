import os.path

import numpy as np
from scipy import io, signal, fft
from scipy.interpolate import interp1d


class RawData:
    def __init__(self, start_at):
        self.start_at = start_at
        self.ascan_size = 2 * 512
        self.spectra = []
        self.cut_spectra = []
        self.matlab_array = []

    def load_spectra(self, file_name):
        """
        Load binary data into matrix.
        Reshape and multiply with constant 540.
        """
        if os.path.isfile(file_name):
            f = open(file_name, "r")
            # Load file from binary file
            a = np.fromfile(f, np.uint16, sep="")
            # Reshape to matrix dimensions
            a = np.reshape(a, (self.ascan_size, np.size(a) // self.ascan_size), order='F')
            a = np.dot(a, 540)
            self.spectra = a
            self.cut_spectra = a[:, self.start_at:self.start_at + 5000]
            print("Loading of raw data succefully finished.")
        else:
            print("Error loading file.")

    def load_offset_chirp(self):
        """Load published matlab variables."""
        self.matlab_array = io.loadmat(os.getcwd() + "/offset_chirp.mat")

    def remove_detector_offset(self, offset):
        """Remove detector offset from signal"""
        for c in range(0, np.shape(self.cut_spectra)[1]):
            self.cut_spectra[:, c] = self.cut_spectra[:, c] - np.transpose(offset)

    def remove_dc(self):
        """Remove mean value over all ascans from every ascan."""
        for i in range(0, np.shape(self.cut_spectra)[0]):
            self.cut_spectra[i, :] = self.cut_spectra[i, :] - np.mean(self.cut_spectra[i, :])

    def apodization(self):
        """Apply hann window for fft apllication."""
        spectra_shape = np.shape(self.cut_spectra)
        for c in range(0, spectra_shape[1]):
            self.cut_spectra[:, c] = np.multiply(self.cut_spectra[:, c], signal.hann(1024))

    def de_chirp(self, chirp):
        """Interpolate ascans to chirp positions."""
        for i in range(0, np.shape(self.cut_spectra)[1]):
            f = interp1d(chirp, self.cut_spectra[:, i])
            self.cut_spectra[:, i] = f(range(0, 1024))

    def fourier_transform(self):
        """Apply fft, take the abs and compress with log."""
        for i in range(0, np.shape(self.cut_spectra)[1]):
            self.cut_spectra[:, i] = np.abs(fft(np.transpose(self.cut_spectra[:, i])))
            self.cut_spectra[:, i] = self.apply_log(self.cut_spectra[:, i])

    @staticmethod
    def apply_log(x):
        """Helper function for fourier_transform."""
        return 20 * np.log(x)

    def load_raw_data(self, path):
        self.load_spectra(path)
        self.load_offset_chirp()

    def process_raw_data(self):
        self.remove_detector_offset(self.matlab_array['Offset'])
        self.remove_dc()
        self.apodization()
        self.de_chirp(np.squeeze(self.matlab_array['Chirp']))
        self.fourier_transform()
