from scan import Scan
import matplotlib.pyplot as plt
import numpy as np
import sys


def main():
    scan = Scan()
    scan.load_data(sys.argv[1])
    peaks = scan.find_peaks(10000)
    scan.show_polar(peaks)


if __name__ == "__main__":
    main()
    # Really important for showing of plot.
    plt.show(block=True)
