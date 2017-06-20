import sys
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt


def load_data():
    """Load binary data into float vector."""
    # file_name = "/media/levperschin/USB_LP/1_EMS/09052017044007__ascan_2.bin"
    file_name = sys.argv[1]
    f = open(file_name, "r")
    a = np.fromfile(f, dtype=np.float32, sep="")
    return a


def scale_interval_zero_one(matrix):
    """Scale matrix values down to interval [0,1]."""
    matrix = np.array(matrix)
    min_v = np.min(matrix)
    max_v = np.max(matrix)
    quotient = 1.0 / (max_v - min_v)
    return matrix * quotient


def main():
    raw_vector = load_data()
    raw_matrix = np.reshape(raw_vector, (512, int(np.size(raw_vector) / 512)))
    sliced_matrix = raw_matrix[:, 0:10000]
    plt.imshow(sliced_matrix)


if __name__ == "__main__":
    main()
    # Really important for showing of plot.
    plt.show(block=True)
