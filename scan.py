import os.path
import math
import numpy as np
import matplotlib.pyplot as plt
from skimage import filters, feature
from skimage.measure import CircleModel, ransac


class Scan:
    def __init__(self, start_at):
        self.matrix = []
        self.cut_matrix = []
        self.peaks = []
        self.polar_views = []
        self.debug = False
        self.ascan_size = 512
        self.start_at = start_at
        self.surface_threshold = 0.37

    def plot_cut_matrix(self):
        plt.figure(), plt.imshow(self.cut_matrix)

    def load_data(self, file_name):
        """Load binary data into scaled matrix."""
        if os.path.isfile(file_name):
            f = open(file_name, "r")
            # Load file from binary file
            self.matrix = np.fromfile(f, np.float32, sep="")
            # Reshape to matrix dimensions
            self.matrix = np.reshape(self.matrix, (self.ascan_size, np.size(self.matrix) // self.ascan_size), order='F')
            self.matrix = self.__scale_interval_zero_one(self.matrix)
            self.cut_matrix = self.matrix[:, self.start_at:self.start_at + 5000]
            self.preprocess_matrix()
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
        print("Matrix scaled.")
        return matrix * quotient

    def find_peaks(self):
        """Find peaks from matrix, showing a sinus curve."""
        matrix = self.cut_matrix

        min_width = 850
        max_width = 1400

        skin_layer_cut = matrix[85:120, :]
        skin_layer_med = filters.median(skin_layer_cut, np.ones([5, 5]))
        skin_layer = feature.canny(skin_layer_med, sigma=1)

        if self.debug:
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

        self.peaks = peaks
        print("Found peaks: " + str(peaks) + ". Searched from: " + str(self.start_at) + " until: " + str(
            self.start_at + 5000))

        # Plot vertical line, where peak was found.
        if self.debug:
            for i in peaks:
                skin_layer[:, i] = 1
            plt.figure(), plt.imshow(skin_layer)

    def create_polar_views(self):
        """Create polar views and save in array."""
        polar_vec = []
        length_peaks = len(self.peaks)
        for i in range(0, length_peaks):
            if i + 1 < length_peaks:
                matrix = self.cut_matrix[:, self.peaks[i]: self.peaks[i + 1]]
                polar_matrix = np.empty([1024, 1024])
                matrix_shape = np.shape(matrix)

                for x in range(0, matrix_shape[1]):
                    for y in range(0, matrix_shape[0]):
                        xp = round(y * math.cos(2 * x * math.pi / matrix_shape[1]) + self.ascan_size)
                        yp = round(y * math.sin(2 * x * math.pi / matrix_shape[1]) + self.ascan_size)
                        polar_matrix[xp, yp] = matrix[y, x]

                polar_vec.append(polar_matrix)
                print(polar_matrix)
                if self.debug:
                    plt.figure(), plt.imshow(polar_matrix)
        self.polar_views = polar_vec
        print("Succesfully saved all polar images.")

    def find_circles(self):
        for i in range(0, len(self.polar_views)):
            self.polar_views[i] = self.interpolation_polar_view(self.polar_views[i])
            polar_view_canny = feature.canny(filters.median(self.polar_views[i], np.ones([5, 5])))

            points = np.array(np.nonzero(polar_view_canny)).T
            model_robust, inliers = ransac(points, CircleModel, min_samples=3, residual_threshold=2, max_trials=1000)
            cy, cx, r = model_robust.params
            f, (ax0, ax1) = plt.subplots(1, 2)

            ax0.imshow(self.polar_views[i])
            ax1.imshow(self.polar_views[i])

            ax1.plot(points[inliers, 1], points[inliers, 0], 'b.', markersize=1)
            ax1.plot(points[~inliers, 1], points[~inliers, 0], 'g.', markersize=1)

            circle = plt.Circle((cx, cy), radius=r, facecolor='none', linewidth=2)
            ax0.add_patch(circle)

    @staticmethod
    def cartesian_coordinates(rho, fi):
        return round(rho * math.cos(fi)), round(rho * math.sin(fi))

    @staticmethod
    def polar_coordinates(x, y):
        if x == 0.0:
            x = 0.1
        rho = round(math.sqrt(x ** 2 + y ** 2))
        fi = round(math.degrees(math.atan(y / x)))
        # Add degrees adapted to quadrant
        if x < 0 and y >= 0:  # second quadrant
            fi += 180
        elif x < 0 and y < 0:  # third quadrant
            fi += 180
        elif x >= 0 and y < 0:  # fourth quadrant
            fi += 360
        return rho, fi

    def interpolation_polar_view(self, matrix, width):
        for x in range(0, np.shape(matrix)[1]):
            for y in range(0, np.shape(matrix)[0]):
                x_new = x - 512
                y_new = y - 512
                if matrix[x, y] == 0 and (x_new ** 2 + y_new ** 2) < 262144:
                    values_in_range = []
                    rho, fi = self.polar_coordinates(x_new, y_new)
                    if self.debug:
                        print("[" + str(rho) + ", " + str(fi) + "]")
                    for i in range(-width, width):
                        for j in range(-2, 2):
                            x_near, y_near = self.cartesian_coordinates(rho + j, fi + i)
                            near_value = matrix[x_near, y_near]
                            if near_value != 0:
                                values_in_range.append(near_value)
                    if len(values_in_range) > 0:
                        matrix[x, y] = np.average(values_in_range)
                    values_in_range.clear()
        return matrix

    def preprocess_matrix(self):
        """Preprocess values of matrix, to get a homogeneous image."""
        self.cut_matrix[self.cut_matrix > self.surface_threshold] = 1.0
        self.cut_matrix[self.cut_matrix < 0] = 0.0
        m1 = np.ma.masked_inside(self.cut_matrix, 0.0, 0.1)
        m1 = 0.1
        m2 = np.ma.masked_inside(self.cut_matrix, 0.1, 0.2)
        m2 = 0.2
        m3 = np.ma.masked_inside(self.cut_matrix, 0.2, 0.3)
        m3 = 0.3
        m4 = np.ma.masked_inside(self.cut_matrix, 0.3, 0.37)
        m4 = 0.37

    def load_scan(self, path):
        self.load_data(path)

    def process_scan(self):
        self.find_peaks()
        self.create_polar_views()
