from scan import Scan
import matplotlib.pyplot as plt
import numpy as np
import sys

def main():
    raw_matrix = Scan()
    raw_matrix.load_data(sys.argv[1])
    peaks = raw_matrix.find_peaks(5000)


if __name__ == "__main__":
    main()
    # Really important for showing of plot.
    plt.show(block=True)
