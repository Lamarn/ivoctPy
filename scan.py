import os.path
import numpy as np
import time
import math
import matplotlib.pyplot as plt
from skimage import filters, feature


class Scan:
    def __init__(self):
        self.__matrix = np.array([0])

    def show_matrix(self):
        """Plot current state of the matrix."""
        plt.figure(), plt.imshow(self.__matrix)

    def get_matrix(self):
        """Get the current matrix returned."""
        return self.__matrix

    def load_data(self, file_name):
        """Load binary data into scaled matrix."""
        if os.path.isfile(file_name):
            f = open(file_name, "r")
            # Load file from binary file
            self.__matrix = np.fromfile(f, np.float32, sep="")
            # Reshape to matrix dimensions
            self.__matrix = np.reshape(self.__matrix, (512, np.size(self.__matrix) // 512), order='F')
            self.__matrix = self.__scale_interval_zero_one(self.__matrix)
            print("Loading of data succefully finished.")
        else:
            print("Error loading file.")

    @staticmethod
    def __scale_interval_zero_one(matrix):
        """Scale matrix values down to interval [0, 1]."""
        matrix = np.array(matrix)
        min_v = np.min(matrix)
        max_v = np.max(matrix)
        quotient = 1.0 / (max_v - min_v)
        return matrix * quotient

    def __remove_second_column(self):
        """Remove every second column of the matrix. Maybe never will be used."""
        new_matrix = np.empty((np.shape(self.__matrix)[0], np.shape(self.__matrix)[1] // 2))
        for i in range(0, np.shape(self.__matrix)[1]):
            if i % 2 == 0:
                new_matrix[:, (i - 1) // 2] = self.__matrix[:, i]
        self.__matrix = new_matrix

    def find_peaks(self, width=None, debug=False):
        """Find peaks from matrix showing a sinus curve."""

        if width is not None:
            matrix = self.__matrix[:, 0:width]

        min_width = 850
        max_width = 1400

        skin_layer_cut = matrix[85:120, :]
        skin_layer_med = filters.median(skin_layer_cut, np.ones([5, 5]))
        skin_layer = feature.canny(skin_layer_med, sigma=1)

        if debug:
            plt.figure(), plt.imshow(skin_layer_med)
            plt.figure(), plt.imshow(skin_layer)
            plt.figure(), plt.imshow(skin_layer)

        skin_layer_shape = np.shape(skin_layer)
        peaks = []
        min_value = skin_layer_shape[0]

        # Find first peak
        for c in range(0, 800):
            for a in range(skin_layer_shape[0] - 1, 0, -1):
                if skin_layer[a, c] and a < min_value:
                    min_value = a
                    peak_at = c
        peaks.append(peak_at)

        # Find following peaks
        while peak_at + max_width < skin_layer_shape[1]:
            min_value = skin_layer_shape[0]
            temp_matrix = skin_layer[:, peaks[-1] + min_width: peaks[-1] + max_width]
            for c in range(0, np.shape(temp_matrix)[1]):
                for a in range(skin_layer_shape[0] - 1, 0, -1):
                    if skin_layer[a, c] and a < min_value:
                        min_value = a
                        peak_at = c
            peak_at = peaks[-1] + min_width + peak_at
            peaks.append(peak_at)
        print("Found peaks: " + str(peaks) + ". Searched until: " + str(width))

        if debug:
            for i in peaks:
                skin_layer[:, i] = 1
            plt.figure(), plt.imshow(skin_layer)
        return peaks

    def show_polar(self, peaks):
        """Create polar views, save and plot them."""
        polar_vec = []
        length_peaks = len(peaks)
        for i in range(0, length_peaks):
            if i + 1 < length_peaks:
                matrix = self.__matrix[:, peaks[i]: peaks[i + 1]]
                polar_matrix = np.empty([1024, 1024])
                matrix_shape = np.shape(matrix)

                for x in range(0, matrix_shape[1]):
                    for y in range(0, matrix_shape[0]):
                        xp = round(y * math.cos(2 * x * math.pi / matrix_shape[1]) + 512)
                        yp = round(y * math.sin(2 * x * math.pi / matrix_shape[1]) + 512)
                        polar_matrix[xp, yp] = matrix[y, x]

                polar_vec.append(polar_matrix)
                plt.figure(), plt.imshow(polar_matrix)
        print("Succesfully saved all polar images.")
        return polar_vec
